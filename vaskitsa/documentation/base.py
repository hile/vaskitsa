"""
Document generator base classes
"""
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING

from ..exceptions import DocumentGeneratorError

if TYPE_CHECKING:
    from vaskitsa.templates.template import TemplateRenderer


class TemplateGenerator:
    """
    Common base class for items linked to template generators
    """
    template_name: str = None

    @property
    def template_directory(self) -> Optional[Path]:
        """
        Return directory for templates from configuration

        By default returns None
        """
        return None

    @property
    def template_loader(self) -> type['TemplateRenderer']:
        """
        Return jinja2 template loader class

        Must return instance of vaskitsa.templates.Template
        """
        raise NotImplementedError('Property template_loader must be implemented in child class')

    @property
    def template_renderer(self) -> 'TemplateRenderer':
        """
        Return template renderer for item
        """
        if self.template_name is None:
            raise DocumentGeneratorError(f'{self.__class__} does not define template_name')
        return self.template_loader(self.template_name, self.template_directory)

    def debug(self, *args) -> None:
        """
        Stub for debug messages
        """
        raise NotImplementedError

    def error(self, *args) -> None:
        """
        Stub for error callback
        """
        raise NotImplementedError

    def message(self, *args) -> None:
        """
        Stub for message callbacck
        """
        raise NotImplementedError

    def get_output_filename(self, directory: Union[str, Path]) -> Path:
        """
        Get output filename for rendered data
        """
        raise NotImplementedError('get_output_filename() must be implemented in child class')

    def render_template(self) -> str:
        """
        Render template, returning the data from template as string
        """
        return self.template_renderer.render(self)

    def generate(self, directory: Union[str, Path]) -> Path:
        """
        Generate output file by rendering template
        """
        path = self.get_output_filename(directory)

        if not path.parent.is_dir():
            self.debug('create directory', path.parent)
            path.parent.mkdir(parents=True)

        with open(path, 'w', encoding='utf-8') as filedescriptor:
            filedescriptor.write(f'{self.render_template()}\n')
        return path
