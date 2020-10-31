"""
Test loading processor with invalid type
"""

import pytest

from vaskitsa.documentation.loader import get_processor
from vaskitsa.documentation.base import DocumentGeneratorError

from .constants import REPO_ROOT_PATH


def test_processor_invalid_type():
    """
    Test lookup for processor with invalid type
    """
    with pytest.raises(DocumentGeneratorError):
        get_processor('invalid', REPO_ROOT_PATH)
