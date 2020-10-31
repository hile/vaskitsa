"""
Common hook runnner classes
"""

from systematic_cli.task import CommandLineTask


class CLIHook(CommandLineTask):
    """
    Async task to run CLI command
    """
