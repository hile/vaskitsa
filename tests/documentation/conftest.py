"""
Unit test configuration for vaskitsa.documentation module
"""
from pathlib import Path
import pytest

MOCK_TEMPLATE_NAME = 'mock-template-file'
MOCK_TEMPLATE = """{{ name }}"""


@pytest.fixture
def mock_template(tmpdir):
    """
    Mock creating empty jinja2 template for unit tests
    """
    path = Path(tmpdir.strpath, f'{MOCK_TEMPLATE_NAME}.j2')
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)
    with path.open('w', encoding='utf-8') as handle:
        handle.write(f'{MOCK_TEMPLATE}\n')
    yield path
