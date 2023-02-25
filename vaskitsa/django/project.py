"""
Django project
"""
import secrets

from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

import inflection

from .app import App, DEFAULT_APPS_PATH
from .renderer import DjangoPackageRenderer

SECRET_ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_LENGTH = 50

if TYPE_CHECKING:
    from .configuration import ProjectConfiguration


class Project(DjangoPackageRenderer):
    """
    Django project generator
    """
    configuration: Optional['ProjectConfiguration']
    project_name: str
    project_version: str
    name: str
    apps_path = Path
    apps: List[App]

    __template_root_path__ = DjangoPackageRenderer.__template_root_path__.joinpath('project')
    __path_replacements__ = (
        'project_name',
        'project_version',
    )

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls,
                path: Path,
                name: Optional[str] = None,
                version: Optional[str] = None,
                apps_path: str = DEFAULT_APPS_PATH,
                create_missing: bool = False,
                sorted: bool = True,
                mode: str = None,
                excluded: List[Path] = list,
                configuration: Optional['ProjectConfiguration'] = None):
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self,
                 path: Path,
                 name: str = None,
                 version: str = None,
                 apps_path: str = DEFAULT_APPS_PATH):
        super().__init__(path)
        self.project_name = name if name else inflection.underscore(self.name)
        self.project_version = version
        self.apps_path = self.joinpath(apps_path)
        self.apps = []

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def generate_secret() -> str:
        """
        Generate secret for django project
        """
        return ''.join(secrets.choice(SECRET_ALLOWED_CHARS) for i in range(SECRET_LENGTH))

    def get_template_vars(self, **kwargs) -> dict:
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

    def add_app(self, name: str) -> App:
        """
        Get app from project
        """
        app = App(self.apps_path.joinpath(name), project=self, name=name)
        self.apps.append(app)
        return app

    def create(self, overwrite: bool = False) -> None:
        """
        Create project
        """
        super().create(overwrite)
        self.joinpath('manage.py').chmod(int('0755', 8))
        for app in self.apps:
            app.create()
