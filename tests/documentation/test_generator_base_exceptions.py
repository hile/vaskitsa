"""
Test exceptions from generator base class
"""

import pytest

from vaskitsa.documentation.base import DocumentGeneratorError, TemplateGenerator
from vaskitsa.templates.template import TemplateRenderer


# pylint: disable=abstract-method
class NoTemplateRenderer(TemplateGenerator):
    """
    Test class without template renderer
    """
    template_name = 'huuhaa'


# pylint: disable=abstract-method
class NoTemplateName(TemplateGenerator):
    """
    Test class without template name
    """
    template_loader = TemplateRenderer


def test_base_generator_get_output_filename_exception():
    """
    Ensure base class template_loader property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        TemplateGenerator().get_output_filename('/tmp')


def test_base_generator_template_loader_exception():
    """
    Ensure base class template_loader property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        TemplateGenerator().template_loader


def test_base_generator_template_renderer_exception():
    """
    Ensure base class template_renderer property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        NoTemplateRenderer().template_renderer


def test_base_generator_template_no_name_exception():
    """
    Ensure base class template_renderer property raises exception
    with renderer defined but no template name
    """
    with pytest.raises(DocumentGeneratorError):
        # pylint: disable=expression-not-assigned
        NoTemplateName().template_renderer


def test_base_generator_callback_exceptions():
    """
    Ensure base class template_renderer message callbacks raise exception
    """
    renderer = TemplateGenerator
    with pytest.raises(NotImplementedError):
        renderer.debug('test undefined debug method')
    with pytest.raises(NotImplementedError):
        renderer.error('test undefined error method')
    with pytest.raises(NotImplementedError):
        renderer.message('test undefined message method')
