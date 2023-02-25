"""
Hook to run flake8
"""
from cli_toolkit.base import Base

from ..hook import CLIHook

COMMAND = (
    'flake8',
)


class Flake8(CLIHook):
    """
    Run flake8 against repository
    """
    def __init__(self, parent: Base, **kwargs) -> None:
        super().__init__(parent, COMMAND, **kwargs)
