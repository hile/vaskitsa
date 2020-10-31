
from pathlib import Path

from ..exceptions import GitError

CHANGE_STATES = {
    ' ': 'unmodified',
    'A': 'added',
    'C': 'copied',
    'D': 'deleted',
    'M': 'modified',
    'R': 'renamed',
    'U': 'updated_unmerged',
}
DEFAULT_FILTER_STATES = (
    'added',
    'copied',
    'modified',
    'renamed',
)


class GitChangeSet:
    """
    Git change set between two revisions
    """
    def __init__(self, repository, start_revision, end_revision):
        self.repository = repository
        self.start_revision = start_revision
        self.end_revision = end_revision

        for status in CHANGE_STATES.values():
            setattr(self, status, [])
        self.__load_change_set__()

    def __repr__(self):
        return f'{self.start_revision}..{self.end_revision}'

    def __load_change_set__(self):
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
                status = CHANGE_STATES[status]
            except KeyError:
                GitError(f'Unexpected git change status {status}')
            getattr(self, status).append(path)

    def filter(self, states=DEFAULT_FILTER_STATES):
        """
        Filter changed files by list of filter states

        By default filters with DEFAULT_FILTER_STATES states
        """
        if isinstance(states, str):
            states = states.split(',')
        filtered = []
        for state in states:
            if state not in CHANGE_STATES.values():
                raise GitError(f'Invalid change state {state}')
            filtered.extend(getattr(self, state))
        return filtered
