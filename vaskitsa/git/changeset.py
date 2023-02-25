"""
Change set in git repository
"""
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Union, TYPE_CHECKING

from ..exceptions import GitError

if TYPE_CHECKING:
    from .repository import GitRepository


class GitChangeState(Enum):
    """
    Enumerate the possible git item change states
    """
    UNMODIFIED = 'unmodified'
    ADDED = 'added'
    COPIED = 'copied'
    DELETED = 'deleted'
    MODIFIED = 'modified'
    RENAMED = 'renamed'
    UPDATED_UNMERGED = 'updated_unmerged'


class GitFilterState(Enum):
    """
    Filter states for git changes
    """
    ADDED = 'added'
    COPIED = 'copied'
    MODIFIED = 'modified'
    RENAMED = 'renamed'


CHANGE_STATE_MAP = {
    ' ': GitChangeState.UNMODIFIED,
    'A': GitChangeState.ADDED,
    'C': GitChangeState.COPIED,
    'D': GitChangeState.DELETED,
    'M': GitChangeState.MODIFIED,
    'R': GitChangeState.RENAMED,
    'U': GitChangeState.UPDATED_UNMERGED,
}
DEFAULT_FILTER_STATES = (
    GitFilterState.ADDED,
    GitFilterState.COPIED,
    GitFilterState.MODIFIED,
    GitFilterState.RENAMED,
)


class GitChangeSet:
    """
    Git change set between two revisions
    """
    repository: 'GitRepository'
    start_revision: str
    end_revision: str

    unmodified: List[Path]
    added: List[Path]
    copied: List[Path]
    deleted: List[Path]
    modified: List[Path]
    renamed: List[Path]
    updated_unmerged: List[Path]

    def __init__(self,
                 repository: 'GitRepository',
                 start_revision: str,
                 end_revision: str) -> None:
        self.repository = repository
        self.start_revision = start_revision
        self.end_revision = end_revision

        for status in list(GitChangeState):
            setattr(self, status.value, [])
        self.__load_change_set__()

    def __repr__(self) -> str:
        return f'{self.start_revision}..{self.end_revision}'

    def __load_change_set__(self) -> None:
        """
        Load changes in change set
        """
        lines = self.repository.run_git_command(
            'diff-tree',
            '--no-commit-id',
            '--name-status',
            '-r',
            f'{self.start_revision}..{self.end_revision}'
        )
        for line in lines:
            status, path = line.split('\t', 1)
            path = Path(path)
            try:
                status = CHANGE_STATE_MAP[status]
            except KeyError as error:
                raise GitError(f'Unexpected git change status {status}') from error
            getattr(self, status.value).append(path)

    def get_filter_states(self, values: Union[str, List[str]]) -> List[GitChangeState]:
        """
        Get a list of change state enums from string
        """
        if isinstance(values, str):
            values = values.split(',')
        states = []
        for value in values:
            try:
                states.append(GitChangeState(value))
            except ValueError as error:
                raise GitError(
                    f'Unexpected git change set filter state: {value}'
                ) from error
        return states

    def filter(self, value: Union[str, GitChangeState, Tuple[GitChangeState]] = DEFAULT_FILTER_STATES):
        """
        Filter changed files by list of filter states

        By default filters with DEFAULT_FILTER_STATES states
        """
        if isinstance(value, str):
            value = self.get_filter_states(value)
        if isinstance(value, GitChangeState):
            value = [value]

        filtered = []
        for state in value:
            filtered.extend(getattr(self, state.value))
        return filtered
