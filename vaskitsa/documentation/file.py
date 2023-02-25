"""
Base class for python file document generator
"""
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING

from ..python.file import PythonFile

from .base import TemplateGenerator


if TYPE_CHECKING:
    from vaskitsa.templates.template import TemplateRenderer


class FileDocumentGenerator(PythonFile, TemplateGenerator):
    """
    Documentation generator for single python file
    """
    template_name: Optional[str] = None
    """Template to render for file documentation"""

    @property
    def template_loader(self) -> type['TemplateRenderer']:
        """
        Template loader class from package
        """
        return self.module.package.template_loader

    def get_output_filename(self, directory: Union[str, Path]) -> Path:
        """
        Get output filename for rendered data
        """
        raise NotImplementedError(
            'get_output_filename() must be implemented in child class'
        )
