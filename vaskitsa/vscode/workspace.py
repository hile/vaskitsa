"""
Visual Studio Code workspaces configuration files
"""

from pathlib import Path


from cli_toolkit.configuration import JsonConfiguration
from .folders import WorkspaceFolderList
from .settings import Settings


class Workspace(JsonConfiguration):
    """
    Visual studio workspace configuration file parsers
    """
    __section_loaders__ = (
        Settings,
    )
    __list_loader_class__ = WorkspaceFolderList

    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False, **loader_args):
        path = Path(path).with_suffix('.code-workspace')
        super().__init__(path, parent, debug_enabled, silent, **loader_args)

    def as_dict(self):
        """
        Return workspace settings as dictionary
        """
        # pylint: disable=no-member
        return {
            'folders': self.folders.as_dict(),
            'settings': self.settings.as_dict(),
        }
