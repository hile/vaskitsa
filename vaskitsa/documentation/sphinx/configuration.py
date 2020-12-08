
from cli_toolkit.configuration import ConfigurationSection

DEFAULT_SPHINX_AUTODOC_PATH = 'docs/code'
DEFAULT_SPHINX_TOCTREE_DEPTH = 2
DEFAULT_SPHINX_AUTOMODULE_FLAGS = (
    'members',
    'undoc-members',
    'inherited-members',
)


class SphinxConfiguration(ConfigurationSection):
    """
    Configuration for sphinx automodule documentation generator
    """
    __name__ = 'sphinx'
    __default_settings__ = {
        'document_path': DEFAULT_SPHINX_AUTODOC_PATH,
        'template_directory': None,
        'templates': {
            'repository': 'repository_index',
            'module': 'module_index',
            'file': 'automodule',
        },
        'repository_index_max_depth': DEFAULT_SPHINX_TOCTREE_DEPTH,
        'module_index_max_depth': DEFAULT_SPHINX_TOCTREE_DEPTH,
        'automodule_flags': DEFAULT_SPHINX_AUTOMODULE_FLAGS,
    }
