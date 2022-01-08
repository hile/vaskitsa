"""
Visual Studio Code settings configuration section parser
"""

from sys_toolkit.configuration.json import JsonConfiguration

from .base import FilePatternList, VSCodeConfigurationSection


class ExcludePatterns(FilePatternList):
    """
    Loader for exclude patterns
    """
    __name__ = 'exclude'


class FileAssociations(FilePatternList):
    """
    Loader for file associations
    """
    __name__ = 'associations'


class Files(VSCodeConfigurationSection):
    """
    Visual Studio Code files configuration
    """
    __name__ = 'files'
    __section_loaders__ = {
        ExcludePatterns,
        FileAssociations,
    }


class Settings(JsonConfiguration, VSCodeConfigurationSection):
    """
    Visual Studio Code settings
    """
    __name__ = 'settings'
    __section_loaders__ = {
        Files,
    }
