"""
Constants for unit tests
"""

from pathlib import Path

# pylint: disable=unused-import
from ..constants import REPO_PACKAGE_PATH, REPO_ROOT_PATH  # noqa: F401

# Path to test module without __init__.py files
NO_INIT_PATH = Path(__file__).parent.joinpath('testdata/test-module-no-indexes')

# Packages expected in loading this repository
EXPECTED_MODULES = (
    'vaskitsa',
    'vaskitsa/bin',
    'vaskitsa/bin/commands',
    'vaskitsa/bin/commands/documentation',
    'vaskitsa/bin/commands/python',
    'vaskitsa/bin/commands/version',
    'vaskitsa/django',
    'vaskitsa/documentation',
    'vaskitsa/documentation/renderers',
    'vaskitsa/documentation/sphinx',
    'vaskitsa/git',
    'vaskitsa/hooks',
    'vaskitsa/hooks/python',
    'vaskitsa/python',
    'vaskitsa/python/classifiers',
    'vaskitsa/python/requirements',
    'vaskitsa/templates',
    'vaskitsa/templates/django',
    'vaskitsa/vscode',
)
EXPECTED_TEST_MODULES = (
    'tests',
    'tests/cli',
    'tests/git',
    'tests/documentation/testdata/test-module-no-indexes/a',
    'tests/documentation/testdata/test-module-no-indexes/b',
    'tests/documentation/testdata/test-module-no-indexes/c',
    'tests/documentation',
    'tests/mock/mock-python-module/mock_python_module',
    'tests/mock/mock-python-module/mock_python_module/demo',
    'tests/mock/mock-python-module/unittests',
    'tests/python',
)

# Ignore testdata directory
EXCLUDED = (
    'testdata',
)
