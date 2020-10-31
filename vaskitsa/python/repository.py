"""
Python code repository with packages
"""

import os

from ..tree import RepositoryTree

from .constants import (
    MODULE_DEFAULT_GROUP,
    REPOSITORY_ROOT_IGNORED_FILES,
    TEST_MODULE_DEFAULT_GROUP
)
from .file import PythonFile
from .module import PythonModule
from .version import PythonRepositoryVersion
from .setup import SetupConfig
from .utils import detect_repository_module_name, get_module_path_components


class Repository(RepositoryTree):
    """
    Repository of code
    """
    python_module_class = PythonModule

    # pylint: disable=attribute-defined-outside-init
    def initialize(self, *args, **kwargs):
        """
        Initialize python tree
        """
        super().initialize(*args, **kwargs)
        self.__module_index__ = {}
        self.__python_modules__ = None
        self.__python_test_modules__ = None
        self.__setup__ = None
        self.module_name = detect_repository_module_name(self)

    @property
    def setup(self):
        """
        Lazy loading of setup.cfg parser
        """
        if self.__setup__ is None:
            self.__setup__ = SetupConfig(self)
        return self.__setup__

    @property
    def python_package_version(self):
        """
        Try to read version from main module index file
        """
        return PythonRepositoryVersion(self)

    @property
    def python_module_paths(self):
        """
        Find valid module paths in directory
        """
        modules = []
        if self.is_dir():
            for item in self.filter('*.py'):
                if item.parent == self and item.name in REPOSITORY_ROOT_IGNORED_FILES:
                    continue
                if item.parent not in modules:
                    modules.append(item.parent)
        return modules

    @property
    def python_modules(self):
        """
        Get python modules
        """
        if self.__python_modules__ is None:
            self.__python_modules__, self.__python_test_modules__ = self.detect_python_modules()
        return self.__python_modules__

    @property
    def python_test_modules(self):
        """
        Get python test modules
        """
        if self.__python_test_modules__ is None:
            self.__python_modules__, self.__python_test_modules__ = self.detect_python_modules()
        return self.__python_test_modules__

    @property
    def python_files(self):
        """
        Return files in all python packages
        """
        files = []
        for module in self.python_modules:
            files.extend(module.files)
        return files

    def detect_python_modules(self):
        """
        Detect python packages in repository
        """
        modules = []
        test_modules = []
        for path in self.python_module_paths:
            name = path.name
            module = None

            parents = list(
                reversed([
                    parent.name
                    for parent in path.relative_to(self).parents
                    if parent.name != ''
                ])
            )
            # pylint: disable=no-member
            test_directory_parent = set(parents).intersection(
                set(self.configuration.test_directories)
            )
            if test_directory_parent or name in self.configuration.test_directories:
                module = self.python_module_class(path, repository=self, group=TEST_MODULE_DEFAULT_GROUP)
                if path not in test_modules:
                    test_modules.append(module)
            else:
                module = self.python_module_class(path, repository=self)
                if path not in modules:
                    modules.append(module)

            module_relative_path = str(module.relative_directory)
            if module_relative_path not in self.__module_index__:
                self.__module_index__[module_relative_path] = module

        return modules, test_modules

    def get_python_module(self, name):
        """
        Get python module by name
        """
        relative_path = str(self.joinpath(name).relative_to(self))
        try:
            return self.__module_index__[relative_path]
        except KeyError:
            return None

    def create_python_module(self, name, test_module=False, group=MODULE_DEFAULT_GROUP):
        """
        Create a new python module to repository
        """
        module_path = get_module_path_components(name)
        group = TEST_MODULE_DEFAULT_GROUP if test_module else MODULE_DEFAULT_GROUP
        for index in range(0, len(module_path)):
            path = str(self.joinpath(*module_path[:index + 1]).relative_to(self))
            module = self.get_python_module(name)
            if module is None:
                module = self.python_module_class.create_module(
                    path,
                    repository=self,
                    group=group
                )
        return module

    def create_python_file(self, path, test_module=False, group=MODULE_DEFAULT_GROUP):
        """
        Create new python file to specified path in repository

        As a side effect creates module path as required
        """
        python_file_path = get_module_path_components(path)
        if len(python_file_path) > 1:
            module_path = str(os.sep.join(python_file_path[:-1]))
            filename = python_file_path[-1]
        else:
            module_path = None
            filename = python_file_path[0]

        if module_path is not None:
            module = self.create_python_module(module_path, test_module=test_module, group=group)
            return module.create_file(filename)
        path = self.joinpath(filename).with_suffix('.py')
        return PythonFile(path, module=None, create_missing=True)
