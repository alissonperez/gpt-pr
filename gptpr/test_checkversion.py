import pytest
import requests
import json
from datetime import datetime
from unittest.mock import patch, mock_open

from gptpr.version import __version__
from gptpr.checkversion import (get_latest_version, load_cache,
                                save_cache, check_for_updates,
                                CACHE_DURATION)


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')


@pytest.fixture
def mock_os_path_exists(mocker):
    return mocker.patch('os.path.exists')


@pytest.fixture
def mock_open_file(mocker):
    return mocker.patch('builtins.open', mock_open())


@pytest.fixture
def mock_datetime(mocker):
    return mocker.patch('gptpr.checkversion.datetime')


def test_get_latest_version(mock_requests_get, mock_os_path_exists):
    mock_os_path_exists.return_value = False
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {'info': {'version': '2.0.0'}}

    assert get_latest_version() == '2.0.0'


def test_get_latest_version_error(mock_requests_get, mock_os_path_exists):
    mock_os_path_exists.return_value = False
    mock_requests_get.side_effect = requests.exceptions.RequestException

    assert get_latest_version() is None


def test_load_cache(mock_os_path_exists, mock_open_file):
    mock_os_path_exists.return_value = True
    mock_open_file.return_value.read.return_value = json.dumps({
        'last_checked': datetime.now().isoformat(),
        'latest_version': '2.0.0'
    })

    cache = load_cache()
    assert cache['latest_version'] == '2.0.0'


def test_load_cache_no_file(mock_os_path_exists):
    mock_os_path_exists.return_value = False

    cache = load_cache()
    assert cache == {}


def test_save_cache(mock_open_file):
    data = {
        'last_checked': datetime.now().isoformat(),
        'latest_version': '2.0.0'
    }

    save_cache(data)
    mock_open_file.return_value.write.assert_called_once_with(json.dumps(data))


def test_check_for_updates_new_version(mocker, mock_datetime, mock_requests_get, mock_open_file):
    # Set up mocks
    last_checked_str = (datetime(2024, 1, 1) - CACHE_DURATION).isoformat()
    mock_datetime.now.return_value = datetime(2024, 1, 2)
    mock_datetime.fromisoformat.return_value = datetime.fromisoformat(last_checked_str)
    mock_open_file.return_value.read.return_value = json.dumps({
        'last_checked': last_checked_str,
        'latest_version': '1.0.0'
    })
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.json.return_value = {'info': {'version': '2.0.0'}}

    # Capture the print statements
    with patch('builtins.print') as mocked_print:
        check_for_updates()
        assert mocked_print.call_count == 3


def test_check_for_updates_no_new_version(mocker, mock_datetime, mock_requests_get, mock_open_file):
    # Set up mocks
    last_checked_str = (datetime(2024, 1, 1) - CACHE_DURATION).isoformat()
    mock_datetime.now.return_value = datetime(2024, 1, 2)
    mock_datetime.fromisoformat.return_value = datetime.fromisoformat(last_checked_str)
    mock_open_file.return_value.read.return_value = json.dumps({
        'last_checked': (datetime(2024, 1, 1) - CACHE_DURATION).isoformat(),
        'latest_version': __version__
    })
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.json.return_value = {'info': {'version': __version__}}

    # Capture the print statements
    with patch('builtins.print') as mocked_print:
        check_for_updates()
        assert mocked_print.call_count == 0


def test_check_for_updates_cache_valid(mock_datetime, mock_open_file):
    # Set up mocks
    last_checked_str = datetime(2024, 1, 2).isoformat()
    mock_datetime.now.return_value = datetime(2024, 1, 2)
    mock_datetime.fromisoformat.return_value = datetime.fromisoformat(last_checked_str)
    mock_open_file.return_value.read.return_value = json.dumps({
        'last_checked': last_checked_str,
        'latest_version': __version__
    })

    # Capture the print statements
    with patch('builtins.print') as mocked_print:
        check_for_updates()
        assert mocked_print.call_count == 0
