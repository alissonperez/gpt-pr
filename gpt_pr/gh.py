import os
from github import Github
from InquirerPy import inquirer
from gpt_pr.config import config, config_command_example, CONFIG_README_SECTION


def _get_gh_token():
    gh_token = config.get_user_config("GH_TOKEN")
    if not gh_token:
        gh_token = os.environ.get("GH_TOKEN")

    if not gh_token:
        print(
            'Please set "gh_token" config. Just run:',
            config_command_example("gh_token", "[my gh token]"),
            "more about at",
            CONFIG_README_SECTION,
        )
        raise SystemExit(1)

    return gh_token


def _get_existing_pr(repo, branch_name):
    """Check if a PR already exists for the given branch."""
    pulls = repo.get_pulls(state="open")
    for pr in pulls:
        if pr.head.ref == branch_name:
            return pr
    return None


def _update_pr(pr, pr_data):
    """Update an existing PR."""
    try:
        pr.edit(title=pr_data.title, body=pr_data.create_body())
        print(f"Pull request #{pr.number} updated successfully.")
    except Exception as e:
        print(f"Failed to update the pull request: {e}")
        raise SystemExit(1)


def create_pr(pr_data, yield_confirmation, gh=None):
    if not gh:
        gh = Github(_get_gh_token())

    repo = gh.get_repo(f"{pr_data.branch_info.owner}/{pr_data.branch_info.repo}")

    existing_pr = _get_existing_pr(repo, pr_data.branch_info.branch)

    if existing_pr:
        message = f"A pull request for branch '{pr_data.branch_info.branch}' already exists. Do you want to update it?"
        update_confirmation = inquirer.confirm(
            message=message,
            default=True,
        ).execute()

        if update_confirmation:
            _update_pr(existing_pr, pr_data)
            return
        else:
            print("Cancelling...")
            return

    pr_confirmation = (
        yield_confirmation
        or inquirer.confirm(message="Create GitHub PR?", default=True).execute()
    )

    if pr_confirmation:
        pr = repo.create_pull(
            title=pr_data.title,
            body=pr_data.create_body(),
            head=pr_data.branch_info.branch,
            base=pr_data.branch_info.base_branch,
        )
        print("Pull request created successfully: ", pr.html_url)
    else:
        print("cancelling...")
