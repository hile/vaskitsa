
from cli_toolkit.configuration import ConfigurationSection

DEFAULT_DOCUMENTS_PATH = 'docs'


class DocumentationConfiguration(ConfigurationSection):
    """
    Common documentation settings
    """
    __name__ = 'documentation'
    __default_settings__ = {
        'document_path': DEFAULT_DOCUMENTS_PATH,
    }
