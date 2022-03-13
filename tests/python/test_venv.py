"""
Unit tests for vaskitsa.python.venv module
"""

from pathlib import Path

import pytest

from packaging.version import Version

from vaskitsa.exceptions import PythonSetupError
from vaskitsa.python.venv import VirtualEnv

DEFAULT_PYTHON_COMMAND = 'python3'
INVALID_PYTHON_COMMAND = 'python3.123'


def test_venv_virtualenv_attributes(tmpdir):
    """
    Test basic attributes of a VirtualEnv object
    """
    obj = VirtualEnv(tmpdir, DEFAULT_PYTHON_COMMAND)
    assert isinstance(obj.__repr__(), str)


def test_venv_virtualenv_python_version_ok(tmpdir):
    """
    Test getting version of VirtualEnv object python interpreter
    """
    obj = VirtualEnv(tmpdir, DEFAULT_PYTHON_COMMAND)
    assert isinstance(obj.python_version, Version)


def test_venv_virtualenv_python_version_error(tmpdir):
    """
    Test getting version of VirtualEnv object python interpreter with invalid command
    """
    with pytest.raises(PythonSetupError):
        VirtualEnv(tmpdir, INVALID_PYTHON_COMMAND)


def test_venv_virtualenv_auto_create(tmpdir):
    """
    Test VirtualEnv object initializes the directory when it's missing
    """
    directory = Path(tmpdir.strpath, 'venv')
    assert not directory.exists()
    obj = VirtualEnv(directory, DEFAULT_PYTHON_COMMAND)
    assert obj.path == directory
    assert directory.exists()
