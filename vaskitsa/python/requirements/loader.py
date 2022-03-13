"""
Python requirements
"""

import re

from collections.abc import MutableSet
from pathlib import Path

from .requirement import Editable, Include, Line, Package, RequirementTypes

RE_EDITABLE = re.compile(r'^-e\s+(?P<path>[^#]+)$')
RE_REFERENCE = re.compile(r'^-r\s+(?P<path>[^#]+)$')

EXPECTED_OBJECT_TYPES = (Editable, Include, Line, Package)


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
        self.line = line.rstrip()
        self.item = self.parse_line(line)

    def __repr__(self):
        return self.line

    def __match_patterns__(self, line):
        """
        Match line to regexp patterns and return object with matching loader
        if pattern matches
        """
        for (pattern, loader) in self.__regexp_match_classes__:
            match = pattern.match(line)
            if match:
                return loader(self, line, **match.groupdict())
        return None

    @property
    def type(self):
        """
        Return requirement type
        """
        return self.item.__type__

    def parse_line(self, line):
        """
        Parse lines in requirements file as Requirement objects
        """
        reference = self.__match_patterns__(line)
        if reference is not None:
            return reference
        if line.strip() == '' or line.strip().startswith('#'):
            return Line(self, line)
        return Package(self, line)


class RequirementsList(MutableSet):
    """
    List of python package requirements
    """
    def __init__(self, package=None, ignored=None):
        super().__init__()
        self.package = package
        self.ignored = ignored if ignored else []
        self.__items__ = []

    def __contains__(self, value):
        """
        Checks for existing requirement
        """
        return value in self.__items__

    def __iter__(self):
        """
        Checks for existing requirement
        """
        return iter(list(self.__items__))

    def __len__(self):
        """
        Checks for existing requirement
        """
        return len(self.__items__)

    @property
    def includes(self):
        """
        Return requirements list include lines for other requirements
        """
        return [entry for entry in list(self) if entry.type == RequirementTypes.INCLUDE]

    @property
    def editables(self):
        """
        Return requirements list editable lines for other requirements
        """
        return [entry for entry in list(self) if entry.type == RequirementTypes.EDITABLE]

    @property
    def packages(self):
        """
        Return requirements list package requirement lines for other requirements
        """
        return [entry for entry in list(self) if entry.type == RequirementTypes.PACKAGE]

    def discard(self, value):
        """
        Remove requirement
        """

    def add(self, value):
        """
        Add requirement
        """
        if not isinstance(value.item, EXPECTED_OBJECT_TYPES):
            raise ValueError(f'Unexpected value item type: {value.item}')
        self.__items__.append(value)


class RequirementsFile(RequirementsList):
    """
    Python requirements file
    """
    def __init__(self, path, package=None, ignored=None):
        super().__init__(package, ignored)
        self.path = Path(path).expanduser().resolve()
        self.__lines__ = []

    def __repr__(self):
        return str(self.path)

    def load(self):
        """
        Load requirments file lines
        """
        with self.path.open('r', encoding='utf-8') as filedescriptor:
            for line in filedescriptor.readlines():
                dependency = RequirementsFileLine(self, line)
                if dependency.item.requirement.name not in self.ignored:
                    self.add(dependency)
