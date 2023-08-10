import os
from github import Github
from InquirerPy import inquirer

GH_TOKEN = os.environ.get('GH_TOKEN')

if not GH_TOKEN:
    print("Please set GH_TOKEN environment variable")
    exit(1)

gh = Github(GH_TOKEN)


def create_pr(pr_data):
    repo = gh.get_repo(
        f'{pr_data.branch_info.owner}/{pr_data.branch_info.repo}')

    pr_confirmation = inquirer.confirm(message="Create GitHub PR?",
                                       default=True).execute()

    if pr_confirmation:
        pr = repo.create_pull(title=pr_data.title, body=pr_data.body,
                              head=pr_data.branch_info.branch, base='main')
        print("Pull request created successfully: ", pr.html_url)
    else:
        print('cancelling...')
