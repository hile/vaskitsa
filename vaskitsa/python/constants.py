"""
Defaults for vaskita repositories
"""

import re

# Groups by module type
MODULE_DEFAULT_GROUP = 'modules'
TEST_MODULE_DEFAULT_GROUP = 'tests'

# Filenames ignored in repository root directory
REPOSITORY_ROOT_IGNORED_FILES = (
    'setup.py',
)

# Dummy version when version  is not available
DUMMY_VERSION = '0.0'

# Pattern to match __version__  field in __init__.py
RE_VERSION_LINE = re.compile(
    r"""^__version__\s*=\s*['"](?P<version>[0-9a-zA-Z.]+)['"].*$"""
)
