"""
Unit tests for loading code package
"""

from pathlib import Path

from jinja2 import Environment, Template

from vaskitsa.documentation.loader import get_processor
from vaskitsa.documentation.sphinx.package import AutodocPackageGenerator
from vaskitsa.documentation.renderers.sphinx import SphinxTemplateRenderer

from .constants import EXPECTED_MODULES, EXCLUDED, REPO_ROOT_PATH
from .validate import (
    validate_file,
    validate_module,
    validate_relative_path,
)


def validate_sphinx_flags(flags):
    """
    Validate sphinx flag values
    """
    assert isinstance(flags, list)
    for flag in flags:
        assert isinstance(flag, str)
        assert flag[0] == ':' and flag[-1] == ':'


def validate_file_import_paths(paths):
    """
    Validate python module sphinx import path list
    """
    assert isinstance(paths, list)


def validate_renderer(renderer):
    """
    Validate template renderer is valid
    """
    assert isinstance(renderer.__repr__(), str)
    assert isinstance(renderer.environment, Environment)
    assert isinstance(renderer.template, Template)


def test_repository_load_sphinx_self():
    """
    Test loading repository source code as sphinx generator
    """
    output_prefix = Path('/tmp/doctest')

    repository = get_processor('sphinx', REPO_ROOT_PATH, excluded=EXCLUDED)
    assert isinstance(repository, AutodocPackageGenerator)
    assert isinstance(repository.__repr__(), str)
    assert len(repository.python_modules) == len(EXPECTED_MODULES)
    validate_relative_path(
        repository.get_output_filename(output_prefix),
        output_prefix
    )

    for module in repository.python_modules:
        assert isinstance(module.caption, str)
        validate_module(module, renderer=SphinxTemplateRenderer)
        validate_relative_path(
            module.get_output_filename(output_prefix),
            output_prefix
        )
        validate_file_import_paths(module.file_import_paths)
        validate_renderer(module.template_renderer)

        for item in module.files:
            validate_file(item, renderer=SphinxTemplateRenderer)
            validate_sphinx_flags(item.automodule_flags)
            validate_relative_path(
                item.get_output_filename(output_prefix),
                output_prefix
            )
            validate_renderer(item.template_renderer)
