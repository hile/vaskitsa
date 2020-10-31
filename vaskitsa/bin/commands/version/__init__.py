"""
CLI command 'vaskitsa version'
"""

from systematic_cli.command import Command

from .show import Show
from .update import Update


class Version(Command):
    """
    Command 'vaskitsa version'
    """
    name = 'version'
    subcommands = (
        Show,
        Update,
    )
