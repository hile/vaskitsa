"""
Load documentation processors
"""
from pathlib import Path
from typing import List

from ..exceptions import DocumentGeneratorError
from .sphinx.package import AutodocPackageGenerator

DEFAULT_PROCESSOR = 'sphinx'
PROCESSOR_TYPES = (
    'sphinx',
)


def get_processor(
        output_type: str,
        path: Path,
        name: str = None,
        excluded: List[str] = list
     ) -> AutodocPackageGenerator:
    """
    Get package processor for specified documentation type and path

    Raises DocumentGeneratorError for unknown output types
    """
    path = Path(path).absolute()
    if output_type == 'sphinx':
        return AutodocPackageGenerator(
            path,
            name=name,
            excluded=excluded,
        )
    raise DocumentGeneratorError(f'Invalid output type: {type}')
