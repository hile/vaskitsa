"""
Python code repository documentation with modules
"""

from pathlib import Path

from ..templates.template import TemplateRenderer
from ..python.package import Package

from .base import TemplateGenerator
from .configuration import DEFAULT_DOCUMENTS_PATH
from .module import ModuleDocumentGenerator


class PackageDocumentGenerator(Package, TemplateGenerator):
    """
    Package document generator
    """
    python_module_class = ModuleDocumentGenerator
    """Package documentation generator class"""

    template_loader = TemplateRenderer
    """Class for jinja2 template rendering"""

    @property
    def template_configuration(self):
        """
        Return template loader specific configuration
        """
        name = getattr(self.template_loader, 'name', None)
        if name:
            return getattr(self.configuration, name)
        return None

    @property
    def default_output_directory(self):
        """
        Return default documentation output directory relative to repository root
        """
        configuration = self.template_configuration
        if configuration and getattr(configuration, 'document_path', None):
            return Path(self, configuration.document_path)
        return Path(self).joinpath(DEFAULT_DOCUMENTS_PATH)

    def get_output_filename(self, directory):
        """
        Return None, repository level indexes are created by modules
        """
        raise NotImplementedError(
            'get_output_filename() must be implemented in child class'
        )

    def generate(self, directory=None):
        """
        Generate repository documentation
        """
        if directory is None:
            self.debug('set output directory to', self.default_output_directory)
            directory = self.default_output_directory

        print(f'generate repository documentation {self} {type(self)}')
        for module in self.python_modules:
            print(f'generate python module docs for {module} to {directory}')
            module.generate_module_docs(directory)
        super().generate(directory)
