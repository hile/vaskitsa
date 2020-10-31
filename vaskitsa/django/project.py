"""
Django project
"""

import secrets
from pathlib import Path

import inflection

from .app import App, DEFAULT_APPS_PATH
from .renderer import DjangoPackageRenderer

SECRET_ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_LENGTH = 50


class Project(DjangoPackageRenderer):
    """
    Django project generator
    """
    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('project')
    __path_replacements__ = (
        'project_name',
        'project_version',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls, path, name=None, version=None,
                apps_path=DEFAULT_APPS_PATH,
                create_missing=False, sorted=True, mode=None, excluded=list, configuration=None):
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self, path, name=None, version=None, apps_path=DEFAULT_APPS_PATH):
        super().__init__(path)
        self.project_name = name if name else inflection.underscore(self.name)
        self.project_version = version
        self.apps_path = self.joinpath(apps_path)
        self.apps = []

    def __repr__(self):
        return str(self)

    @staticmethod
    def generate_secret():
        """
        Generate secret for django project
        """
        return ''.join(secrets.choice(SECRET_ALLOWED_CHARS) for i in range(SECRET_LENGTH))

    def get_template_vars(self, **kwargs):
        """
        Extend template vars for project
        """
        template_vars = super().get_template_vars(**kwargs)
        template_vars.update({
            'settings_module': 'config.settings.base',
            'secret_key': self.generate_secret(),
            'database_host': '127.0.0.1',
            'database_port': '5432',
            'database_name': inflection.underscore(self.name),
            'database_user': inflection.underscore(self.name),
            'database_password': self.generate_secret(),
        })
        return template_vars

    def add_app(self, name):
        """
        Get app from project
        """
        app = App(self.apps_path.joinpath(name), project=self, name=name)
        self.apps.append(app)
        return app

    def create(self, overwrite=False):
        """
        Create project
        """
        super().create(overwrite)
        self.joinpath('manage.py').chmod(int('0755', 8))
        for app in self.apps:
            app.create()
