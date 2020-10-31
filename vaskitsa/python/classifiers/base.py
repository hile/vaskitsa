"""
Python trove classifiers and classifiers groups
"""


# pylint: disable=too-few-public-methods
class TroveClassifier:
    """
    Base class for trove classifiers
    """
    def __init__(self, parent, path):
        self.parent = parent
        self.path = path
        self.name = path[-1]

    def __repr__(self):
        return ' :: '.join(self.path)


# pylint: disable=
class TroveClassifierGroup:
    """
    Base class for Trove classifiers
    """
    __group_loader_classes__ = {}
    __classifier_loader_class__ = TroveClassifier

    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        self.classifiers = []
        self.groups = {}

    def __repr__(self):
        return self.name

    def __get_path__group__(self, path):
        """
        Get group for path

        Creates tree of groups as side effect
        """
        if len(path) == 1:
            return self
        name = path[0]
        if name not in self.groups:
            loader = self.__group_loader_classes__.get(name, TroveClassifierGroup)
            self.groups[name] = loader(name, parent=self)
        return self.groups[name].__get_path__group__(path[1:])

    @property
    def path(self):
        """
        Return trove groups path
        """
        path = [self]
        parent = self.parent
        while parent is not None:
            path.append(parent)
            parent = parent.parent
        return list(reversed(path))

    def add_classifer(self, path):
        """
        Add classifier to group
        """
        group = self.__get_path__group__(path[1:])
        classifier = group.__classifier_loader_class__(group, path)
        group.classifiers.append(classifier)
        return classifier

    def to_dict(self):
        """
        Returns trove group as dictionary
        """
        if self.groups:
            return dict(
                (name, group.to_dict())
                for name, group in self.groups.items()
            )
        return [classifier.name for classifier in self.classifiers]
