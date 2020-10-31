"""
Template renderer for sphinx jinja templaes
"""

from vaskitsa.templates.template import (
    TemplateRenderer,
    TEMPLATES_MODULE_PATH
)


class SphinxTemplateRenderer(TemplateRenderer):
    """
    Sphinx jinja template renderer
    """
    name = 'sphinx'
    template_path = TEMPLATES_MODULE_PATH.joinpath('sphinx')
    auto_extension = '.rst.j2'
