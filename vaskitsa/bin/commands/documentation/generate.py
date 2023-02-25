"""
CLI subcommand 'vaskitsa documentation generate'
"""
from vaskitsa.documentation.loader import (
    get_processor,
    DEFAULT_PROCESSOR,
    PROCESSOR_TYPES,
)
from .base import AutodocGeneratorCommand


class Generate(AutodocGeneratorCommand):
    """
    Generate python module documentation
    """
    name = 'generate'
    usage = 'python-autodoc-generator generate <args>'

    def register_parser_arguments(self, parser):
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '-t', '--type',
            choices=PROCESSOR_TYPES,
            default=DEFAULT_PROCESSOR,
            help='Type of generated documentation'
        )
        parser.add_argument(
            '-o', '--output-directory',
            help='Target directory for generated documentation'
        )
        return parser

    def run(self, args):
        """
        Generate python module documentation
        """
        processor = get_processor(
            args.type,
            args.repository,
        )
        processor.generate(args.output_directory)
