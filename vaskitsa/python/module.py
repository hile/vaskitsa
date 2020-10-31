"""
Base class for python module document generator

A module is part of a package and contains python files
"""

import os

from pathlib import Path

from systematic_files.exceptions import FilesystemError
from systematic_files.tree import Tree

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
    def __init__(self, path, repository=None, group=None,
                 create_missing=False, sorted=True, mode=None):
        super().__init__(path, create_missing=False, sorted=sorted, mode=mode)
        self.repository = repository
        self.group = group
        if not self.is_dir() and create_missing:
            self.mkdir(parents=True)
        self.files = []
        self.load_files()

    @classmethod
    def create_module(cls, path, repository=None, group=MODULE_DEFAULT_GROUP):
        """
        Create module to repository

        Initializes __init__.py as side effect
        """
        if not isinstance(path, (Path, str)):
            raise ValueError('create_module() path must be str or Path instance')

        if repository and isinstance(path, str):
            path = repository.joinpath(path)

        try:
            path.relative_to(repository)
        except ValueError as error:
            raise ValueError(f'create_module() path is not not under {repository}') from error

        if path.exists() and not path.is_dir():
            raise ValueError(f'create_module() path is not directory: {path}')

        module = cls(path, repository=repository, group=group, create_missing=True)
        module.create_file('__init__')
        return module

    @property
    def parent(self):
        """
        Return module parent as Module
        """
        if not self.repository:
            return None
        item = self.repository.joinpath(super().parent)
        for module in self.repository.python_modules:
            if item == module:
                return module
        return self.repository

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
        if self.repository:
            return Path(self.relative_to(self.repository))
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
        Pass debug message to repository
        """
        if self.repository:
            return self.repository.debug(*args)
        raise FilesystemError('Module not linked to a package')

    def error(self, *args):
        """
        Pass error message to repository
        """
        if self.repository:
            return self.repository.error(*args)
        raise FilesystemError('Module not linked to a package')

    def message(self, *args):
        """
        Pass messages to repository
        """
        if self.repository:
            return self.repository.message(*args)
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
