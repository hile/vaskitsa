"""
Classes for handling a single requirement reference
"""

from enum import Enum
from pathlib import Path

from packaging.requirements import Requirement


class RequirementTypes(Enum):
    """
    Known types of requirements
    """
    EDITABLE = 'Editable developer requirement'
    INCLUDE = 'Requirements file include reference'
    PACKAGE = 'Package requirement'


# pylint: disable=too-few-public-methods
class Line:
    """
    Base class for requirement items

    This class is used for comments and empty lines in requirements files
    """
    __type__ = None

    def __init__(self, container, line):
        self.container = container
        self.line = line.rstrip()


# pylint: disable=too-few-public-methods
class Include(Line):
    """
    Reference to other requirement file by path
    """
    __type__ = RequirementTypes.INCLUDE

    def __init__(self, container, line, path):
        super().__init__(container, line)
        path = Path(path)
        if not path.is_absolute():
            path = self.container.requirements.path.parent.joinpath(path)
        self.path = path

    def __repr__(self):
        return str(self.path)


# pylint: disable=too-few-public-methods
class Editable(Line):
    """
    Reference to editable requirement
    """
    __type__ = RequirementTypes.EDITABLE

    def __init__(self, container, line, path):
        super().__init__(container, line)
        path = Path(path).resolve()
        self.path = path

    def __repr__(self):
        return str(self.path)


# pylint: disable=too-few-public-methods
class Package(Line):
    """
    Reference to package requirement

    Package requirement is handled by packaging module
    """
    __type__ = RequirementTypes.PACKAGE

    def __init__(self, container, line):
        super().__init__(container, line)
        self.requirement = Requirement(line)

    def __repr__(self):
        return str(self.requirement)
