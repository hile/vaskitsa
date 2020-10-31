"""
Template to create django model basic data structure to an django app
"""

from pathlib import Path

import inflection

from .renderer import DjangoPackageRenderer


class Model(DjangoPackageRenderer):
    """
    Django model template with filters, serializers, views and tests
    """
    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('model')
    __path_replacements__ = (
        'model_name',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls, path, app=None, name=None,
                create_missing=False, sorted=True, mode=None, excluded=list, configuration=None):
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self, path, app, name):
        super().__init__(path)
        self.app = app
        self.model_name = inflection.underscore(name)

    def get_template_vars(self, **kwargs):
        """
        Expand template vars for model
        """
        template_vars = super().get_template_vars(**kwargs)
        template_vars.update({
            'app_name': self.app.app_name,
            'camel_case_model_name': inflection.camelize(self.model_name),
        })
        return template_vars
