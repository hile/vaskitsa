"""
Python package Trove Classifiers loader
"""
from collections.abc import Collection
from typing import Dict, List, Optional

import requests

from .base import TroveClassifier, TroveClassifierGroup
from .development_status import DevelopmentStatusGroup

CLASSIFIERS_URL = 'https://pypi.org/pypi?%3Aaction=list_classifiers'
CLASSIFIERS_LOOKUP_TIMEOUT = 15


class Classifiers(Collection):
    """
    Singleton class to load and validate python trove classifiers
    """
    __classifiers__: Optional[List[TroveClassifier]] = None
    __group_loader_classes__ = {
        'Development Status': DevelopmentStatusGroup,
    }
    groups: Dict = {}

    def __init__(self) -> None:
        if Classifiers.__classifiers__ is None:
            Classifiers.__classifiers__ = Classifiers.__load_classifiers__(self)

    def __parse_classifier_topic_line__(self, line: str) -> TroveClassifier:
        """
        Parse a classifier from line
        """
        path = line.split(' :: ')
        if len(path) == 1:
            return None
        group = path[0]
        if group not in self.groups:
            loader = self.__group_loader_classes__.get(group, TroveClassifierGroup)
            self.groups[group] = loader(group)
        return self.groups[group].add_classifer(path)

    def __load_classifiers__(self) -> List[str]:
        """
        Loads classifiers from pypi.org
        """
        res = requests.get(CLASSIFIERS_URL, timeout=CLASSIFIERS_LOOKUP_TIMEOUT)
        if res.status_code != 200:
            raise ValueError(
                f'Error fetching classifiers from {CLASSIFIERS_URL}: '
                f'HTTP status code {res.status_code}'
            )
        classifiers = []
        for line in str(res.content, encoding='utf-8').splitlines():
            item = self.__parse_classifier_topic_line__(line)
            classifier = str(item)
            if classifier is not None:
                classifiers.append(classifier)
        return classifiers

    def __contains__(self, item: str) -> bool:
        return item in self.__classifiers__

    def __iter__(self):
        return iter(self.__classifiers__)

    def __len__(self) -> int:
        return len(self.__classifiers__)

    def __getitem__(self, index: int) -> str:
        return self.__classifiers__[index]

    def to_dict(self) -> dict:
        """
        Return classifier data as dictionary
        """
        return dict(
            (name, group.to_dict())
            for name, group in self.groups.items()
        )
