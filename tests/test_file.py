"""
Unit test cases for loading File objects
"""

import pytest

from pathlib_tree.tree import FilesystemError

from vaskitsa.python.file import PythonFile


def test_file_load_self_no_module():
    """
    Test loading itself as File without linking to module
    """
    testcase = PythonFile(__file__)
    assert testcase.module_root is False
    assert testcase.import_path is None
    assert testcase.is_index is False
    assert testcase.module is None
    assert testcase.relative_path is None
    assert testcase.relative_directory is None


def test_file_callbacks_no_module():
    """
    Test plain File callbacks raise errors
    """
    testcase = PythonFile(__file__)
    with pytest.raises(FilesystemError):
        testcase.debug('test debug method error')
    with pytest.raises(FilesystemError):
        testcase.error('test error method errors')
    with pytest.raises(FilesystemError):
        testcase.message('test message method error')
