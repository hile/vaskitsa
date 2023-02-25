"""
Hook to run pylint
"""
from cli_toolkit.base import Base
from ..hook import CLIHook

COMMAND = (
    'pylint',
    '--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'
)


class Pylint(CLIHook):
    """
    Run pylint
    """
    def __init__(self, parent: Base, **kwargs):
        super().__init__(parent, COMMAND, **kwargs)
