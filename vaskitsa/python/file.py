"""
Base class for python file
"""

from pathlib import Path
import os

from pathlib_tree.exceptions import FilesystemError

EMPTY_FILE = '''"""
Automatically generated file
"""
'''


class PythonFile:
    """
    Python code file
    """

    def __init__(self, path, module=None, create_missing=False):
        self.module = module
        self.path = Path(path)
        if not self.path.is_file() and create_missing:
            with open(self.path, 'w', encoding='utf-8') as filedescriptor:
                filedescriptor.write(EMPTY_FILE)
        self.module_root = self.path.name == '__init__.py'

    def __repr__(self):
        if self.import_path is not None:
            if self.path.name == '__init__.py':
                return self.path.name
            return self.import_path
        return str(self.path)

    @property
    def relative_path(self):
        """
        Return path relative to package
        """
        if self.module and self.module.repository:
            return self.path.relative_to(self.module.repository)
        return None

    @property
    def relative_directory(self):
        """
        Return parent directory relativve to package root
        """
        if self.relative_path:
            return self.relative_path.parent
        return None

    @property
    def import_path(self):
        """
        Return file import path
        """
        path = self.relative_path
        if path is not None:
            if path.name == '__init__.py':
                path = path.with_suffix('').parent
            else:
                path = path.with_suffix('')
            return str(path).replace(os.sep, '.')
        return None

    @property
    def is_index(self):
        """
        Check if this is file is module root index (__init__.py)
        """
        return self.path.name == '__init__.py'

    @property
    def is_module_index(self):
        """
        Check if this is file is modle root index (__init__)
        """
        return self.module and self.module.parent is None and self.path.name == '__init__.py'

    @property
    def name(self):
        """
        Return name of file without extension
        """
        return self.path.stem

    def debug(self, *args):
        """
        Pass debug message to repository
        """
        if self.module:
            return self.module.debug(*args)
        raise FilesystemError('File not linked to a module')

    def error(self, *args):
        """
        Pass error message to repository
        """
        if self.module:
            return self.module.error(*args)
        raise FilesystemError('File not linked to a module')

    def message(self, *args):
        """
        Pass messages to repository
        """
        if self.module:
            return self.module.message(*args)
        raise FilesystemError('File not linked to a module')
