"""
CLI subcommands for python-autodoc-generator
"""

from systematic_cli.command import Command

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
