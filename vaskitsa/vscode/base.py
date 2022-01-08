
from sys_toolkit.configuration.base import ConfigurationSection


class VSCodeConfigurationSection(ConfigurationSection):
    """
    Visual Code configuration section
    """

    @property
    def __dict_loader__(self):
        """
        Return loader for dict items
        """
        return VSCodeConfigurationSection


class FilePatternList(VSCodeConfigurationSection):
    """
    Visual Studio Code file pattern list
    """
    def __init__(self, data=dict, parent=None, debug_enabled=False, silent=False):
        self.patterns = {}
        super().__init__(data, parent, debug_enabled, silent)

    def set(self, attr, value):
        self.patterns[attr] = value

    def __load_dictionary__(self, data):
        for key, value in data.items():
            self.set(key, value)
