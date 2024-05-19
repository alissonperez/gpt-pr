from dataclasses import dataclass
import json
import os
from openai import OpenAI

from gptpr.gitutil import BranchInfo
from gptpr.config import config
import gptpr.consolecolor as cc

TOKENIZER_RATIO = 4
MAX_TOKENS = 6000

DEFAULT_PR_TEMPLATE = ('### Ref. [Link]\n\n## What was done?\n[Fill here]\n\n'
                       '## How was it done?\n[Fill here]\n\n'
                       '## How was it tested?\n[Fill here with test information from diff content or commits]')


def _get_pr_template():
    pr_template = DEFAULT_PR_TEMPLATE

    try:
        github_dir = os.path.join(os.getcwd(), '.github')
        github_files = os.listdir(github_dir)
        pr_template_file = [f for f in github_files if f.lower().startswith('pull_request_template')][0]
        pr_template_file_path = os.path.join(github_dir, pr_template_file)

        with open(pr_template_file_path, 'r') as f:
            local_pr_template = f.read()

            if local_pr_template.strip() != '':
                print('Found PR template at:', pr_template_file_path)
                pr_template = local_pr_template
            else:
                print('Empty PR template at:', pr_template_file_path, 'using default template.')
    except Exception:
        print('PR template not found in .github dir. Using default template.')

    return pr_template


def _get_open_ai_key():
    api_key = config.get_user_config('OPENAI_API_KEY')

    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY')

    if not api_key:
        print('Please set "openai_api_key" config, just run:',
              cc.yellow('gpt-pr-config set openai_api_key [open ai key]'))
        exit(1)

    return api_key


@dataclass
class PrData():
    branch_info: BranchInfo
    title: str
    body: str

    def to_display(self):
        return '\n'.join([
            f'{cc.bold("Repository")}: {cc.yellow(self.branch_info.owner)}/{cc.yellow(self.branch_info.repo)}',
            f'{cc.bold("Title")}: {cc.yellow(self.title)}',
            f'{cc.bold("Branch name")}: {cc.yellow(self.branch_info.branch)}',
            f'{cc.bold("Base branch")}: {cc.yellow(self.branch_info.base_branch)}',
            f'{cc.bold("PR Description")}:\n{self.body}',
        ])


functions = [
    {
        "name": "create_pr",
        "description": "Creates a Github Pull Request",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "PR title, following angular commit convention"
                },
                "description": {
                    "type": "string",
                    "description": "PR description"
                },
            },
            "required": ["title", "description"]
        },
    }
]


def get_pr_data(branch_info):
    system_content = ('You are a development assistant designed to craft Git pull requests '
                      'by incorporating information from main and secondary commits, diff changes, '
                      'and adhering to a provided PR template. Your output includes a complete PR '
                      'template with all necessary details and a suitable PR title. In the '
                      'PR description, detail the work accomplished, the methodology employed, '
                      'including testing procedures, and list significant changes in bullet points '
                      'if they are extensive. Avoid incorporating diff content directly into '
                      'the PR description.')

    messages = [
        {'role': 'system', 'content': system_content},
    ]

    if len(branch_info.highlight_commits) > 0:
        messages.append({'role': 'user', 'content': 'main commits: ' + '\n'.join(branch_info.highlight_commits)})
        messages.append({'role': 'user', 'content': 'secondary commits: ' + '\n'.join(branch_info.commits)})
    else:
        messages.append({'role': 'user', 'content': 'git commits: ' + '\n'.join(branch_info.commits)})

    messages.append({'role': 'user', 'content': 'PR template:\n' + _get_pr_template()})

    current_total_length = sum([len(m['content']) for m in messages])

    if current_total_length / TOKENIZER_RATIO > MAX_TOKENS:
        raise Exception(f'Current total length {current_total_length} is greater than max tokens {MAX_TOKENS}')

    total_length_with_diff = current_total_length + len(branch_info.diff)
    if total_length_with_diff / TOKENIZER_RATIO > MAX_TOKENS:
        print('Total content length (with diff) is too big.', cc.red('Skipping diff content...'))
    else:
        messages.append({'role': 'user', 'content': 'Diff changes:\n' + branch_info.diff})

    client = OpenAI(api_key=_get_open_ai_key())

    openai_model = config.get_user_config('OPENAI_MODEL')
    print('Using OpenAI model:', cc.yellow(openai_model))

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=openai_model,
        functions=functions,
        function_call={'name': 'create_pr'},
        temperature=0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    arguments = _parse_json(chat_completion.choices[0].message.function_call.arguments)

    return PrData(
        branch_info=branch_info,
        title=arguments['title'],
        body=arguments['description']
    )


def _parse_json(content):
    '''
    A bit of a hack to parse the json content from the chat completion
    Sometimes it returns a string with invalid json content (line breaks) that
    makes it hard to parse.
    example:

    content = '{\n"title": "feat(dependencies): pin dependencies versions",\n"description":
                "### Ref. [Link]\n\n## What was done? ..."\n}'
    '''

    try:
        content = content.replace('{\n"title":', '{"title":')
        content = content.replace(',\n"description":', ',"description":')
        content = content.replace('\n}', '}')
        content = content.replace('\n', '\\n')

        return json.loads(content)
    except Exception as e:
        print('Error to decode message:', e)
        print('Content:', content)
        raise e
