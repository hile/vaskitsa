"""
Python requirements
"""

import re

from collections.abc import MutableSet
from pathlib import Path

from packaging.requirements import Requirement

RE_EDITABLE = re.compile(r'^-e\s+(?P<path>[^#]+)$')
RE_REFERENCE = re.compile(r'^-r\s+(?P<path>[^#]+)$')


# pylint: disable=too-few-public-methods
class RequirementsFileItem:
    """
    Reference in requirements file
    """
    def __init__(self, container, line):
        self.container = container
        self.line = line


# pylint: disable=too-few-public-methods
class Include(RequirementsFileItem):
    """
    Reference to requirement file
    """
    def __init__(self, container, line, path):
        super().__init__(container, line)
        path = Path(path)
        if not path.is_absolute():
            path = self.container.requirements.path.parent.joinpath(path)
        self.path = path

    def __repr__(self):
        return str(self.path)


# pylint: disable=too-few-public-methods
class Editable(RequirementsFileItem):
    """
    Reference to editable requirement
    """
    def __init__(self, container, line, path):
        super().__init__(container, line)
        path = Path(path)
        if not path.is_absolute():
            path = self.container.requirements.repository.joinpath(path)
        self.path = path

    def __repr__(self):
        return str(self.path.relative_to(self.container.requirements.repository))


# pylint: disable=too-few-public-methods
class PackageRequirement(RequirementsFileItem):
    """
    Reference to package requirement
    """
    def __init__(self, container, line, requirement):
        super().__init__(container, line)
        self.requirement = requirement

    def __repr__(self):
        return str(self.requirement)


class Requirements(MutableSet):
    """
    List of python package requirements
    """
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.includes = []
        self.editables = []
        self.packages = []

    def __contains__(self, value):
        """
        Checks for existing requirement
        """

    def __iter__(self):
        """
        Checks for existing requirement
        """

    def __len__(self):
        """
        Checks for existing requirement
        """

    def discard(self, value):
        """
        Remove requirement
        """

    def add(self, value):
        """
        Add requirement
        """
        if isinstance(value.item, Editable):
            self.editables.append(value)
        if isinstance(value.item, Include):
            self.includes.append(value)
        if isinstance(value.item, PackageRequirement):
            self.packages.append(PackageRequirement)


class RequirementsFileLine:
    """
    Line in requirements file
    """
    __regexp_match_classes__ = (
        (RE_EDITABLE, Editable),
        (RE_REFERENCE, Include),
    )

    def __init__(self, requirements, line):
        self.requirements = requirements
        self.line = line
        self.item = self.parse_line(line)

    def __repr__(self):
        return f'{self.line} {type(self.item)}'

    def __parse_reference__(self, line):
        """
        Parse a reference to editable or git requirement
        """
        for (pattern, loader) in self.__regexp_match_classes__:
            match = pattern.match(line)
            if match:
                return loader(self, line, **match.groupdict())
        return None

    def parse_line(self, line):
        """
        Parse lines in requirements file as Requirement objects
        """
        reference = self.__parse_reference__(line)
        if reference is not None:
            return reference
        if line.strip() == '' or line.strip().startswith('#'):
            return RequirementsFileItem(self, line)
        return PackageRequirement(self, line, Requirement(line))


class RequirementsFile(Requirements):
    """
    Python requirements file
    """
    def __init__(self, repository, path):
        super().__init__(repository)
        self.path = Path(path).expanduser()
        self.__lines__ = []

    def load(self):
        """
        Load requirments file lines
        """
        with self.path.open('r') as filedescriptor:
            for line in filedescriptor.readlines():
                self.add(RequirementsFileLine(self, line.rstrip()))
