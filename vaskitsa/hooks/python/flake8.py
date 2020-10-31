
from ..hook import CLIHook

COMMAND = (
    'flake8',
)


class Flake8(CLIHook):
    """
    Run pylint
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, COMMAND, **kwargs)
