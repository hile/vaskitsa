"""
Python module setup configuration and test environment
"""
from collections.abc import ItemsView, KeysView
from pathlib import Path
from typing import Any, List, TYPE_CHECKING

from configparser import ConfigParser

from ..exceptions import PythonSetupError

if TYPE_CHECKING:
    from .package import Package


class TestEnvironment:
    """
    Setup settings for testenv
    """
    package: 'Package'
    settings: dict

    def __init__(self, package: 'Package', settings: dict) -> None:
        self.package = package
        self.settings = settings

    @staticmethod
    def __parse_line_list__(value: str) -> List[str]:
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
    def commands(self) -> List[str]:
        """
        Parse test environment 'commands' list
        """
        return self.__parse_line_list__(self.settings.get('commands', None))

    @property
    def deps(self) -> List[str]:
        """
        Parser test environment 'deps' list
        """
        return self.__parse_line_list__(self.settings.get('deps', None))


class SetupConfig(ConfigParser):
    """
    Parser for setup.cfg file in python package
    """
    package: 'Package'
    path: Path

    def __init__(self, package: 'Package'):
        super().__init__()
        self.package = package
        self.path = self.package.joinpath('setup.cfg')
        if self.path.is_file():
            if not self.read(self.path):
                raise PythonSetupError(f'Error loading {self.path}')

    def __getitem__(self, item) -> Any:
        """
        Override __getitem__ to not return DEFAULT
        """
        if item == 'DEFAULT':
            raise KeyError
        return super().__getitem__(item)

    @property
    def testenv(self) -> TestEnvironment:
        """
        Return testenv settings parsed with TestEnvironment class
        """
        if 'testenv' not in self:
            raise PythonSetupError(f'testenv not configured in {self.path}')
        return TestEnvironment(self.package, self['testenv'])

    def keys(self) -> KeysView:
        """
        Return configuration without DEFAULT
        """
        return KeysView(key for key in super().keys() if key != 'DEFAULT')

    # pylint: disable=redefined-builtin
    def items(self, section: str = None, raw: bool = False, vars: List[str] = None) -> ItemsView:
        """
        Return configuration without DEFAULT
        """
        if section:
            return self[section].items()
        # pylint: disable=consider-using-dict-items
        return ItemsView(dict((key, self[key]) for key in self.keys()))
