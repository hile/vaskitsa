"""
Test CLI command 'list' against current repository
"""

import sys
from unittest.mock import patch

import pytest

from vaskitsa.bin.main import main
from ..constants import REPO_ROOT_PATH


def test_cli_list_self_default():
    """
    Test running CLI 'list' command against current repository
    """
    testargs = [
        sys.argv[0],
        'documentation',
        'list',
        str(REPO_ROOT_PATH)
    ]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exit_status:
            main()
        assert exit_status.value.code == 0


def test_cli_list_self_files():
    """
    Test running CLI 'list' command against current repository
    """
    testargs = [
        sys.argv[0],
        'documentation',
        'list',
        '--output-mode=files',
        str(REPO_ROOT_PATH)
    ]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exit_status:
            main()
        assert exit_status.value.code == 0


def test_cli_list_self_modules():
    """
    Test running CLI 'list' command against current repository
    """
    testargs = [
        sys.argv[0],
        'documentation',
        'list',
        '--output-mode=modules',
        str(REPO_ROOT_PATH)
    ]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exit_status:
            main()
        assert exit_status.value.code == 0
