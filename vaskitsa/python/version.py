
from packaging.version import Version, InvalidVersion

from systematic_files.tree import FilesystemError

from .constants import DUMMY_VERSION, RE_VERSION_LINE
from .utils import validate_module_name


class PythonRepositoryVersion(Version):
    """
    Class to handle repository version parsing and updating
    """

    def __init__(self, repository, main_module_name=None):
        self.repository = repository
        if main_module_name is None:
            main_module_name = validate_module_name(
                repository.name.replace('-', '_')
            )
        self.main_module_name = validate_module_name(main_module_name)
        super().__init__(self.__load__())

    def __load__(self):
        """
        Read version string from __init__.py variable __version__
        """
        module = self.repository.get_module(self.main_module_name)
        if module and module.index:
            with open(module.index.path, 'r', encoding='utf-8') as filedescriptor:
                for line in filedescriptor.readlines():
                    match = RE_VERSION_LINE.match(line)
                    if match:
                        return match.groupdict()['version']
        return DUMMY_VERSION

    def update(self, version):
        """
        Update new version to the version __init__.py __version__ field
        """
        if not isinstance(version, Version):
            version = Version(version)
        if self != DUMMY_VERSION and version <= self:
            raise InvalidVersion(
                f'New version {version} is smaller or same as previous version {self}'
            )
        module = self.repository.get_module(self.main_module_name)
        if not module:
            raise FilesystemError('Repository has no main module')
        if not module.index:
            module.create_file('__init__.py')

        lines = []
        version_line = f"""__version__ = '{version}'\n"""
        with open(module.index.path, 'r') as filedescriptor:
            for line in filedescriptor.readlines():
                match = RE_VERSION_LINE.match(line)
                if match:
                    lines.append(version_line)
                else:
                    lines.append(line)
        lines = [line.rstrip() for line in lines]
        with open(module.index.path, 'w') as filedescriptor:
            data = '\n'.join(lines)
            filedescriptor.write(f'{data}\n')
