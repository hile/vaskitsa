
from systematic_cli.command import Command


class AutodocGeneratorCommand(Command):
    """
    Common base class for python-autodoc-generator subcommands
    """

    @staticmethod
    def register_parser_arguments(parser):
        """
        Register common arguments for python-autodoc-generator subcommands
        """
        parser.add_argument(
            'repository',
            help='Python repository to scan'
        )
        return parser

    def parse_args(self, args):
        """
        Parse arguments for autodoc generators
        """
        return args
