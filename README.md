# GPT-PR

GPT-PR is an open source command line designed to streamline your GitHub workflow. With GPT-PR, you can get the current directory's commit changes, generate a PR template, and automatically open a GitHub PR with a description and title, all powered by OpenAI's ChatGPT API.

## Features
- Consider diff changes of current branch against `main` branch.
- Possibility to remove files changed to be considered to generate PR data. (useful to ignore that `package.lock` with 5k lines changed).
- Consider commit messages

## Installation

Before you start, ensure you have these prerequisites installed:
- Python 3.7 or higher
- Pipenv

Once you've confirmed that you have the prerequisites, follow these steps:

1. Clone the repository:

```shell
git clone https://github.com/alissonperez/gpt-pr.git
cd gpt-pr
```

2. Install the dependencies with Pipenv:

```shell
pipenv install
```

## Usage

Within a project directory (this could be any directory where you're currently working), simply run the command:

For instance, let's suppose **this** project was cloned to `~/workplace/gpt-pr`:

```bash
$ GH_TOKEN=[fill-it] OPENAI_API_KEY=[fill-it] PIPENV_PIPFILE=~/workplace/gpt-pr/Pipfile pipenv run python ~/workplace/gpt-pr/main.py
```

Output:
![image](https://github.com/alissonperez/gpt-pr/assets/756802/5ad932e0-dd3c-4cce-b5e0-c88bd8210189)

## TOOD

- [ ] improve how to run it, maybe with a shell script or at least an alias in bash rc files.
- [ ] add tests.
- [ ] Get github pr template from current project.
