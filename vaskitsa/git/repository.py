"""
Git repository as python class
"""

from ..exceptions import GitError
from ..tree import RepositoryTree

from .changeset import GitChangeSet
from .commit import GitCommit
from .config import GitRepositoryConfig
from .utils import detect_git_repository_path, run_git_command


class GitRepository(RepositoryTree):
    """
    Abstraction of git repository checkout details for specified path
    """

    # pylint: disable=redefined-builtin
    def __new__(cls, path, name=None, create_missing=False, sorted=True, mode=None,
                excluded=list, configuration=None):
        git_repository_path = detect_git_repository_path(path)
        if git_repository_path is not None:
            path = git_repository_path

        if git_repository_path:
            cls.is_git_directory = True
            cls.__commits_detected__ = None
            cls.config = GitRepositoryConfig(git_repository_path)
        else:
            cls.is_git_directory = False
            cls.__commits_detected__ = False
            cls.config = None
        return super().__new__(cls, path, name, create_missing, sorted, mode, excluded, configuration)

    @property
    def has_commits(self):
        """
        Check for git repository with no commits

        This is used to avoid running git commands until there are commits
        to avoid script exceptions from self.run_git_command
        """
        if not self.is_git_directory:
            return False
        if self.__commits_detected__:
            return True
        lines = run_git_command(*['rev-list', '-n1', '--all'], cwd=self)
        if lines:
            self.__commits_detected__ = True
            return True
        return False

    @property
    def head(self):
        """
        Return git commit HEAD
        """
        self.validate()
        if not self.has_commits:
            raise GitError(f'Repository has no commits: {self}')
        return GitCommit(self)

    @property
    def reflog(self):
        """
        Return git reflog items as GitCommit objects
        """
        self.validate()
        lines = run_git_command(*['reflog', 'show', '--format=%H'], cwd=self)
        return [GitCommit(self, ref) for ref in lines]

    def validate(self):
        """
        Ensure directory exists and is a valid git repository
        """
        if not self.exists():
            raise GitError(f'No such directory: {self}')
        if not self.is_git_directory:
            raise GitError(f'Directory is not git repository: {self}')

    def run_git_command(self, *args):
        """
        Run a git command with specified arguments, returning stdout

        Command is always executed in the repository directory
        """
        self.validate()
        if not self.has_commits:
            raise GitError(f'Repository has no commits: {self}')
        return run_git_command(*args, cwd=self)

    def get_revision(self, characters=None):
        """
        Get git revision for current branch HEAD

        If characters is specified return first <characters> letters
        """
        value = self.head.commit_hash
        if characters is not None:
            return value[:characters]
        return value

    def get_commit(self, reference):
        """
        Get GitCommit object for specified git reference

        Reference is NOT validated before creating GitCommit object
        """
        self.validate()
        if not self.has_commits:
            raise GitError(f'Repository has no commits: {self}')
        return GitCommit(self, reference)

    def get_change_set(self, start_revision, end_revision):
        """
        Show changed files between two change

        If revision is not given compare to self.reference~1
        """
        self.validate()
        return GitChangeSet(self, start_revision, end_revision)
