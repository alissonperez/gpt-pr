# GPT-PR

GPT-PR is an open-source command-line tool designed to streamline your GitHub workflow for opening PRs. Leveraging OpenAI's ChatGPT API, it automatically opens a GitHub Pull Request with a predefined description and title directly from your current project directory.

[![asciicast](https://asciinema.org/a/JIqhN0Du3bQiwXgsFJW37mMe3.svg)](https://asciinema.org/a/JIqhN0Du3bQiwXgsFJW37mMe3)

## Features

- Analyzes the diff changes of the current branch against the `main` branch.
- Provides an option to exclude certain file changes from PR generation (for instance, you can ignore a `package.lock` file with 5k lines changed).
- Incorporates commit messages into the process.

## Prerequisites

Before getting started, make sure you have the following installed:

- Python 3.7 or higher
- [Pipenv](https://pipenv.pypa.io/en/latest/)

## Installation

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

You can use GPT-PR within any git project directory.

Suppose you've cloned **this project** to `~/workplace/gpt-pr`, here's how you can use it:

```bash
$ GH_TOKEN=[fill-it] OPENAI_API_KEY=[fill-it] PIPENV_PIPFILE=~/workplace/gpt-pr/Pipfile pipenv run python ~/workplace/gpt-pr/main.py
```

Output:
![image](https://github.com/alissonperez/gpt-pr/assets/756802/5ad932e0-dd3c-4cce-b5e0-c88bd8210189)

## How to contribute?

Follow our [CONTRIBUTING](./CONTRIBUTING.md) guide.

## Roadmap

- [ ] Improve execution method, possibly through a shell script or at least an alias in bash rc files.
- [ ] Add unit tests.
- [ ] Fetch GitHub PR templates from the current project.
