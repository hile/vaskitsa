"""
Python package dependencies processor
"""
import os
import re

from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
from typing import List, Optional, Tuple, Union

from ..exceptions import PythonSetupError
from .requirements import RequirementsFile
from .venv import VirtualEnv

DEFAULT_PYTHON_COMMAND = 'python3'
UPLOAD_VENV_DIRECTORY = 'update'
VENV_DIRECTORY = 'venv'

UPLOAD_ENVIRONMENT_PACKAGES = (
    'twine==3.8.0',
)
ARTIFACT_REGISTRY_PACKAGES = (
    'keyrings.google-artifactregistry-auth==1.0.0',
)
CLEAR_VAR_PREFIXES = (
    'TWINE_',
)
DEFAULT_IGNORED_PACKAGES = (
    'pip',
    'setuptools',
    'wheel',
)

GOOGLE_ARTIFACT_REGISTRY_PATTERN = r'^https://[a-z0-9-]+-python.pkg.dev/.*$'


class PythonRepository:
    """
    Base class for python package registries
    """
    pattern: Optional[str] = None
    clear_env: bool = False
    environment_packages: Tuple[str] = UPLOAD_ENVIRONMENT_PACKAGES
    required_packages: Tuple[str]

    def __repr__(self) -> str:
        return 'Generic PyPI registry'

    def install_packages(self, virtualenv):
        """
        Install packages required for the repository to the specified virtualenv
        """
        packages = list(self.environment_packages) + list(self.required_packages)
        print(f'Install packages to {virtualenv}')
        virtualenv.install_packages(packages)


class GoogleArtifactRegistry(PythonRepository):
    """
    Google artifact repository parameters
    """
    pattern: str = re.compile(GOOGLE_ARTIFACT_REGISTRY_PATTERN)
    clear_env: bool = True
    required_packages: Tuple[str] = ARTIFACT_REGISTRY_PACKAGES

    def __repr__(self) -> str:
        return 'Google Artifact Registry'


class DependenciesProcessor:
    """
    Processor for python package dependencies
    """
    __repository_loaders__: Tuple[PythonRepository] = (
        GoogleArtifactRegistry,
    )
    __cache_directory__: TemporaryDirectory
    python_command: str
    ignored: Tuple[str]
    __upload_virtulenv__: Optional[VirtualEnv]
    __virtulenv__: Optional[VirtualEnv]

    def __init__(self,
                 python_command: str = DEFAULT_PYTHON_COMMAND,
                 ignored: Tuple[str] = DEFAULT_IGNORED_PACKAGES) -> None:
        self.python_command = python_command
        # pylint: disable=consider-using-with
        self.__cache_directory__ = TemporaryDirectory()
        self.ignored = ignored
        self.__virtulenv__ = None
        self.__upload_virtulenv__ = None

    def __repr__(self) -> str:
        return str(self.cache_directory)

    @property
    def cache_directory(self) -> Path:
        """
        Return self.__cache_directory__ TemporaryDirectory object as pathlib.Path
        """
        return Path(self.__cache_directory__.name)

    @property
    def packages_directory(self) -> Path:
        """
        Directory for downloaded packages
        """
        return self.cache_directory.joinpath('packages')

    @property
    def upload_virtualenv(self) -> VirtualEnv:
        """
        Virtualenv for processor in cache directory
        """
        if self.__upload_virtulenv__ is None:
            self.__upload_virtulenv__ = VirtualEnv(
                self.cache_directory.joinpath(UPLOAD_VENV_DIRECTORY),
                self.python_command,
            )
        return self.__upload_virtulenv__

    @property
    def virtualenv(self) -> VirtualEnv:
        """
        Virtualenv for processor in cache directory
        """
        if self.__virtulenv__ is None:
            self.__virtulenv__ = VirtualEnv(
                self.cache_directory.joinpath(VENV_DIRECTORY),
                self.python_command,
            )
        return self.__virtulenv__

    def install_editable(self, paths: List[Union[str, Path]] = list) -> CompletedProcess:
        """
        Install python package as editable dependency to processor virtualenv
        """
        return self.virtualenv.install_editable(paths)

    def install_packages(self, paths: List[Union[str, Path]] = list) -> CompletedProcess:
        """
        Install python packages to processor virtualenv
        """
        return self.virtualenv.install_packages(paths)

    def install_requirement(self, paths: List[Union[str, Path]] = list) -> CompletedProcess:
        """
        Install python requirements lists to processor virtualenv
        """
        return self.virtualenv.install_requirement(paths)

    def load_requirements(self) -> RequirementsFile:
        """
        Get python packages as frozen requirements from virtualenv
        """
        stdout, _stderr = self.virtualenv.run_command_lineoutput(
            'pip', 'list',
            '--format=freeze',
            '--local',
            '--exclude-editable',
        )
        path = self.cache_directory.joinpath('dependencies.txt')
        with path.open(mode='w', encoding='utf-8') as filedescriptor:
            filedescriptor.write('\n'.join(stdout))
        requirements = RequirementsFile(path, ignored=self.ignored)
        requirements.load()
        return requirements

    def download_requirements(self, requirements: Optional[Union[str, Path]] = None) -> Path:
        """
        Download requirements specified in requirements file to local cache directory
        """
        if requirements is None:
            requirements = self.load_requirements()
        self.virtualenv.run(
            'pip', 'download',
            f'--dest={self.packages_directory}',
            f'--requirement={requirements}'
        )

    def get_repository_loader(self, repository: str) -> PythonRepository:
        """
        Match artifact registry by repository name string
        """
        for loader_class in self.__repository_loaders__:
            loader = loader_class()
            pattern = re.compile(loader.pattern)
            if loader.pattern and pattern.match(repository):
                return loader
        return PythonRepository()

    def setup_upload_environment(self, repository: str) -> PythonRepository:
        """
        Set up pacakges for upload environment
        """
        print(f'Set up upload environment for {repository}')
        loader = self.get_repository_loader(repository)
        loader.install_packages(self.upload_virtualenv)
        return loader

    @staticmethod
    def get_clear_upload_env(
            clear_env: bool = False,
            clear_vars: Optional[List[str]] = None) -> dict:
        """
        Get environment without upload twine variables
        """
        def match_prefixes(value):
            for prefix in CLEAR_VAR_PREFIXES:
                if value[:len(prefix)] == prefix:
                    return True
            return False

        env = os.environ.copy()
        clear_vars = clear_vars if clear_vars else []
        if clear_env:
            for var in list(env):
                if match_prefixes(var) or var in clear_vars:
                    del env[var]
        return env

    def remove_ignored_packages(self) -> None:
        """
        Remove ignored packages from the download directory to avoid
        uploading the packages with twine
        """
        def match_ignored(name) -> bool:
            """
            Match package filename to ignore file lists
            """
            for item in self.ignored:
                pattern = fr'^{item}-\d+.*$'
                if re.compile(pattern).match(name):
                    return True
            return False

        if not self.packages_directory.is_dir():
            return
        for package in self.packages_directory.iterdir():
            print(f'process {package}')
            if match_ignored(package.name):
                package.unlink()

    def upload_to_repository(
            self,
            repository: str,
            clear_vars: Optional[List[str]] = None) -> CompletedProcess:
        """
        Upload packages to specified repository with twine
        """
        if not self.packages_directory.is_dir():
            raise PythonSetupError(f'No such directory: {self.packages_directory}')
        loader = self.setup_upload_environment(repository)
        env = self.get_clear_upload_env(loader.clear_env, clear_vars)

        self.remove_ignored_packages()

        print(f'Upoad packages to {loader} repository {repository}')
        return self.upload_virtualenv.run(
            'twine',
            '--no-color',
            'upload',
            '--non-interactive',
            '--skip-existing',
            '--verbose',
            f'--repository-url={repository}',
            f'{self.packages_directory}/*',
            env=env,
        )
