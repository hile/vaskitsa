"""
Django project template configuration
"""

from pathlib import Path

import yaml

from .project import Project


# pylint: disable=too-few-public-methods
class ProjectConfiguration:
    """
    Loader for django project template configuration yaml files
    """
    def __init__(self, directory, configuration_template):
        self.directory = Path(directory)
        self.path = Path(configuration_template)
        self.project = None

    def load(self):
        """
        Load project configuration
        """
        self.project = None
        with self.path.open('r') as filedescriptor:
            config = yaml.safe_load(filedescriptor.read())

        self.project = Project(
             self.directory.joinpath(config['name']),
             config.get('version', None)
        )
        for item in config.get('apps', []):
            app = self.project.add_app(item['name'])
            for model in item.get('models', []):
                app.add_model(model)
