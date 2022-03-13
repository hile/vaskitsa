"""
Unit tests for vaskitsa.python.dependencies module
"""

from pathlib import Path

from vaskitsa.python.dependencies import DependenciesProcessor


def test_python_dependencies_processor_attributes():
    """
    Test attributes of DependenciesProcessor object
    """
    obj = DependenciesProcessor()
    for attr in ('__upload_virtulenv__', '__virtulenv__'):
        assert getattr(obj, attr) is None
    assert isinstance(obj.__repr__(), str)
    for attr in ('cache_directory', 'packages_directory'):
        assert isinstance(getattr(obj, attr), Path)
