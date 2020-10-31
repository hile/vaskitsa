
from pathlib import Path

from ..module import ModuleDocumentGenerator
from .file import AutoModuleFileGenerator


class AutodocModuleGenerator(ModuleDocumentGenerator):
    """
    Autodoc output generator for python module in a package
    """
    python_file_class = AutoModuleFileGenerator
    """Class for loading python files from autodoc module"""

    @property
    def index_max_depth(self):
        """
        Return index max depth for module documentation TOC
        """
        return self.repository.template_configuration.module_index_max_depth

    @property
    def template_directory(self):
        """
        Return directory for templates from configuration

        By default returns None
        """
        return self.repository.template_directory

    @property
    def template_name(self):
        """
        Return template name for module documentation
        """
        return self.repository.template_configuration.templates.module

    @property
    def caption(self):
        """
        Caption for module index
        """
        return str(self.relative_directory)

    @property
    def file_import_paths(self):
        """
        Return file import paths in TOC format
        """
        return [
            item.path.relative_to(self).with_suffix('')
            for item in self.files
        ]

    def get_output_filename(self, directory):
        """
        Return output filename for generated module index
        """
        return Path(directory, self.relative_directory, 'index.rst')
