from gptpr.prdata import _parse_json


def test_parse_json():
    content = ('{\n"title": "feat(dependencies): pin dependencies '
               'versions",\n"description": "### Ref. [Link]\n\n## What was done? ..."\n}')

    expected = {
        'title': 'feat(dependencies): pin dependencies versions',
        'description': '### Ref. [Link]\n\n## What was done? ...'
    }

    assert _parse_json(content) == expected, "The function did not return the expected output."
