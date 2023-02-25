"""
CLI subcommand 'vaskitsa documentation'
"""
from cli_toolkit.command import Command

from .generate import Generate
from .list import List


class Documentation(Command):
    """
    Vaskitsa 'documentation' subcommand
    """
    name = 'documentation'
    subcommands = (
        Generate,
        List
    )
