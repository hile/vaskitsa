"""
Run git command
"""

import os

from pathlib import Path

from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run_command_lineoutput

from ..exceptions import GitError


def detect_git_repository_path(directory=None):
    """
    Detect git repository path by .git directory
    """
    if directory is not None:
        directory = Path(directory).expanduser()
    else:
        directory = Path(os.getcwd())

    directory = directory.absolute()
    while directory.parent != directory:
        if directory.joinpath('.git').is_dir():
            return directory
        directory = directory.parent
    return None


def run_git_command(*args, **kwargs):
    """
    Run a git command with specified arguments, returning stdout

    Current work directory for command can be specified with
    cwd=<path> in kwargs. If not specified, command runs in current
    work directory.
    """
    if 'cwd' in kwargs:
        cwd = kwargs.pop('cwd', os.getcwd())
    else:
        cwd = os.getcwd()

    cmd = ['git'] + list(args)
    try:
        stdout, stderr = run_command_lineoutput(*cmd, cwd=cwd)
    except CommandError as error:
        raise GitError(error) from error
    if stderr:
        print(stderr)
    return stdout
