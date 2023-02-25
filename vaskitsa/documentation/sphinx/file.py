"""
File in python documentation tree sphinx documentation
"""
from pathlib import Path
from typing import List, Union

from ..file import FileDocumentGenerator


class AutoModuleFileGenerator(FileDocumentGenerator):
    """
    Autodoc automodule import generator for python file
    """

    @property
    def template_directory(self) -> Path:
        """
        Return directory for templates from configuration

        By default returns None
        """
        return self.module.package.template_directory

    @property
    def template_name(self) -> str:
        """
        Return template name for module documentation
        """
        return self.module.package.template_configuration.templates.file

    @property
    def automodule_flags(self) -> List[str]:
        """
        Generate list of automodule flags, indented with 4 spaces
        """
        flags = self.module.package.template_configuration.automodule_flags
        return [f':{flag}:' for flag in flags]

    @property
    def file_import_paths(self) -> List[Path]:
        """
        Return module file import paths excluding this file
        """
        return [
            item.path.relative_to(self.module).with_suffix('')
            for item in self.module.files
            if item != self
        ]

    def get_output_filename(self, directory: Union[str, Path]) -> Path:
        """
        Return output filename for generated file

        If this is module index file __inint__.py generate index.rst
        """
        if self.is_index:
            return Path(
                directory,
                self.relative_directory,
                'index.rst'
            )
        return Path(
            directory,
            self.relative_directory,
            f'{self.name}.rst'
        )
