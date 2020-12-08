
from cli_toolkit.script import Script

from .commands.documentation import Documentation
from .commands.python import Python
from .commands.version import Version

HELP = """vaskitsa

Utility to initialize and manage python modules
"""


class Vaskitsa(Script):
    """
    CLI script 'vaskitsa'
    """
    help = HELP
    subcommands = (
        Documentation,
        Python,
        Version
    )


def main():
    """
    Main entrypoint for vaskitsa CLI
    """
    Vaskitsa().run()
