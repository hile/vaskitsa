"""
Test error handling from template renderer
"""

import pytest

from vaskitsa.templates.template import TemplateRenderer, TemplateError


def test_template_missing_template_file():
    """
    Test attempt to load missing template file
    """
    template = TemplateRenderer(name='missing_template.j2')
    with pytest.raises(TemplateError):
        # pylint: disable=pointless-statement
        template.template
