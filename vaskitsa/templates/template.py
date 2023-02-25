"""
Render jinja2 templates to create files to documentation
"""
from pathlib import Path
from typing import Any, List, Optional, Union

from jinja2 import (
    Environment,
    FileSystemLoader,
    PackageLoader,
    select_autoescape
)
from jinja2.environment import Template
from jinja2 import exceptions as j2_exceptions

TEMPLATES_MODULE_PATH = Path('templates')
"""Relative path to templates in package"""


class TemplateError(Exception):
    """
    Group exceptions received from template processing
    """


class TemplateRenderer:
    """
    Generic base module to render Jinja2 templates to generate document
    tree files

    :param name: Name of template

    If name is missing extension, .j2 is added automatically.
    """
    name: str
    template_path: Path = TEMPLATES_MODULE_PATH
    autoescape: List[str] = ['html', 'xml']
    auto_extension: str = '.j2'

    def __init__(self, name: str, template_directory: Optional[Path] = None) -> None:
        self.template_directory = template_directory
        path = Path(name)
        if not path.suffix:
            path = path.with_suffix(self.auto_extension)
        self.name = path.name

    def __repr__(self) -> str:
        return self.name

    @property
    def loader(self) -> Union[FileSystemLoader, PackageLoader]:
        """
        Return template loader
        """
        if self.template_directory is not None:
            return FileSystemLoader(self.template_directory)
        return PackageLoader(self.__module__.split('.', maxsplit=1)[0], str(self.template_path))

    @property
    def environment(self) -> Environment:
        """
        Return jinja2 rendering environment
        """
        return Environment(loader=self.loader, autoescape=select_autoescape(self.autoescape))

    @property
    def template(self) -> Template:
        """
        Return template to be rendered
        """
        try:
            return self.environment.get_template(str(self.name))
        except j2_exceptions.TemplateNotFound as error:
            raise TemplateError(f'Error looking up {self} template {self.name}') from error

    def render(self, item: Any) -> str:
        """
        Render template to a string with specified item
        """
        return self.template.render({'item': item}).rstrip()
