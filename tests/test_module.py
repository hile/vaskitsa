"""
Unit test cases for loading Module objects
"""

from pathlib import Path

import pytest

from pathlib_tree.tree import FilesystemError

from vaskitsa.python.module import PythonModule


def test_module_load_self_no_module():
    """
    Test loading itself as File without linking to module
    """
    testcase = PythonModule(Path(__file__).parent)
    assert testcase.repository is None
    assert testcase.relative_directory is None


def test_module_callbacks_no_module():
    """
    Test plain File callbacks raise errors
    """
    testcase = PythonModule(Path(__file__).parent)
    with pytest.raises(FilesystemError):
        testcase.debug('test debug method error')
    with pytest.raises(FilesystemError):
        testcase.error('test error method errors')
    with pytest.raises(FilesystemError):
        testcase.message('test message method error')
