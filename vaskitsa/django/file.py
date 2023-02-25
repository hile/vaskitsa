"""
Templated file for django projects and apps
"""
from pathlib import Path
from typing import TYPE_CHECKING

from vaskitsa.templates.template import TemplateRenderer

if TYPE_CHECKING:
    from .model import Model


class FileTemplate(TemplateRenderer):
    """
    File with template variable substition for django projects
    """
    component: 'Model'
    path: Path

    def __init__(self, component: 'Model', path: Path) -> None:
        super().__init__(path.name, template_directory=path.parent)
        self.component = component
        self.path = path

    def __repr__(self) -> str:
        return str(self.path)

    # pylint: disable=arguments-differ,arguments-renamed
    def render(self, target_path) -> None:
        """
        Render template to target path
        """
        kwargs = self.component.get_template_vars()
        with open(target_path, 'w', encoding='utf-8') as handle:
            # pylint: disable=consider-using-f-string
            handle.write('{}\n'.format(self.template.render(**kwargs)))
