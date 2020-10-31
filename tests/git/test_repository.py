

from vaskitsa.git.repository import GitRepository
from ..constants import REPO_ROOT_PATH


def test_git_repository_load_project():
    """
    Test loading git repository for vaskitsa
    """
    git = GitRepository(REPO_ROOT_PATH)
    assert git == REPO_ROOT_PATH
