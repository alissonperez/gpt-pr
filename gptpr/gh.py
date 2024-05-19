import os
from github import Github
from InquirerPy import inquirer
from gptpr.config import config, config_command_example, CONFIG_README_SECTION


def _get_gh_token():
    gh_token = config.get_user_config('GH_TOKEN')
    if not gh_token:
        gh_token = os.environ.get('GH_TOKEN')

    if not gh_token:
        print('Please set "gh_token" config. Just run:',
              config_command_example('gh_token', '[my gh token]'),
              'more about at', CONFIG_README_SECTION)
        exit(1)

    return gh_token


gh = Github(_get_gh_token())


def create_pr(pr_data, yield_confirmation):
    repo = gh.get_repo(
        f'{pr_data.branch_info.owner}/{pr_data.branch_info.repo}')

    pr_confirmation = yield_confirmation or inquirer.confirm(
        message="Create GitHub PR?",
        default=True).execute()

    if pr_confirmation:
        pr = repo.create_pull(title=pr_data.title, body=pr_data.body,
                              head=pr_data.branch_info.branch, base=pr_data.branch_info.base_branch)
        print("Pull request created successfully: ", pr.html_url)
    else:
        print('cancelling...')
