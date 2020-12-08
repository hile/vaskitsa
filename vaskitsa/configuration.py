"""
Parser for code generatation repository configuration
"""

import os

from pathlib import Path

from cli_toolkit.configuration import YamlConfiguration

from .documentation.configuration import DocumentationConfiguration
from .documentation.sphinx.configuration import SphinxConfiguration
from .hooks.configuration import HooksConfiguration

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
    Documentation configuration for repository in yml format
    """
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

    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False):
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
    def git_repository(self):
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
    def python_repository(self):
        """
        Return python repository for directory
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from .python.repository import Repository
        if 'python' not in self.__tree_instances__:
            self.__tree_instances__['python'] = Repository(
                self.__path__.parent,
                configuration=self
            )
        return self.__tree_instances__['python']

    @property
    def sphinx_generator(self):
        """
        Return sphinx document generator for directory
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from .documentation.sphinx.repository import AutodocRepositoryGenerator
        if 'sphinx_generator' not in self.__tree_instances__:
            self.__tree_instances__['sphinx_generator'] = AutodocRepositoryGenerator(
                self.__path__.parent,
                configuration=self
            )
        return self.__tree_instances__['sphinx_generator']
