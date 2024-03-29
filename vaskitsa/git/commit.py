"""
Git commit in a repository
"""
import json
from datetime import datetime
from typing import List, TYPE_CHECKING
from zoneinfo import ZoneInfo

from sys_toolkit.encoders import DateTimeEncoder

if TYPE_CHECKING:
    from .changeset import GitChangeSet
    from .repository import GitRepository

DEFAULT_JSON_INDENT = 2
DEFAULT_REVISION = 'HEAD'
UTC_TIMEZONE = ZoneInfo('UTC')


class GitCommit:
    """
    Git commit for repository
    """
    repository: 'GitRepository'
    revision: str

    def __init__(self, repository: 'GitRepository', revision: str = DEFAULT_REVISION):
        self.repository = repository
        self.revision = revision

    def __repr__(self) -> str:
        return self.revision

    def __show_formatted__(self, format_string) -> str:
        """
        Run git show with --no-notes --no-patch and specified format string
        """
        return self.repository.run_git_command(
            'show',
            '--no-notes',
            '--no-patch',
            f'--format={format_string}',
            self.revision
        )

    @property
    def properties(self) -> List[str]:
        """
        Return all available properties
        """
        skipped = ('repository', 'properties',)
        props = []
        for prop in dir(self):
            if prop.startswith('_') or prop in skipped:
                continue
            attr = getattr(self.__class__, prop, None)
            if attr is not None and callable(attr):
                continue
            props.append(prop)
        return props

    @property
    def commit_hash(self) -> str:
        """
        Return git commit hash
        """
        return self.__show_formatted__('%H')[0]

    @property
    def tree_hash(self) -> str:
        """
        Return git commit hash
        """
        return self.__show_formatted__('%T')[0]

    @property
    def author_email(self) -> str:
        """
        Return git commit author email
        """
        return self.__show_formatted__('%ae')[0]

    @property
    def author_name(self) -> str:
        """
        Return git commit author name
        """
        return self.__show_formatted__('%an')[0]

    @property
    def author_timestamp(self) -> int:
        """
        Return git commit author timestamp
        """
        return int(self.__show_formatted__('%at')[0])

    @property
    def author_date(self) -> datetime:
        """
        Return git commit author timestamp as datetime in UTC
        """
        return datetime.fromtimestamp(self.author_timestamp).astimezone(UTC_TIMEZONE)

    @property
    def commit_message(self) -> str:
        """
        Return git commit message as list of lines
        """
        return self.__show_formatted__('%s')

    @property
    def commit_timestamp(self) -> int:
        """
        Return commit timestamp
        """
        return int(self.__show_formatted__('%ct')[0])

    @property
    def commit_date(self) -> datetime:
        """
        Return commit timestamp as datetime in UTC
        """
        return datetime.fromtimestamp(self.commit_timestamp).astimezone(UTC_TIMEZONE)

    @property
    def ref_names(self) -> List[str]:
        """
        Return commit ref names
        """
        return self.__show_formatted__('%D')[0].split(', ')

    @property
    def signing_key(self) -> str:
        """
        Return signing key for GPG signed commit
        """
        return self.__show_formatted__('%GK')[0]

    @property
    def signing_key_fingerprint(self) -> str:
        """
        Return signing key fingerprint for GPG signed commit
        """
        return self.__show_formatted__('%GF')[0]

    @property
    def signing_primary_key_fingerprint(self) -> str:
        """
        Return primary signing key fingerprint for GPG signed commit
        """
        return self.__show_formatted__('%GP')[0]

    @property
    def signing_key_trust(self) -> str:
        """
        Return primary signing key fingerprint for GPG signed commit
        """
        return self.__show_formatted__('%GT')[0]

    @property
    def signing_signer_name(self) -> str:
        """
        Return author name for GPG signed commit
        """
        return self.__show_formatted__('%GS')[0]

    def get_change_set(self, revision: str = None) -> 'GitChangeSet':
        """
        Show changed files between this against specified revision

        If revision is not given compare to self.revision~1
        """
        if revision is None:
            revision = f'{self.revision}~1'
        return self.repository.get_change_set(self.revision, revision)

    def to_dict(self) -> dict:
        """
        Return all properties as dictionary

        This method runs one git command for each property
        """
        items = {}
        for prop in self.properties:
            items[prop] = getattr(self, prop)
        return items

    def to_json(self, indent: int = DEFAULT_JSON_INDENT) -> str:
        """
        Return git commit details rendered as JSON
        """
        return json.dumps(self.to_dict(), indent=indent, cls=DateTimeEncoder)
