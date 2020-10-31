"""
Unit tests for loading code repository
"""

import sys
from unittest.mock import patch

import pytest

from systematic_files.tree import Tree

from vaskitsa.documentation.base import DocumentGeneratorError
from vaskitsa.documentation.repository import RepositoryDocumentGenerator
from vaskitsa.templates.template import TemplateRenderer

from .constants import (
    EXCLUDED,
    NO_INIT_PATH,
    REPO_PACKAGE_PATH,
    REPO_ROOT_PATH,
    EXPECTED_MODULES,
    EXPECTED_TEST_MODULES,
)
from .validate import (
    validate_module,
    validate_file,
)


def validate_missing_message_callbacks(item):
    """
    Validate message callbacks on item with no connected message handlers
    """
    with patch.object(sys.stdout, 'write') as mock_stdout:
        with patch.object(sys.stderr, 'write') as mock_stderr:
            item.debug('test mock no debug message')
            item.error('test mock no error message')
            item.message('test mock no message')
    assert not mock_stdout.called
    assert not mock_stderr.called


def test_repository_load_self():
    """
    Load systematic-doc-generator source code as plain repository
    """
    repository = RepositoryDocumentGenerator(REPO_ROOT_PATH, excluded=EXCLUDED)
    print(repository.python_modules)
    assert len(repository.python_modules) == len(EXPECTED_MODULES)
    assert len(repository.python_test_modules) == len(EXPECTED_TEST_MODULES)

    docs = repository.default_output_directory
    assert docs.relative_to(repository)

    with pytest.raises(NotImplementedError):
        repository.get_output_filename('/tmp')

    assert len(repository.python_files) > 0
    for item in repository.python_files:
        validate_file(item, renderer=TemplateRenderer)

    with pytest.raises(NotImplementedError):
        repository.get_output_filename('/tmp')

    for module in repository.python_modules:
        validate_module(module, renderer=TemplateRenderer)

        with pytest.raises(NotImplementedError):
            module.get_output_filename('/tmp')

        for item in module.files:
            validate_file(item, renderer=TemplateRenderer)

            with pytest.raises(NotImplementedError):
                item.get_output_filename('/tmp')


def test_repository_load_no_init():
    """
    Test loading the test repository without init files in
    submodules
    """
    repository = RepositoryDocumentGenerator(NO_INIT_PATH)
    print(repository.python_modules)
    assert len(repository.python_modules) == 3
    assert len(repository.python_files) == 3

    for module in repository.python_modules:
        validate_module(module, renderer=TemplateRenderer)


def test_repository_load_package_directory():
    """
    Test loading package directory as repository
    """
    with pytest.raises(DocumentGeneratorError):
        RepositoryDocumentGenerator(REPO_PACKAGE_PATH)


def test_repository_generate_exception():
    """
    Test generating a bare repository documentation fails
    """
    repository = RepositoryDocumentGenerator(NO_INIT_PATH)
    docs_directory = repository.default_output_directory
    if docs_directory.exists():
        Tree(docs_directory).remove(recursive=True)

    with pytest.raises(NotImplementedError):
        repository.generate()

    with pytest.raises(NotImplementedError):
        repository.generate(docs_directory)

    assert not docs_directory.exists()
