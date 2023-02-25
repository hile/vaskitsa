"""
Classifier group for Development Status
"""
from typing import List

from .base import TroveClassifier, TroveClassifierGroup


# pylint: disable=too-few-public-methods
class DevelopmentStatus(TroveClassifier):
    """
    Development status value
    """
    index: int
    label: str

    def __init__(self, parent: TroveClassifierGroup, path: List[str]) -> None:
        super().__init__(parent, path)
        index, self.label = self.name.split(' - ')
        self.index = int(index)


class DevelopmentStatusGroup(TroveClassifierGroup):
    """
    Group loader for development status values
    """
    __classifier_loader_class__ = DevelopmentStatus

    def to_dict(self) -> dict:
        """
        Return development status strings as dict
        """
        return [
            {
                'index': item.index,
                'label': item.label,
            }
            for item in self.classifiers
        ]
