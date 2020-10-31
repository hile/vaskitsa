"""
Test CLI command 'list' against current repository
"""

import sys
from tempfile import mkdtemp
from unittest.mock import patch

import pytest

from vaskitsa.bin.main import main
from ..constants import REPO_ROOT_PATH


def test_cli_generate_self_default():
    """
    Test running CLI 'generate' command against current repository
    """
    target = mkdtemp()
    testargs = [
        sys.argv[0],
        'documentation',
        'generate',
        f'--output-directory={target}',
        str(REPO_ROOT_PATH)
    ]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exit_status:
            main()
        assert exit_status.value.code == 0
