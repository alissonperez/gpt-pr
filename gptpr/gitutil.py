from dataclasses import dataclass
import os

from git import Repo
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


@dataclass
class BranchInfo:
    owner: str
    repo: str
    base_branch: str
    branch: str
    commits: list
    highlight_commits: list
    diff: str


@dataclass
class FileChange:
    file_path: str
    lines_added: int
    lines_removed: int

    @property
    def total_lines_changed(self):
        return self.lines_added + self.lines_removed

    @property
    def desc(self):
        return f'{self.file_path} (+{(self.lines_added)} -{self.lines_removed})'


def get_branch_info(base_branch, yield_confirmation):
    # Get current directory
    current_dir = os.getcwd()

    # Instantiate the repository
    repo = Repo(current_dir)

    # Check that the repository loaded correctly
    if not repo.bare:
        print(f'Repo at {repo} successfully loaded.')
    else:
        raise Exception('Could not load repository.')

    # Get the current branch
    current_branch = repo.active_branch

    # Make sure we are on a branch, not a detached HEAD
    if current_branch:
        print(f'Current branch is {current_branch}.')
    else:
        raise Exception('Not currently on any branch.')

    if not _branch_exists(repo, base_branch):
        raise Exception(f'Base branch {base_branch} does not exist.')

    owner, repo_name = _get_remote_info(repo)

    commits = _get_diff_messages_against_base_branch(repo, current_branch.name, base_branch)
    commits = _get_valid_commits(commits, yield_confirmation)

    if not commits:
        print('No commit changes detected.')
        return None

    highlight_commits = _get_highlight_commits(commits, yield_confirmation)

    return BranchInfo(
        owner=owner,
        repo=repo_name,
        base_branch=base_branch,
        branch=current_branch.name,
        commits=commits,
        highlight_commits=highlight_commits,
        diff=_get_diff_changes(repo, base_branch, current_branch.name, yield_confirmation)
    )


def _branch_exists(repo, branch_name):
    if branch_name in repo.branches:
        return True

    return False


def _get_diff_messages_against_base_branch(repo, branch, base_branch):
    # Get commit messages that are in the current branch but not in the base branch
    commits_diff = list(repo.iter_commits(f'{base_branch}..{branch}'))

    return [commit.message.strip('\n') for commit in commits_diff]


def _get_valid_commits(commits, yield_confirmation):
    if not commits:
        return commits

    options = [Choice(value=commit, name=commit) for commit in commits]

    commits_to_ignore = []
    if not yield_confirmation:
        commits_to_ignore = inquirer.checkbox(
            message='Pick commits that should be IGNORED (optional)\':',
            choices=options,
            instruction="(Press <space> to select, <enter> to confirm)",
        ).execute()

    return [commit for commit in commits if commit not in commits_to_ignore]


def _get_highlight_commits(commits, yield_confirmation):
    if yield_confirmation or len(commits) <= 1:
        return []

    options = [Choice(value=commit, name=commit) for commit in commits]

    highlight_commits = inquirer.checkbox(
        message='Pick commits to highlight in description (optional)\':',
        choices=options,
        instruction="(Press <space> to select, <enter> to confirm)",
    ).execute()

    return highlight_commits


def _get_remote_info(repo):
    for remote in repo.remotes:
        if remote.name != 'origin':
            continue

        remote_urls_joined = ','.join([str(url) for url in remote.urls])

        print(f'Remote name: {remote.name}, Urls: {remote_urls_joined}')

        for url in remote.urls:
            return _extract_owner_and_repo(url)

    raise Exception('Could not find origin remote.')


def _extract_owner_and_repo(repo_url):
    '''given git@github.com:grupo-sbf/product-aggregator.git return grupo-sbf and product-aggregator'''

    repo = repo_url.split(':')[1]
    owner, repo_info = repo.split('/')

    return owner, '.'.join(repo_info.split('.')[:-1])


def _get_diff_changes(repo, base_branch, branch, yield_confirmation):
    diff_changes = []

    stats = _get_stats(repo, base_branch, branch)
    files_to_ignore = _get_files_to_ignore(stats, yield_confirmation)

    for file_change in stats:
        if file_change.file_path in files_to_ignore:
            continue

        file_diff = repo.git.diff(base_branch, branch, '--', file_change.file_path)

        diff_changes.append(file_diff)

    return '\n'.join(diff_changes)


def _get_stats(repo, base_branch, branch):
    '''
    Get the stats of the difference between the current branch and the base branch
    '''

    # returns:
    # 4       0       README.md
    # 2       0       application/aggregator/aggregator.go
    # 0       257     go.sum
    diff_index = repo.git.diff(base_branch, branch, '--numstat')

    files_changed = []
    for line in diff_index.split('\n'):
        if not line:
            continue

        line = line.split('\t')
        files_changed.append(FileChange(
            file_path=line[2],
            lines_added=int(line[0]),
            lines_removed=int(line[1])
        ))

    return files_changed


def _get_files_to_ignore(stats, yield_confirmation):
    '''
    Get the files that should be ignored from the stats
    '''

    if yield_confirmation:
        return []

    options = [Choice(stats.file_path, name=stats.desc) for stats in stats]

    files_to_ignore = inquirer.checkbox(
        message="Select files to exclude (or press Enter to keep all)",
        choices=options,
        instruction="(Press <space> to select, <enter> to confirm)",
    ).execute()

    return files_to_ignore
