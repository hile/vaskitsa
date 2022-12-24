
from cli_toolkit.command import Command


class AutodocGeneratorCommand(Command):
    """
    Common base class for python-autodoc-generator subcommands
    """

    def register_parser_arguments(self, parser):
        """
        Register common arguments for python-autodoc-generator subcommands
        """
        parser.add_argument(
            'repository',
            help='Python repository to scan'
        )
        return parser

    def parse_args(self, args=None, namespace=None):
        """
        Parse arguments for autodoc generators
        """
        return args
