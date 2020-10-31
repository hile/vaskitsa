"""
Django app in project
"""

from pathlib import Path

import inflection

from .model import Model
from .renderer import DjangoPackageRenderer

DEFAULT_APPS_PATH = 'apps'


class App(DjangoPackageRenderer):
    """
    Django app in vaskitsa managed django project
    """
    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('app')
    __path_replacements__ = (
        'app_name',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls, path, project=None, name=None,
                create_missing=False, sorted=True, mode=None, excluded=list, configuration=None):
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self, path, project, name):
        super().__init__(path)
        self.project = project
        self.app_name = name
        self.models = []

    def add_model(self, name):
        """
        Get a model object for app
        """
        model = Model(str(self), app=self, name=name)
        self.models.append(model)
        return model

    def get_template_vars(self, **kwargs):
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

    def create(self, overwrite=False):
        """
        Create app and it's models
        """
        module_init = self.joinpath('models/__init__.py')
        if module_init.exists():
            module_init.unlink()
        super().create(overwrite)
        for model in self.models:
            model.create(overwrite)
