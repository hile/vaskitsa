
from collections.abc import ItemsView, KeysView
from configparser import ConfigParser

from ..exceptions import PythonSetupError


class TestEnvironment:
    """
    Setup settings for testenv
    """
    def __init__(self, repository, settings):
        self.repository = repository
        self.settings = settings

    @staticmethod
    def __parse_line_list__(value):
        """
        Parse a field value with multiple lines of text
        """
        if value:
            return [
                line
                for line in value.splitlines()
                if line != ''
            ]
        return []

    @property
    def commands(self):
        """
        Parse test environment 'commands' list
        """
        return self.__parse_line_list__(self.settings.get('commands', None))

    @property
    def deps(self):
        """
        Parser test environment 'deps' list
        """
        return self.__parse_line_list__(self.settings.get('deps', None))


class SetupConfig(ConfigParser):
    """
    Parser for setup.cfg file in python repository
    """
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.path = self.repository.joinpath('setup.cfg')
        if self.path.is_file():
            if not self.read(self.path):
                raise PythonSetupError(f'Error loading {self.path}')

    def __getitem__(self, item):
        """
        Override __getitem__ to not return DEFAULT
        """
        if item == 'DEFAULT':
            raise KeyError
        return super().__getitem__(item)

    @property
    def testenv(self):
        """
        Return testenv settings parsed with TestEnvironment class
        """
        if 'testenv' not in self:
            raise PythonSetupError(f'testenv not configuredd in {self.path}')
        return TestEnvironment(self.repository, self['testenv'])

    def keys(self):
        """
        Return configuration without DEFAULT
        """
        return KeysView(key for key in super().keys() if key != 'DEFAULT')

    # pylint: disable=redefined-builtin
    def items(self, section=None, raw=False, vars=None):
        """
        Return configuration without DEFAULT
        """
        if section:
            return self[section].items()
        return ItemsView(dict((key, self[key]) for key in self.keys()))
