from pprint import pprint
import os
from github import Github
from InquirerPy import inquirer

# using an access token
gh = Github(os.environ['GH_TOKEN'])

def create_pr(pr_data):
    repo = gh.get_repo(f'{pr_data.branch_info.owner}/{pr_data.branch_info.repo}')

    # Then play with your Github objects:
    pprint(dict(title=pr_data.title, body=pr_data.body, head=pr_data.branch_info.branch, base='main'))

    pr_confirmation = inquirer.confirm(message="Create github PR?", default=False).execute()

    if pr_confirmation:
        pr = repo.create_pull(title=pr_data.title, body=pr_data.body, head=pr_data.branch_info.branch, base='main')
        print("Pull request created successfully: ", pr.html_url)
    else:
        print('cancelling...')
