"""
Django app in project
"""
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

import inflection

from .model import Model
from .renderer import DjangoPackageRenderer

if TYPE_CHECKING:
    from .configuration import ProjectConfiguration

DEFAULT_APPS_PATH = 'apps'


class App(DjangoPackageRenderer):
    """
    Django app in vaskitsa managed django project
    """
    project: Optional[str]
    name: Optional[str]
    create_missing: bool
    sorted: bool
    mode: Optional[str]
    excluded: List[Path]
    configuration: Optional['ProjectConfiguration']

    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('app')
    __path_replacements__ = (
        'app_name',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls,
                path: Path,
                project: Optional[str] = None,
                name: Optional[str] = None,
                create_missing: bool = False,
                sorted: bool = True,
                mode: Optional[str] = None,
                excluded: List[Path] = list,
                configuration: Optional['ProjectConfiguration'] = None):
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self, path: Path, project: str, name: str) -> None:
        super().__init__(path)
        self.project = project
        self.app_name = name
        self.models = []

    def add_model(self, name: str) -> Model:
        """
        Get a model object for app
        """
        model = Model(str(self), app=self, name=name)
        self.models.append(model)
        return model

    def get_template_vars(self, **kwargs) -> dict:
        """
        Extend template vars for project
        """
        template_vars = super().get_template_vars(**kwargs)
        template_vars.update({
            'camel_case_app_name': inflection.camelize(self.name),
        })
        template_vars['models'] = [
            {
                'model_name': model.model_name,
                'model': inflection.camelize(model.model_name),
            }
            for model in self.models
        ]
        return template_vars

    def create(self, overwrite: bool = False) -> None:
        """
        Create app and it's models
        """
        module_init = self.joinpath('models/__init__.py')
        if module_init.exists():
            module_init.unlink()
        super().create(overwrite)
        for model in self.models:
            model.create(overwrite)
