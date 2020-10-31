
from pathlib import Path

from vaskitsa.documentation.file import FileDocumentGenerator
from vaskitsa.documentation.module import ModuleDocumentGenerator


def validate_relative_path(path, parent):
    """
    Ensure path is under parent path
    """
    assert isinstance(path, Path)
    assert isinstance(parent, Path)
    relative_path = path.relative_to(parent)
    assert str(relative_path) != ''


def validate_module(module, renderer):
    """
    Validate module details
    """
    print('validate module', module, type(module))
    assert isinstance(module, ModuleDocumentGenerator)
    assert len(module.files) > 0
    assert isinstance(module.__repr__(), str)
    assert isinstance(module.relative_directory, Path)
    assert module.template_loader == renderer

    has_index = module.joinpath('__init__.py').is_file()
    index = module.index
    if has_index:
        print('index', module, index, type(index))
        assert isinstance(index, FileDocumentGenerator)
        index_file = [item for item in module.files if item.is_index][0]
        assert index_file == index
    else:
        assert index is None


def validate_file(python_file, renderer):
    """
    Validate module details
    """
    assert isinstance(python_file.__repr__(), str)
    assert isinstance(python_file.name, str)
    assert python_file.template_loader == renderer

    assert isinstance(python_file.relative_path, Path)
    assert isinstance(python_file.relative_directory, Path)

    subpath = python_file.relative_path.relative_to(python_file.relative_directory)
    assert isinstance(subpath, Path)
