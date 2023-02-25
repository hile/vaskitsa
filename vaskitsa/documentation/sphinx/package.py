"""
Package in python documentation tree sphinx documentation
"""
from pathlib import Path
from typing import Union

from ..renderers.sphinx import SphinxTemplateRenderer
from ..package import PackageDocumentGenerator

from .module import AutodocModuleGenerator


class AutodocPackageGenerator(PackageDocumentGenerator):
    """
    Autodoc generator for python repository
    """
    python_module_class = AutodocModuleGenerator
    """Class for loading modules"""

    template_loader = SphinxTemplateRenderer
    """Class for jinja2 template rendering"""

    def __repr__(self) -> str:
        return f'sphinx {super().__str__()}'

    @property
    def template_directory(self) -> Path:
        """
        Return directory for templates from configuration

        By default returns None
        """
        return self.template_configuration.template_directory

    @property
    def index_max_depth(self) -> int:
        """
        Return sphinx repository documentation root TOC index max depth
        """
        return self.template_configuration.repository_index_max_depth

    @property
    def template_name(self) -> str:
        """
        Return template name for module documentation
        """
        return self.template_configuration.templates.repository

    def get_output_filename(self, directory: Union[str, Path]) -> Path:
        """
        Return output filename for generated documentation index file
        """
        return Path(directory, 'index.rst')
