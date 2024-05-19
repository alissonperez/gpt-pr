import requests
import os
import json
import tempfile
from gptpr.version import __version__
from datetime import datetime, timedelta

from gptpr import consolecolor as cc


PACKAGE_NAME = 'gpt-pr'
CACHE_FILE = os.path.join(os.path.expanduser("~"), '.gpt_pr_update_cache.json')
CACHE_DURATION = timedelta(days=1)


def cache_daily_version(func):
    def wrapper(*args, **kwargs):
        cache = load_cache()
        last_checked = cache.get('last_checked')

        if last_checked:
            last_checked = datetime.fromisoformat(last_checked)

            if datetime.now() - last_checked < CACHE_DURATION:
                # Use cached version info
                latest_version = cache.get('latest_version')
                if latest_version:
                    return latest_version

        latest_version = func(*args, **kwargs)
        cache = {
            'last_checked': datetime.now().isoformat(),
            'latest_version': latest_version
        }
        save_cache(cache)

        return latest_version

    return wrapper


def get_cache_file_path():
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f'{PACKAGE_NAME}_update_cache.json')


@cache_daily_version
def get_latest_version():
    url = f'https://pypi.org/pypi/{PACKAGE_NAME}/json'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest version info: {e}")
        return None


def load_cache():
    cache_file = get_cache_file_path()
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return json.load(file)

    return {}


def save_cache(data):
    cache_file = get_cache_file_path()
    with open(cache_file, 'w') as file:
        file.write(json.dumps(data))


def check_for_updates():
    latest_version = get_latest_version()

    if latest_version and latest_version != __version__:
        print('')
        print(cc.yellow(
            f'A new version of {PACKAGE_NAME} is available ({latest_version}). '
            f'You are using version {__version__}. Please update by running'),
            cc.green(f'pip install --upgrade {PACKAGE_NAME}.'))
        print('')


if __name__ == "__main__":
    check_for_updates()
    # Your CLI code here
