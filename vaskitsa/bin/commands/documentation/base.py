"""
CLI subcommand base classes for 'vaskitsa documentation' subcommands
"""
from argparse import ArgumentParser, Namespace
from cli_toolkit.command import Command


class AutodocGeneratorCommand(Command):
    """
    Common base class for python-autodoc-generator subcommands
    """

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register common arguments for python-autodoc-generator subcommands
        """
        parser.add_argument(
            'repository',
            help='Python repository to scan'
        )
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse arguments for autodoc generators
        """
        return args
