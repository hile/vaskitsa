"""
Utilities for vaskitsa
"""

import keyword
import os

from pathlib import Path

import inflection


def is_python_module_directory(directory):
    """
    Checks if directory is python module directory
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return False

    # Detect if directory name is valid python identifier
    if not str(directory.name).isidentifier():
        return False

    # Detect __init__.py file
    if directory.joinpath('__init__.py').exists():
        return True

    return False


def detect_package_module_name(repository):
    """
    Set main module name using specified value or if not specified, deduce from
    repository folder name
    """
    module_name = inflection.underscore(repository.name)
    if '-' in module_name:
        module_name = module_name.replace('-', '_')
    return module_name


def detect_python_package_path(directory=None):
    """
    Directory package root from python code directory
    """
    if directory is not None:
        directory = Path(directory)
    else:
        directory = Path(os.getcwd())

    directory = directory.absolute()
    if not is_python_module_directory(directory):
        return None

    while directory.parent != directory:
        if directory.joinpath('setup.py').exists():
            return directory
        if not is_python_module_directory(directory):
            return directory
        directory = directory.parent

    return None


def validate_module_name(value, convert_lowercase=False, allow_keywords=False):
    """
    Validate a string to be used as python package or module name
    """
    if not isinstance(value, str):
        raise NameError(f'Module must be string: {value}')

    if not value.isidentifier():
        raise NameError(f'Name is not valid python identifier: {value}')

    if not allow_keywords and keyword.iskeyword(value):
        raise NameError(f'Name is a python keyword: {value}')

    lowercase = value.lower()
    if not convert_lowercase and lowercase != value:
        raise NameError(f'Name is not a lowercase string: {value}')

    if convert_lowercase:
        value = lowercase

    return value


def get_module_path_components(value, convert_lowercase=False, allow_keywords=False):
    """
    Validate and return module path components

    Path can contain . and / letters but not mixed together

    Returns list of validated module names
    """
    separator = None
    if '/' in value:
        separator = '/'
    if '.' in value:
        if separator is not None:
            raise NameError(f'Path contains both . and /: {value}')
        separator = '.'

    if separator:
        return [
            validate_module_name(name, convert_lowercase, allow_keywords)
            for name in value.split(separator)
        ]
    return [validate_module_name(value, convert_lowercase, allow_keywords)]
