"""
Test exceptions from generator base class
"""
from pathlib import Path

import pytest

from vaskitsa.documentation.base import DocumentGeneratorError, TemplateGenerator
from vaskitsa.templates.template import TemplateRenderer

from .conftest import MOCK_TEMPLATE_NAME


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


# pylint: disable=abstract-method
class DummyTemplateGenerator(TemplateGenerator):
    """
    Test class with simple mocked mocked renderer
    """
    template_name = MOCK_TEMPLATE_NAME
    template_loader = TemplateRenderer


class EmptyTemplateGenerator(TemplateGenerator):
    """
    Test class with empty template from mocked mocked renderer
    """
    template_name = MOCK_TEMPLATE_NAME
    template_loader = TemplateRenderer

    def __init__(self, mock_template_directory: Path) -> None:
        self. mock_template_directory = mock_template_directory

    @property
    def template_directory(self) -> Path:
        """
        Return the mock data template directory
        """
        return self.mock_template_directory


def test_template_generator_empty_template_render(mock_template):
    """
    Test rendering of an empty template with minimal class on top of base
    """
    generator = EmptyTemplateGenerator(mock_template.parent)
    assert generator.template_directory == mock_template.parent
    output = generator.render_template()
    assert isinstance(output, str)
    assert output == ''


def test_template_generator_properties() -> None:
    """
    Test properties of a minimal template generator object
    """
    generator = DummyTemplateGenerator()
    assert generator.template_directory is None


def test_template_generator_get_output_filename_exception() -> None:
    """
    Ensure base class template_loader property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        TemplateGenerator().get_output_filename('/tmp')


def test_template_generator_template_loader_exception() -> None:
    """
    Ensure base class template_loader property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        TemplateGenerator().template_loader


def test_template_generator_template_renderer_exception() -> None:
    """
    Ensure base class template_renderer property raises error
    """
    with pytest.raises(NotImplementedError):
        # pylint: disable=expression-not-assigned
        NoTemplateRenderer().template_renderer


def test_template_generator_template_no_name_exception() -> None:
    """
    Ensure base class template_renderer property raises exception
    with renderer defined but no template name
    """
    with pytest.raises(DocumentGeneratorError):
        # pylint: disable=expression-not-assigned
        NoTemplateName().template_renderer


def test_template_generator_callback_exceptions() -> None:
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
