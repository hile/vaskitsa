"""
Base class for python module document generator

A module is part of a package and contains python files
"""
from pathlib import Path
from typing import Union, TYPE_CHECKING

from ..python.module import PythonModule

from .base import TemplateGenerator
from .file import FileDocumentGenerator

if TYPE_CHECKING:
    from vaskitsa.templates.template import TemplateRenderer


class ModuleDocumentGenerator(PythonModule, TemplateGenerator):
    """
    Documentation generator for module in a package
    """
    python_file_class = FileDocumentGenerator
    """Class for loading self.files"""
    template_name = None
    """Template to render for module document"""

    @property
    def template_loader(self) -> type['TemplateRenderer']:
        """
        Template loader class from package
        """
        return self.package.template_loader

    def get_output_filename(self, directory: Union[str, Path]) -> Path:
        """
        Get output filename for rendered data
        """
        raise NotImplementedError('get_output_filename() must be implemented in child class')

    def generate_module_docs(self, directory: Union[str, Path]) -> None:
        """
        Generate documentation for module

        This must be implemented in child class
        """
        for item in self.files:
            item.generate(directory)

        # Only create index file if there is no __init__.py
        if not self.index:
            super().generate(directory)
