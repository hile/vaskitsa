"""
Various errors raised by vaskitsa code repository module
"""


class DocumentGeneratorError(Exception):
    """
    Errors from document generators
    """


class GitError(Exception):
    """
    Errors from git commands
    """


class PythonSetupError(Exception):
    """
    Exceptions processing setup.py an setup.cfg files
    """


class RepositoryConfigurationError(Exception):
    """
    Errors parsing repository configuration
    """
