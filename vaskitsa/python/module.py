"""
Base class for python module document generator

A module is part of a package and contains python files
"""

import os

from pathlib import Path

from pathlib_tree.exceptions import FilesystemError
from pathlib_tree.tree import Tree

from .constants import MODULE_DEFAULT_GROUP
from .file import PythonFile


class PythonModule(Tree):
    """
    Documentation generator for module in a package
    """
    python_file_class = PythonFile

    def __repr__(self):
        return str(self.relative_directory)

    # pylint: disable=redefined-builtin
    def __init__(self, path, package=None, group=None, create_missing=False,
                 sorted=True, mode=None, excluded=None):
        super().__init__(path, create_missing=False, sorted=sorted, mode=mode, excluded=excluded)
        self.package = package
        self.group = group
        if not self.is_dir() and create_missing:
            self.mkdir(parents=True)
        self.files = []
        self.load_files()

    @classmethod
    def create_module(cls, path, package=None, group=MODULE_DEFAULT_GROUP):
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
    def parent(self):
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
    def index(self):
        """
        Return package index file __init__.py
        """
        for item in self.files:
            if item.module == self and item.path.name == '__init__.py':
                return item
        return None

    @property
    def relative_directory(self):
        """
        Return relative parent directory to package root
        """
        if self.package:
            return Path(self.relative_to(self.package))
        return None

    @property
    def import_path(self):
        """
        Return file import path
        """
        path = self.relative_directory
        if path is not None:
            return str(path).replace(os.sep, '.')
        return None

    def debug(self, *args):
        """
        Pass debug message to parent
        """
        if self.package:
            return self.package.debug(*args)
        raise FilesystemError('Module not linked to a package')

    def error(self, *args):
        """
        Pass error message to parent
        """
        if self.package:
            return self.package.error(*args)
        raise FilesystemError('Module not linked to a package')

    def message(self, *args):
        """
        Pass messages to parent
        """
        if self.package:
            return self.package.message(*args)
        raise FilesystemError('Module not linked to a package')

    def load_files(self):
        """
        Load python files in module
        """
        files = []
        for child in self:
            if child.parent == self and child.suffix == '.py' and child.is_file():
                files.append(self.python_file_class(child, module=self))
        self.files = files

    def create_file(self, name):
        """
        Create python file to module
        """
        path = self.joinpath(name).with_suffix('.py')
        python_file = PythonFile(path, module=self, create_missing=True)
        self.load_files()
        return python_file
