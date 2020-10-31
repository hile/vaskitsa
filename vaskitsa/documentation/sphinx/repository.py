
from pathlib import Path

from ..renderers.sphinx import SphinxTemplateRenderer
from ..repository import RepositoryDocumentGenerator

from .module import AutodocModuleGenerator


class AutodocRepositoryGenerator(RepositoryDocumentGenerator):
    """
    Autodoc generator for python repository
    """
    python_module_class = AutodocModuleGenerator
    """Class for loading modules"""

    template_loader = SphinxTemplateRenderer
    """Class for jinja2 template rendering"""

    def __repr__(self):
        return f'sphinx {super().__str__()}'

    @property
    def template_directory(self):
        """
        Return directory for templates from configuration

        By default returns None
        """
        return self.template_configuration.template_directory

    @property
    def index_max_depth(self):
        """
        Return sphinx repository documentation root TOC index max depth
        """
        return self.template_configuration.repository_index_max_depth

    @property
    def template_name(self):
        """
        Return template name for module documentation
        """
        return self.template_configuration.templates.repository

    @staticmethod
    def get_output_filename(directory):
        """
        Return output filename for generated documentation index file
        """
        return Path(directory, 'index.rst')
