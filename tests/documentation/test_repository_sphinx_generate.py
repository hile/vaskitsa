"""
Test generating sphinx documentation for test data
"""

from systematic_files.tree import Tree
from vaskitsa.documentation.loader import get_processor

from .constants import NO_INIT_PATH


def test_repository_generate_sphinx_testdata():
    """
    Test generating sphinx documentation to test data directory
    """
    generator = get_processor('sphinx', NO_INIT_PATH)
    docs_directory = generator.default_output_directory
    assert not docs_directory.exists()

    generator.generate()
    assert docs_directory.exists()

    Tree(docs_directory).remove(recursive=True)
