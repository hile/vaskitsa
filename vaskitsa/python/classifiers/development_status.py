"""
Classifier group for Development Status
"""

from .base import TroveClassifier, TroveClassifierGroup


# pylint: disable=too-few-public-methods
class DevelopmentStatus(TroveClassifier):
    """
    Development status value
    """
    def __init__(self, parent, path):
        super().__init__(parent, path)
        self.index, self.label = self.name.split(' - ')
        self.index = int(self.index)


class DevelopmentStatusGroup(TroveClassifierGroup):
    """
    Group loader for development status values
    """
    __classifier_loader_class__ = DevelopmentStatus

    def to_dict(self):
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
