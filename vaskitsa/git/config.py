"""
Utility classes for git configuration
"""

from ..exceptions import GitError
from .utils import run_git_command

INCLUDEIF_CONDITIONS = (
    'gitdir',
    'gitdir/i',
    'onbranch',
)


def get_section_loader_class(name):
    """
    Get section loader class based on section name
    """
    if name.lower() in ('include', 'includeif'):
        return GitIncludeConfig
    return GitConfigSection


# pylint: disable=too-few-public-methods
class GitConfigSetting:
    """
    Setting in git configuration
    """
    def __init__(self, config, scope, key, value):
        """
        Git configuration settings with scope
        """
        self.config = config
        self.scope = scope
        self.key = key
        self.value = value

    def __repr__(self):
        return self.value


class GitConfigSection:
    """
    Git configuration section
    """
    def __init__(self, config, parent, name):
        self.__config__ = config
        self.__parent__ = parent
        self.__name__ = name

    def __repr__(self):
        return '.'.join(self.__section_path__)

    @property
    def __section_path__(self):
        """
        Path to this section from root
        """
        parts = [self.__name__]
        section = self.__parent__
        while section is not None:
            if section.__name__:
                parts.append(section.__name__)
            section = section.__parent__
        return list(reversed(parts))

    def __get_or_create_section__(self, path):
        """
        Get or create configuration section by path
        """
        assert isinstance(path, list)
        section = getattr(self, path[0], None)
        if section is None:
            name = path[0]
            loader_class = get_section_loader_class(name)
            section = loader_class(
                config=self.__config__,
                parent=self,
                name=name
            )
            setattr(self, section.__name__, section)

        if len(path) > 1:
            return section.__get_or_create_section__(path[1:])
        return section

    def set(self, attr, value):
        """
        Set value to configuration section
        """
        setattr(self, attr, value)


class GitIncludePattern:
    """
    Include path configuration
    """
    def __init__(self, condition, pattern=None):
        self.condition = condition
        self.pattern = pattern
        self.paths = []

    def __repr__(self):
        return f'{self.condition} {self.pattern}'

    def set(self, attr, value):
        """
        Set git include pattern path
        """
        if attr == 'path':
            self.paths.append(value)
        else:
            raise GitError(f'Unexpected attribute {attr} to GitIncludePattern class')


class GitIncludeCondition:
    """
    Git includeIf condition
    """
    def __init__(self, condition):
        self.__condition__ = condition
        self.patterns = []

    def __repr__(self):
        return self.__condition__

    def add_pattern(self, pattern):
        """
        Add pattern to condition, returns created GitIncludePattern
        """
        pattern = GitIncludePattern(self, pattern)
        self.patterns.append(pattern)
        return pattern


class GitIncludeConfig(GitConfigSection):
    """
    Git configuration section for include and includeif settings
    """

    def __init__(self, config, parent, name):
        super().__init__(config, parent, name)
        self.paths = []

    @staticmethod
    def __parse_include__(path):
        """
        Parse include or includeif attribute
        """
        if ':' in path:
            try:
                condition, pattern = path.split(':', 1)
                if condition not in INCLUDEIF_CONDITIONS:
                    raise GitError(f'Unsupported includeIf condition: {condition}')
                return condition, pattern
            except ValueError as error:
                raise GitError(f'Unsupported includeIf config: {path}') from error
        raise GitError(f'Error parsing include {path}')

    def __get_or_create_section__(self, path):
        """
        Get or create incclude path configuration
        """
        condition, pattern = self.__parse_include__(path[0])
        if getattr(self, condition, None) is None:
            setattr(self, condition, GitIncludeCondition(condition))
        condition_config = getattr(self, condition)
        return condition_config.add_pattern(pattern)

    def set(self, attr, value):
        """
        Set GitIncludeConfig section setting
        """
        if attr == 'path':
            return self.paths.append(value)
        return super().set(attr, value)


# pylint: disable=too-few-public-methods
class GitConfig(GitConfigSection):
    """
    Git configuration handler base class
    """
    def __init__(self):
        super().__init__(config=self, parent=None, name='')

    @staticmethod
    def run_git_command(*args, **kwargs):
        """
        Run 'git config' command with arguments
        """
        args = list(args)
        if args[0] != 'config':
            args = ['config'] + args
        return run_git_command(*args, cwd=kwargs.get('cwd', None))

    def __load_config__(self):
        """
        Load configuration
        """
        return self.run_git_command('--show-scope', '--list')

    def load(self):
        """
        Load git configuration
        """
        for line in self.__load_config__():
            scope, item = line.split(None, 1)
            key, value = item.split('=', 1)
            setting = GitConfigSetting(self, scope, key, value)
            path = setting.key.split('.')[:-1]
            name = setting.key.split('.')[-1]
            section = self.__get_or_create_section__(path)
            section.set(name, setting)


class GitRepositoryConfig(GitConfig):
    """
    Git configuration for a git repository
    """
    def __init__(self, repository_path):
        super().__init__()
        self.repository_path = repository_path

    def __repr__(self):
        return f'{self.repository_path} config'

    def __load_config__(self):
        """
        Load configuration
        """
        return self.run_git_command(
            '--show-scope', '--list',
            cwd=self.repository_path
        )
