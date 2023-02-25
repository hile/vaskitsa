"""
Vaskista code documentation generator configuration
"""
from sys_toolkit.configuration.base import ConfigurationSection

DEFAULT_DOCUMENTS_PATH = 'docs'


class DocumentationConfiguration(ConfigurationSection):
    """
    Common documentation settings
    """
    __name__ = 'documentation'
    __default_settings__ = {
        'document_path': DEFAULT_DOCUMENTS_PATH,
    }
