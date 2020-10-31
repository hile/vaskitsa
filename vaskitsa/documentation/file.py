"""
Base class for python file document generator
"""

from ..python.file import PythonFile

from .base import TemplateGenerator


class FileDocumentGenerator(PythonFile, TemplateGenerator):
    """
    Documentation generator for single python file
    """
    template_name = None
    """Template to render for file documentation"""

    @property
    def template_loader(self):
        """
        Template loader class from package
        """
        return self.module.repository.template_loader

    def get_output_filename(self, directory):
        """
        Get output filename for rendered data
        """
        raise NotImplementedError(
            'get_output_filename() must be implemented in child class'
        )
