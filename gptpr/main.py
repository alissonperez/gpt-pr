from InquirerPy import inquirer

from gptpr.gitutil import get_branch_info
from gptpr.gh import create_pr
from gptpr.prdata import get_pr_data


def main():
    branch_info = get_branch_info()

    if not branch_info:
        exit(0)

    pr_data = None
    generate_pr_data = True
    while generate_pr_data:
        pr_data = get_pr_data(branch_info)
        print('')
        print('#########################################')
        print(pr_data.to_display())
        print('#########################################')
        print('')
        generate_pr_data = not inquirer.confirm(
            message="Create PR with this? If 'no', let's try again...",
            default=True).execute()
        if generate_pr_data:
            print('Generating another PR data...')

    create_pr(pr_data)


if __name__ == '__main__':
    main()
