"""
Create and run shell commands in a virtualenv
"""

import os

from itertools import chain
from pathlib import Path
from subprocess import CompletedProcess
from typing import Dict, List, Optional, Tuple, Union

from packaging.version import Version

from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run, run_command_lineoutput, DEFAULT_ENCODINGS

from ..exceptions import PythonSetupError


class VirtualEnv:
    """
    Virtualenv from python code
    """
    def __init__(self, path: Path, python_command: str) -> None:
        self.path = path
        self.python_command = python_command
        self.python_version = self.get_python_version_info()
        if not self.path.exists():
            self.create()

    def __repr__(self) -> str:
        return f'{self.path} python {self.python_version}'

    def setup_environment(self, env: dict = None) -> dict:
        """
        Set variables to run commands in the virtual environment
        """
        if env is None:
            env = os.environ.copy()
        env['PATH'] = os.pathsep.join([str(self.path.joinpath('bin')), env['PATH']])
        env['VIRTUAL_ENV'] = str(self.path)
        return env

    def get_python_version_info(self) -> Version:
        """
        Get detailed python version info for self.python_version command
        """
        command = (self.python_command, '--version')
        try:
            stdout, _stderr = run_command_lineoutput(*command)
            return Version(stdout[0].replace('Python ', ''))
        except CommandError as error:
            raise PythonSetupError(
                f'Error checking python version for {self.python_command}: {error}'
            ) from error

    def create(self) -> None:
        """
        Create virtualenv for dependency processing to the cache directory with specified python version
        """
        command = (self.python_command, '-m', 'venv', str(self.path))
        try:
            print(f'create virtualenv: {self.path}')
            run(*command)
        except CommandError as error:
            raise PythonSetupError(f'Error creating virtualenv {self.path}: {error}') from error

    def install_editable(self, paths: list) -> CompletedProcess:
        """
        Install python package as editable dependency to processor virtualenv
        """
        if isinstance(paths, str):
            paths = [paths]
        args = ['pip', 'install'] + list(chain(*[['--editable', path] for path in paths]))
        return self.run(*args)

    def install_packages(self, packages: Union[str, List[str]]) -> CompletedProcess:
        """
        Install python packages as editable dependency to processor virtualenv
        """
        if isinstance(packages, str):
            packages = [packages]
        args = ['pip', 'install'] + packages
        return self.run(*args)

    def install_requirement(self, paths: Union[str, List[str]]) -> CompletedProcess:
        """
        Install python requirements lists to processor virtualenv
        """
        if isinstance(paths, str):
            paths = [paths]
        args = ['pip', 'install'] + list(chain(*[['--requirement', path] for path in paths]))
        return self.run(*args)

    def run(self,
            *args,
            cwd: str = None,
            expected_return_codes: Optional[List[int]] = None,
            env: Optional[Dict] = None,
            timeout: Union[int, float] = None) -> CompletedProcess:
        """
        Run shell command in virtualenv context
        """
        env = self.setup_environment(env)
        kwargs = {
            'cwd': cwd,
            'expected_return_codes': expected_return_codes,
            'env': self.setup_environment(env),
            'timeout': timeout,
        }
        return run(*args, **kwargs)

    def run_command_lineoutput(
            self,
            *args,
            cwd: str = None,
            expected_return_codes: Optional[List[int]] = None,
            env: Optional[Dict] = None,
            timeout: Union[int, float] = None,
            encodings: List[str] = DEFAULT_ENCODINGS) -> Tuple[List[str], List[str]]:
        """
        Run shell command with line output in virtualenv context
        """
        kwargs = {
            'cwd': cwd,
            'expected_return_codes': expected_return_codes,
            'env': self.setup_environment(env),
            'timeout': timeout,
            'encodings': encodings,
        }
        return run_command_lineoutput(*args, **kwargs)
