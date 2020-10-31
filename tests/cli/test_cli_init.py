"""
Test initializing vaskitsa CLI
"""

import sys

import pytest

from vaskitsa.bin.main import main


def test_cli_main_no_arguments():
    """
    Test running CLI main
    """
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1


def test_cli_main_help(monkeypatch):
    """
    Test running 'vaskitsa --help'
    """
    monkeypatch.setattr(sys, 'argv', ['vaskitsa', '--help'])
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
