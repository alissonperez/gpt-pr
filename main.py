from InquirerPy import inquirer

from gitutil import get_branch_info
from gh import create_pr
from prdata import get_pr_data

branch_info = get_branch_info()

pr_data = None
generate_pr_data = True
while generate_pr_data:
    pr_data = get_pr_data(branch_info)
    print('')
    print('#########################################')
    print(pr_data.to_display())
    print('#########################################')
    print('')
    generate_pr_data = not inquirer.confirm(message="Create PR with this? If 'no', let's try again...", default=True).execute()
    if generate_pr_data:
        print('Generating another PR data...')

create_pr(pr_data)
