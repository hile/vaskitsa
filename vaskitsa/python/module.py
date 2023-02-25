"""
Base class for python module document generator

A module is part of a package and contains python files
"""
import os

from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from pathlib_tree.exceptions import FilesystemError
from pathlib_tree.tree import Tree

from .constants import MODULE_DEFAULT_GROUP
from .file import PythonFile

if TYPE_CHECKING:
    from .package import Package


class PythonModule(Tree):
    """
    Documentation generator for module in a package
    """
    path: Path
    package: Optional['Package']
    group: Optional[str]
    files: List[PythonFile]

    python_file_class = PythonFile

    def __repr__(self):
        return str(self.relative_directory)

    # pylint: disable=redefined-builtin
    def __init__(self,
                 path: Path,
                 package: Optional['Package'] = None,
                 group: Optional[str] = None,
                 create_missing: bool = False,
                 sorted: bool = True,
                 mode: str = None,
                 excluded: List[str] = None):
        super().__init__(path, create_missing=False, sorted=sorted, mode=mode, excluded=excluded)
        self.package = package
        self.group = group
        if not self.is_dir() and create_missing:
            self.mkdir(parents=True)
        self.files = self.load_files()

    @classmethod
    def create_module(
            cls,
            path: Union[str, Path],
            package: Optional['Package'] = None,
            group: str = MODULE_DEFAULT_GROUP) -> 'PythonModule':
        """
        Create module to package

        Initializes __init__.py as side effect
        """
        if not isinstance(path, (Path, str)):
            raise ValueError('create_module() path must be str or Path instance')

        if package and isinstance(path, str):
            path = package.joinpath(path)

        try:
            path.relative_to(package)
        except ValueError as error:
            raise ValueError(f'create_module() path is not not under {package}') from error

        if path.exists() and not path.is_dir():
            raise ValueError(f'create_module() path is not directory: {path}')

        module = cls(path, package=package, group=group, create_missing=True)
        module.create_file('__init__')
        return module

    @property
    def parent(self) -> Optional[Union['Package', 'PythonModule']]:
        """
        Return module parent as Module
        """
        if not self.package:
            return None
        item = self.package.joinpath(super().parent)
        for module in self.package.python_modules:
            if item == module:
                return module
        return self.package

    @property
    def index(self) -> Optional[PythonFile]:
        """
        Return package index file __init__.py
        """
        for item in self.files:
            if item.module == self and item.path.name == '__init__.py':
                return item
        return None

    @property
    def relative_directory(self) -> Optional[Path]:
        """
        Return relative parent directory to package root
        """
        if self.package:
            return Path(self.relative_to(self.package))
        return None

    @property
    def import_path(self) -> Optional[str]:
        """
        Return file import path
        """
        path = self.relative_directory
        if path is not None:
            return str(path).replace(os.sep, '.')
        return None

    def debug(self, *args) -> None:
        """
        Pass debug message to parent
        """
        if self.package:
            return self.package.debug(*args)
        raise FilesystemError('Module not linked to a package')

    def error(self, *args) -> None:
        """
        Pass error message to parent
        """
        if self.package:
            return self.package.error(*args)
        raise FilesystemError('Module not linked to a package')

    def message(self, *args) -> None:
        """
        Pass messages to parent
        """
        if self.package:
            return self.package.message(*args)
        raise FilesystemError('Module not linked to a package')

    def load_files(self) -> List[PythonFile]:
        """
        Load python files in module
        """
        files = []
        for child in self:
            if child.parent == self and child.suffix == '.py' and child.is_file():
                files.append(self.python_file_class(child, module=self))
        return files

    def create_file(self, name: str) -> PythonFile:
        """
        Create python file to module
        """
        path = self.joinpath(name).with_suffix('.py')
        python_file = PythonFile(path, module=self, create_missing=True)
        self.load_files()
        return python_file
