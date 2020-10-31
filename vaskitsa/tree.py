"""
Extend systematic_files.tree.Tree for vaskitsa
"""

from pathlib import Path
from systematic_cli.base import Meta
from systematic_files.tree import Tree

from .configuration import Configuration


class RepositoryTree(Tree, metaclass=Meta):
    """
    Abstraction for source code repository trees
    """
    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls, path, name=None, create_missing=False, sorted=True, mode=None,
                excluded=list, configuration=None):
        """
        Ensure repository tree path is always absolute
        """
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    # pylint: disable=redefined-builtin
    def __init__(self, path, name=None, create_missing=False, sorted=True, mode=None,
                 excluded=list, configuration=None):

        self.configuration = configuration if configuration is not None else Configuration(self)
        self.excluded = list(excluded) if isinstance(excluded, (tuple, list)) else []
        # pylint: disable=no-member
        self.excluded.extend(self.configuration.ignored_directories)

        super().__init__(path, create_missing, sorted, mode, self.excluded)

        self.repository_name = name if name is not None else self.name

    def initialize(self, *args, **kwargs):
        """
        Meta init method for trees. Executed after object is initialized
        """
        self.debug('initialize repository tree', args, kwargs)

    def debug(self, *args):
        """
        Pass debug messages to configuration
        """
        self.configuration.debug(*args)

    def error(self, *args):
        """
        Pass error messages to configuration
        """
        self.configuration.error(*args)

    def message(self, *args):
        """
        Pass messages to configuration
        """
        self.configuration.message(*args)
