"""
Load documentation processors
"""

from pathlib import Path

from ..exceptions import DocumentGeneratorError
from .sphinx.repository import AutodocRepositoryGenerator

DEFAULT_PROCESSOR = 'sphinx'
PROCESSOR_TYPES = (
    'sphinx',
)


def get_processor(output_type, path, name=None, excluded=list):
    """
    Get repository processor for specified documentation type and path

    Raises DocumentGeneratorError for unknown output types
    """
    path = Path(path).absolute()
    if output_type == 'sphinx':
        return AutodocRepositoryGenerator(
            path,
            name=name,
            excluded=excluded,
        )
    raise DocumentGeneratorError(f'Invalid output type: {type}')
