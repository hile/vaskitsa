"""
Unit tests for vaskitsa.python module, testing vaskitsa.python.package, vaskitsa.python.module and
vaskitsa.python.file
"""

from vaskitsa.git.repository import GitRepository
from vaskitsa.python.module import PythonModule
from vaskitsa.python.package import Package

from ..constants import MOCK_DATA

MOCK_PACKAGE_NAME = 'mock-python-module'
MOCK_MISSING_MODULE_NAME = 'mock_python_module/missing_module'
MOCK_TEST_MODULE_NAME = 'mock_python_module/demo'
MOCK_PACKAGE_PATH = MOCK_DATA.joinpath(MOCK_PACKAGE_NAME)


def validate_module(package, module):
    """
    Validate python module object
    """
    assert isinstance(module, PythonModule)
    assert module.package == package


def test_python_package_attributes():
    """
    Test attributes of a python package object with mocked data
    """
    package = Package(MOCK_PACKAGE_PATH)
    assert isinstance(package.__repr__(), str)
    assert isinstance(package.git_repository, GitRepository)


def test_python_package_get_module_found():
    """
    Test fetching python module by name from package
    """
    package = Package(MOCK_PACKAGE_PATH)
    module = package.get_python_module(MOCK_TEST_MODULE_NAME)
    validate_module(package, module)


def test_python_package_get_module_not_found():
    """
    Test fetching python module by name from package
    """
    package = Package(MOCK_PACKAGE_PATH)
    module = package.get_python_module(MOCK_MISSING_MODULE_NAME)
    assert module is None
