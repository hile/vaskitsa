"""
Parsing of python package version from various places
"""
from typing import Optional, TYPE_CHECKING

from packaging.version import Version, InvalidVersion
from pathlib_tree.tree import FilesystemError

import toml

from .constants import DUMMY_VERSION, PYPROJECT_TOML_FILE, RE_VERSION_LINE, VersionTypes
from .utils import validate_module_name

if TYPE_CHECKING:
    from .package import Package


class PythonPackageVersion(Version):
    """
    Class to handle package version parsing and updating
    """
    package: 'Package'
    main_module_name: str
    version_type: str

    def __init__(self, package: 'Package', main_module_name: Optional[str] = None) -> None:
        self.package = package
        if main_module_name is None:
            main_module_name = validate_module_name(package.name.replace('-', '_'))
        self.main_module_name = validate_module_name(main_module_name)
        self.version_type = None
        super().__init__(self.__load__())

    def __get_peotry_tool_section__(self) -> dict:
        """
        Get poetry setting section from pyproject.toml file

        Returns empty dictionary if configuration is not found in file
        """
        path = self.package.joinpath(PYPROJECT_TOML_FILE)
        if not path.is_file():
            return {}
        with path.open('r', encoding='utf-8') as filedescriptor:
            return toml.loads(filedescriptor.read()).get('tool', {}).get('poetry', {})

    def __load_poetry_version__(self) -> Optional[str]:
        """
        Load poetry version from pyproject.toml file
        """
        poetry = self.__get_peotry_tool_section__()
        if poetry:
            value = poetry.get('version', None)
            if value is not None:
                self.version_type = VersionTypes.POETRY
                return value
        return None

    def __load_module_version__(self) -> Optional[str]:
        """
        Read version string from pyproject.toml file or __init__.py variable __version__
        """
        module = self.package.get_python_module(self.main_module_name)
        if module and module.index:
            with open(module.index.path, 'r', encoding='utf-8') as filedescriptor:
                for line in filedescriptor.readlines():
                    match = RE_VERSION_LINE.match(line)
                    if match:
                        self.version_type = VersionTypes.MODULE
                        return match.groupdict()['version']
        return None

    def __load__(self) -> str:
        """
        Load version string from known sources
        """
        loaders = (
            self.__load_poetry_version__,
            self.__load_module_version__,
        )
        for loader in loaders:
            version = loader()
            if version is not None:
                return version
        return DUMMY_VERSION

    def update_module_version(self, version: str) -> None:
        """
        Update new version to the version __init__.py __version__ field
        """
        if not isinstance(version, Version):
            version = Version(version)
        if self != DUMMY_VERSION and version <= self:
            raise InvalidVersion(
                f'New version {version} is smaller or same as previous version {self}'
            )
        module = self.package.get_python_module(self.main_module_name)
        if not module:
            raise FilesystemError('package has no main module')
        if not module.index:
            module.create_file('__init__.py')

        lines = []
        version_line = f"""__version__ = '{version}'\n"""
        with open(module.index.path, 'r', encoding='utf-8') as filedescriptor:
            for line in filedescriptor.readlines():
                match = RE_VERSION_LINE.match(line)
                if match:
                    lines.append(version_line)
                else:
                    lines.append(line)
        lines = [line.rstrip() for line in lines]
        with open(module.index.path, 'w', encoding='utf-8') as filedescriptor:
            data = '\n'.join(lines)
            filedescriptor.write(f'{data}\n')
