"""
Visual studio code workspace configuration folder list
"""

from pathlib import Path

from cli_toolkit.configuration import ConfigurationList, ConfigurationSection


class WorkspaceFolder(ConfigurationSection):
    """
    Single folder in workspace folder configuration
    """
    def __init__(self, data=dict, parent=None, debug_enabled=False, silent=False):
        self.name = ''
        self.path = None
        self.__relative__ = None
        super().__init__(data, parent, debug_enabled, silent)

    def __repr__(self):
        # pylint: disable=no-member
        return self.name

    def __str__(self):
        return str(self.path)

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.absolute() == other
        return self.absolute() == other.absolute()

    def __ne__(self, other):
        if isinstance(other, Path):
            return self.absolute() != other
        return self.absolute() != other.absolute()

    def __lt__(self, other):
        if isinstance(other, Path):
            return self.absolute() < other
        return self.absolute() < other.absolute()

    def __gt__(self, other):
        if isinstance(other, Path):
            return self.absolute() > other
        return self.absolute() > other.absolute()

    def __le__(self, other):
        if isinstance(other, Path):
            return self.absolute() <= other
        return self.absolute() <= other.absolute()

    def __ge__(self, other):
        if isinstance(other, Path):
            return self.absolute() >= other
        return self.absolute() >= other.absolute()

    @property
    def workspace_config(self):
        """
        Path to workspace file where the folder is linked to. Returns pathlib.Path
        object representing path to the .code-workspace file
        """
        return self.__parent__.__parent__.__path__

    def absolute(self):
        """
        Return absolute path to workspace folder
        """
        if self.__relative__:
            path = self.workspace_config.parent.joinpath(self.path)
        path = Path(self.path)
        return path.resolve()

    def validate_path(self, value):
        """
        Validate workspace folder path
        """
        path = Path(value)
        if not path.is_absolute():
            self.__relative__ = True
            abspath = self.workspace_config.parent.joinpath(path)
        else:
            abspath = path
            self.__relative__ = False
        if not abspath.is_dir():
            raise ValueError(f'No such directory: {abspath}')
        return path

    def as_dict(self):
        """
        Return folder configuration as dictionary for saving
        """
        return {
            'name': self.name,
            'path': str(self.path),
        }


class WorkspaceFolderList(ConfigurationList):
    """
    List of folders in visual studio code .code-workspace configuration file
    """
    __name__ = 'folders'
    __dict_loader_class__ = WorkspaceFolder

    def as_dict(self):
        """
        Return list of folders as dictionary
        """
        return [folder.as_dict() for folder in self]

    def add_folder(self, path, name=None):
        """
        Add a folder to workspace

        If name is not spacified user path directory name part as name
        """
        resolved_path = Path(path).resolve()
        if not resolved_path.is_dir():
            raise ValueError(f'No such directory: {resolved_path}')

        if name is None:
            name = resolved_path.name

        data = {
            'name': name,
            'path': str(resolved_path)
        }
        folder = WorkspaceFolder(
            data,
            parent=self,
            debug_enabled=self.__debug_enabled__,
            silent=self.__silent__
        )
        if folder in self.__values__:
            raise ValueError(f'Duplicate folder: {folder}')

        self.__values__.append(folder)
