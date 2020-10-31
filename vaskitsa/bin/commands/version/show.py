"""
CLI command 'vaskitsa version show'
"""


from .base import VersionSubCommand


class Show(VersionSubCommand):
    """
    CLI command 'vaskitsa version show'
    """
    name = 'show'

    def run(self, args):
        print(args)
