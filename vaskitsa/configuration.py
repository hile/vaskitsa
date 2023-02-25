"""
Parser for code generatation repository configuration
"""
import os

from pathlib import Path
from typing import Dict, Optional, Union, TYPE_CHECKING

from sys_toolkit.configuration import YamlConfiguration

from .documentation.configuration import DocumentationConfiguration
from .documentation.sphinx.configuration import SphinxConfiguration
from .hooks.configuration import HooksConfiguration

if TYPE_CHECKING:
    from .documentation.sphinx.package import AutodocPackageGenerator
    from .git.repository import GitRepository
    from .python.package import Package

REPOSITORY_CONFIGURATION = '.vaskitsa.yml'

DEFAULT_IGNORED_DIRECTORIES = [
    '.eggs/',
    '.pytest_cache/',
    '__pycache__/',
    '.git/',
    '.tox/',
    '*.egg-info/',
    'dist/',
    'build/',
    'public/',
    'docs/',
]


class Configuration(YamlConfiguration):
    """
    Documentation configuration for repository in YAML format
    """
    __tree_instances__: Dict
    __default_settings__ = {
        'ignored_directories': DEFAULT_IGNORED_DIRECTORIES,
        'test_directories': (
            'tests',
        )
    }
    __section_loaders__ = (
        DocumentationConfiguration,
        HooksConfiguration,
        SphinxConfiguration,
    )

    def __init__(self,
                 path: Optional[Union[str, Path]] = None,
                 parent: 'Configuration' = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        if path is None:
            path = Path(os.getcwd())
        if not isinstance(path, Path):
            path = Path(path).expanduser()

        super().__init__(
            path.joinpath(REPOSITORY_CONFIGURATION),
            parent=parent,
            debug_enabled=debug_enabled,
            silent=silent
        )
        self.__tree_instances__ = {}

    @property
    def git_repository(self) -> 'GitRepository':
        """
        Return git repository for directory
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from .git.repository import GitRepository
        if 'git' not in self.__tree_instances__:
            self.__tree_instances__['git'] = GitRepository(
                self.__path__.parent,
                configuration=self
            )
        return self.__tree_instances__['git']

    @property
    def python_package(self) -> 'Package':
        """
        Return python package for directory
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from .python.package import Package
        if 'python' not in self.__tree_instances__:
            self.__tree_instances__['python'] = Package(
                self.__path__.parent,
                configuration=self
            )
        return self.__tree_instances__['python']

    @property
    def sphinx_generator(self) -> 'AutodocPackageGenerator':
        """
        Return sphinx document generator for directory
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from .documentation.sphinx.package import AutodocPackageGenerator
        if 'sphinx_generator' not in self.__tree_instances__:
            self.__tree_instances__['sphinx_generator'] = AutodocPackageGenerator(
                self.__path__.parent,
                configuration=self
            )
        return self.__tree_instances__['sphinx_generator']
