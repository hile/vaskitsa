"""
Template to create django model basic data structure to an django app
"""
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

import inflection

from .renderer import DjangoPackageRenderer

if TYPE_CHECKING:
    from .app import App
    from .configuration import ProjectConfiguration


class Model(DjangoPackageRenderer):
    """
    Django model template with filters, serializers, views and tests
    """
    app: 'App'
    configuration: Optional['ProjectConfiguration']
    name: str

    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('model')
    __path_replacements__ = (
        'model_name',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls,
                path: Path,
                app: Optional['App'] = None,
                name: str = None,
                create_missing: bool = False,
                sorted: bool = True,
                mode: str = None,
                excluded: List[Path] = list,
                configuration: Optional['ProjectConfiguration'] = None) -> None:
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self, path: Path, app: Optional['App'], name: str):
        super().__init__(path)
        self.app = app
        self.model_name = inflection.underscore(name)

    def get_template_vars(self, **kwargs) -> dict:
        """
        Expand template vars for model
        """
        template_vars = super().get_template_vars(**kwargs)
        template_vars.update({
            'app_name': self.app.app_name,
            'camel_case_model_name': inflection.camelize(self.model_name),
        })
        return template_vars
