
from systematic_cli.configuration import ConfigurationSection


class HooksConfiguration(ConfigurationSection):
    """
    Configuration for running code analysis hooks
    """
    __name__ = 'hooks'
    __default_settings__ = {
        'flake8': {
            'flags': (
                '--verbose',
            ),
        },
        'pylint': {
            'flags': (
                '--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}',
            ),
        },
    }
