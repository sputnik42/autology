"""
Module that is responsible for syncing the data files across the storage modules. Initial version of this assumes that
git is the storage module, but there is not a reason why another storage implementation cannot be used in the future.

Current implementation assumes that git is initialized in the project directory, and has a remote named origin.
"""
import git
from autology.configuration import get_configuration_root
from autology import topics


# The current repository that all of the files will be stored/modified in.
_repo = None

# Whether the remote repository is available for access or not
_accessible = True


def register_plugin():
    """Initializes the git module for the directory that the configuration file is currently being stored in."""
    topics.Application.INITIALIZE.subscribe(_initialization)


def _initialization():
    global _repo, _accessible

    # If creating the git repository fails, then don't need to continue with this storage engine
    try:
        _repo = git.Repo(str(get_configuration_root()))
    except git.InvalidGitRepositoryError:
        return

    # Try to fetch from the origin remote in order to determine if the remote repository is active
    try:
        _repo.remotes.origin.fetch()
        _accessible = True
    except (git.GitCommandError, AttributeError):
        # Command error is raised when the remote is not accessible and attribute error is raised when the remote is not
        # defined.
        _accessible = False

    topics.Storage.FILE_ADDED.subscribe(_file_added)
    topics.Storage.FINISHED_MODIFICATIONS.subscribe(_finished_changes)
    topics.Storage.PULL_CHANGES.subscribe(_pull_changes)
    topics.Storage.PUSH_CHANGES.subscribe(_push_changes)


def _file_added(file):
    """Add file to the repository"""
    _repo.index.add([str(file)])


def _finished_changes(message):
    """Commit the changes to the repository."""
    _repo.index.commit(message)


def _pull_changes():
    """Pull changes from the repository and do a merge"""
    if _accessible:
        _repo.remotes.origin.pull('master')


def _push_changes():
    """Push changes to the repository."""
    if _accessible:
        _repo.remotes.origin.push('master')
