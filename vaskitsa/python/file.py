"""
Base class for python file
"""
import os

from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING

from pathlib_tree.exceptions import FilesystemError

if TYPE_CHECKING:
    from .module import PythonModule

EMPTY_FILE = '''"""
Automatically generated file
"""
'''


class PythonFile:
    """
    Python code file
    """
    module: Optional['PythonModule']
    path: Path
    module_root: bool

    def __init__(self,
                 path: Union[str, Path],
                 module: Optional['PythonModule'] = None,
                 create_missing: bool = False) -> None:
        self.module = module
        self.path = Path(path)
        if not self.path.is_file() and create_missing:
            with open(self.path, 'w', encoding='utf-8') as filedescriptor:
                filedescriptor.write(EMPTY_FILE)
        self.module_root = self.path.name == '__init__.py'

    def __repr__(self) -> str:
        if self.import_path is not None:
            if self.path.name == '__init__.py':
                return self.path.name
            return self.import_path
        return str(self.path)

    @property
    def relative_path(self) -> Optional[Path]:
        """
        Return path relative to package
        """
        if self.module and self.module.package:
            return self.path.relative_to(self.module.package)
        return None

    @property
    def relative_directory(self) -> Optional[Path]:
        """
        Return parent directory relativve to package root
        """
        if self.relative_path:
            return self.relative_path.parent
        return None

    @property
    def import_path(self) -> str:
        """
        Return file import path
        """
        path = self.relative_path
        if path is not None:
            if path.name == '__init__.py':
                path = path.with_suffix('').parent
            else:
                path = path.with_suffix('')
            return str(path).replace(os.sep, '.')
        return None

    @property
    def is_index(self) -> bool:
        """
        Check if this is file is module root index (__init__.py)
        """
        return self.path.name == '__init__.py'

    @property
    def is_module_index(self) -> bool:
        """
        Check if this is file is modle root index (__init__)
        """
        return self.module and self.module.parent is None and self.path.name == '__init__.py'

    @property
    def name(self) -> str:
        """
        Return name of file without extension
        """
        return self.path.stem

    def debug(self, *args) -> None:
        """
        Pass debug message to parent
        """
        if self.module:
            return self.module.debug(*args)
        raise FilesystemError('File not linked to a module')

    def error(self, *args) -> None:
        """
        Pass error message to parent
        """
        if self.module:
            return self.module.error(*args)
        raise FilesystemError('File not linked to a module')

    def message(self, *args) -> None:
        """
        Pass messages to parent
        """
        if self.module:
            return self.module.message(*args)
        raise FilesystemError('File not linked to a module')
