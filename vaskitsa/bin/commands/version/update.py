"""
CLI command 'vaskitsa version update'
"""

from .base import VersionSubCommand


class Update(VersionSubCommand):
    """
    CLI command 'vaskitsa version update'
    """
    name = 'update'

    def run(self, args):
        print(args)
