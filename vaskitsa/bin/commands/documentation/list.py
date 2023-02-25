"""
CLI subcommand 'vaskitsa documentation list'
"""
from vaskitsa.documentation.package import PackageDocumentGenerator

from .base import AutodocGeneratorCommand


class List(AutodocGeneratorCommand):
    """
    List files or modules in python package
    """
    name = 'list'
    usage = 'vaskitsa documentation list <args>'

    def register_parser_arguments(self, parser):
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '-o', '--output-mode',
            choices=('files', 'modules'),
            default='files',
            help='Output mode'
        )
        return parser

    def list_package_files(self, package):
        """
        List files in package with relative path
        """
        for item in package.python_files:
            self.message(item.relative_path)

    def list_package_modules(self, package):
        """
        List modules in package
        """
        for item in package.python_modules:
            self.message(item.import_path)

    def run(self, args):
        """
        List files to be used in documentation auto generation
        """
        package = PackageDocumentGenerator(args.repository)
        if args.output_mode == 'files':
            self.list_package_files(package)
        if args.output_mode == 'modules':
            self.list_package_modules(package)
