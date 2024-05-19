import fire
from InquirerPy import inquirer

from gptpr.gitutil import get_branch_info
from gptpr.gh import create_pr
from gptpr.prdata import get_pr_data
from gptpr.version import __version__
from gptpr.config import config, config_command_example, CONFIG_README_SECTION
from gptpr import consolecolor as cc
from gptpr.checkversion import check_for_updates


def run(base_branch='main', yield_confirmation=False, version=False):
    '''
    Create Pull Requests from current branch with base branch (default 'main' branch)
    '''

    if version:
        print('Current version:', __version__)
        return

    branch_info = get_branch_info(base_branch, yield_confirmation)

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

        if yield_confirmation:
            break

        generate_pr_data = not inquirer.confirm(
            message="Create PR with this? If 'no', let's try again...",
            default=True).execute()

        if generate_pr_data:
            print('Generating another PR data...')

    create_pr(pr_data, yield_confirmation)


def set_config(name, value):
    name = name.upper()
    config.set_user_config(name, value)
    config.persist()

    print('Config value', cc.bold(name), 'set to', cc.yellow(value))


def get_config(name):
    upper_name = name.upper()
    print('Config value', cc.bold(name), '=', cc.yellow(config.get_user_config(upper_name)))


def reset_config(name):
    upper_name = name.upper()
    config.reset_user_config(upper_name)
    print('Config value', cc.bold(name), '=', cc.yellow(config.get_user_config(upper_name)))


def print_config():
    print('Config values at', cc.yellow(config.get_filepath()))
    print('')
    print('To set values, just run:', cc.yellow(config_command_example('[config name]', '[value]')))
    print('More about at', cc.yellow(CONFIG_README_SECTION))
    print('')
    current_section = None
    for section, option, value in config.all_values():
        if current_section != section:
            print('')
            current_section = section

        print(f'[{cc.bold(section)}]', option, '=', cc.yellow(value))


def main():
    check_for_updates()

    fire.Fire(run)


def run_config():
    check_for_updates()

    fire.Fire({
        'set': set_config,
        'get': get_config,
        'print': print_config,
        'reset': reset_config
    })


if __name__ == '__main__':
    main()
