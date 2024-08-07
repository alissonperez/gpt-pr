# GPT-PR

GPT-PR is an open-source command-line tool designed to streamline your GitHub workflow for opening PRs. Leveraging OpenAI's ChatGPT API, it automatically opens a GitHub Pull Request with a predefined description and title directly from your current project directory.

[![asciicast](https://asciinema.org/a/u0PwZlNjAGZcdXPPrjf84wj2A.svg)](https://asciinema.org/a/u0PwZlNjAGZcdXPPrjf84wj2A)

## Quick Start

For a more detailed explanation, see [Installation](#installation) and [Configuration](#configuration).

### 1. Installation

```bash
pip install -U gpt-pr
```

If you don't have the `pip` command available, follow [these instructions](https://pip.pypa.io/en/stable/installation/) to install it on different platforms.

### 2. Fill OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys) and generate a new key.
2. Run the following command to fill your key in GPT-PR (it will be stored in `~/.gpt-pr.ini`):

```bash
gpt-pr-config set openai_api_key MY-API-KEY-VALUE
```

### 3. Generate a GitHub GH Token to Open PRs

1. Go to [GitHub Settings](https://github.com/settings/tokens), choose `Generate new token (classic)`, and select all permissions under `repo` (full control of private repositories).
2. Run the following command to fill your GH token (it will also be stored in `~/.gpt-pr.ini`):

```bash
gpt-pr-config set gh_token MY-GH-TOKEN-VALUE
```

### 4. Ready to NEVER WRITE A PR AGAIN

1. Make your changes, commit them, and push to origin (important!).
2. Run the following command in your project directory:

```bash
gpt-pr
```

3. Answer the questions. At the end, you'll receive the URL of a freshly opened PR.

## Contributing and Feedback

We welcome your contributions and feedback to help improve GPT-PR! Here’s how you can get involved:

### Open Issues

- **Feature Requests**: Have an idea for a new feature? We’d love to hear it! Open an issue to request new features or enhancements.
- **Bug Reports**: Encountered a bug? Let us know by opening an issue with detailed information so we can fix it.
- **General Feedback**: Any other suggestions or feedback? Feel free to share your thoughts.

To open an issue, go to the [Issues](https://github.com/your-repo/gpt-pr/issues) section of our GitHub repository. Your contributions are very welcome and highly appreciated!

More details about it at our [CONTRIBUTING](./CONTRIBUTING.md) guide.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How to Contribute](#how-to-contribute)
- [Roadmap](#roadmap)

## Features

- Analyzes the diff changes of the current branch against the `main` branch.
- Provides an option to exclude certain file changes from PR generation (for instance, you can ignore a `package.lock` file with 5k lines changed).
- Incorporates commit messages into the process.

## Prerequisites

Before getting started, make sure you have the following installed:

- Python 3.7 or higher
- [Pipenv](https://pipenv.pypa.io/en/latest/)

## Installation

You can install and use GPT-PR in one of two ways. Choose the option that best suits your needs.

### Option 1: Using `pip install` (Recommended)

1. Install OR Update the package:

```bash
pip install -U gpt-pr
```

2. Setup API keys for GitHub and OpenAI, take a look at [Configuration](#configuration).

3. Inside the Git repository you are working on, ensure you have pushed your branch to origin, then run:

```bash
gpt-pr --help
```

### Option 2: Cloning the code (NOT recommended)

1. Clone the repository:

```bash
git clone https://github.com/alissonperez/gpt-pr.git
```

2. Navigate to the project directory and install dependencies:

```bash
cd gpt-pr
pipenv install
```

After setting up API keys ([Configuration](#configuration)), you can use GPT-PR within any git project directory. Suppose you've cloned **this project** to `~/workplace/gpt-pr`, here's how you can use it:

```bash
PYTHONPATH=~/workplace/gpt-pr/gpt-pr \
PIPENV_PIPFILE=~/workplace/gpt-pr/Pipfile \
pipenv run python ~/workplace/gpt-pr/gptpr/main.py --help
```

## Configuration

### See all configs available

To print all default configs and what is being used, just run:

```bash
gpt-pr-config print
```

### Setting up GitHub Token (`GH_TOKEN`)

GPT-PR tool will look for a `GH_TOKEN` in current shell env var OR in gpt-pr config file (at `~/.gpt-pr.ini`).

To authenticate with GitHub, generate and export a GitHub Personal Access Token:

1. Navigate to [GitHub's Personal Access Token page](https://github.com/settings/tokens).
2. Click "Generate new token."
3. Provide a description and select the required permissions `repo` for the token.
4. Click "Generate token" at the bottom of the page.
5. Copy the generated token.
6. Set `gh_token` config running (supposing your gh token is `ghp_4Mb1QEr9gY5e8Lk3tN1KjPzX7W9z2V4HtJ2b`):

```bash
gpt-pr-config set gh_token ghp_4Mb1QEr9gY5e8Lk3tN1KjPzX7W9z2V4HtJ2b
```

Or just export it as an environment variable in your shell initializer:

```bash
export GH_TOKEN=your_generated_token_here
```

### Setting up OpenAI API Key (`OPENAI_API_KEY`)

GPT-PR tool will look for a `OPENAI_API_KEY` env var in current shell OR in gpt-pr config file (at `~/.gpt-pr.ini`).

This project needs to interact with the ChatGPT API to generate the pull request description. So, you need to generate and export an OpenAI API Key:

1. Navigate to [OpenAI's API Key page](https://platform.openai.com/signup).
2. If you don't have an account, sign up and log in.
3. Go to the API Keys section and click "Create new key."
4. Provide a description and click "Create."
5. Copy the generated API key.
6. Set `openai_api_key` config running (supposing your openai_api_key is `QEr9gY5e8Lk3tN1KjPzX7W9z2V4Ht`):

```bash
gpt-pr-config set openai_api_key QEr9gY5e8Lk3tN1KjPzX7W9z2V4Ht
```

Or just export it as an environment variable in your shell initializer:

```bash
export OPENAI_API_KEY=your_generated_api_key_here
```

### Setting Max Input LLM Tokens

You can adjust the maximum number of input tokens allowed when calling the LLM model by modifying the corresponding setting.

For example, to change the maximum to 20,000 tokens, use the following command:

```bash
gpt-pr-config set input_max_tokens 20000
```

### Change OpenAI model

To change OpenAI model, just run:

```bash
gpt-pr-config set openai_model gpt-4o-mini
```

> Obs.: `gpt-4o-mini` already is the default model of the project

To see a full list of available models, access [OpenAI Models Documentation](https://platform.openai.com/docs/models)

### GPT-PR Library Signature in PRs

To help other developers recognize and understand the use of the GPT-PR library in generating pull requests, we have included an optional signature feature. By default, this feature is enabled and appends the text "Generated by GPT-PR" at the end of each pull request. This transparency fosters better collaboration and awareness among team members about the tools being utilized in the development process.

If you prefer to disable this feature, simply run the following command:

```bash
gpt-pr-config set add_tool_signature false
```

### Reset config

To reset any config to default value, just run:

```bash
gpt-pr-config reset config_name
```

Example:

```bash
gpt-pr-config reset openai_model
```

## Usage

### Generating Github Pull Requests

To create a Pull request from your current branch commits to merge with `main` branch, just run:

```
gpt-pr
```

If you would like to compare with other base branch that is not `main`, just use `-b` param:

```
gpt-pr -b my-other-branch
```

### Usage help

To show help commands:

```
gpt-pr -h
```

Output:
![image](https://github.com/alissonperez/gpt-pr/assets/756802/cc6c0ca4-5759-44ce-ad35-e4e7305b3875)

## Roadmap

- [x] Improve execution method, possibly through a shell script or at least an alias in bash rc files.
  - Change to use with pip installation and console_scripts entry point.
- [x] Fetch GitHub PR templates from the current project.
- [ ] Add configuration to set which LLM and model should be used (OpenAI GPT, Mistral, etc...)
- [ ] Add unit tests.
