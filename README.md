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

## Authentication & API Keys

### Setting up GitHub Token (`GH_TOKEN`)

To authenticate with GitHub, generate and export a GitHub Personal Access Token:

1. Navigate to [GitHub's Personal Access Token page](https://github.com/settings/tokens).
2. Click "Generate new token."
3. Provide a description and select the required permissions `repo` for the token.
4. Click "Generate token" at the bottom of the page.
5. Copy the generated token.
6. Export it as an environment variable:

```bash
export GH_TOKEN=your_generated_token_here
```

### Setting up OpenAI API Key (`OPENAI_API_KEY`)

This project needs to interact with the ChatGPT API to generate the pull request description. So, you need to generate and export an OpenAI API Key:

1. Navigate to [OpenAI's API Key page](https://platform.openai.com/signup).
2. If you don't have an account, sign up and log in.
3. Go to the API Keys section and click "Create new key."
4. Provide a description and click "Create."
5. Copy the generated API key.
6. Export it as an environment variable:

```bash
export OPENAI_API_KEY=your_generated_api_key_here
```

## Usage

After exporting api keys as environment variables ([Authentication & API Keys](#authentication--api-keys)), you can use GPT-PR within any git project directory. Suppose you've cloned **this project** to `~/workplace/gpt-pr`, here's how you can use it:

```bash
$ PIPENV_PIPFILE=~/workplace/gpt-pr/Pipfile pipenv run python ~/workplace/gpt-pr/main.py
```

Output:
![image](https://github.com/alissonperez/gpt-pr/assets/756802/5ad932e0-dd3c-4cce-b5e0-c88bd8210189)

## How to contribute?

Follow our [CONTRIBUTING](./CONTRIBUTING.md) guide.

## Roadmap

- [ ] Improve execution method, possibly through a shell script or at least an alias in bash rc files.
- [ ] Add unit tests.
- [ ] Fetch GitHub PR templates from the current project.
