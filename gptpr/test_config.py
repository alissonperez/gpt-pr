import os
import configparser

from pytest import fixture

from gptpr.config import Config


@fixture
def temp_config(tmpdir):
    temp_dir = tmpdir.mkdir('config_dir')
    config = Config(temp_dir)
    return config, temp_dir


def _check_config(config, temp_dir, config_list):
    # Read the configuration file and verify its contents
    config_to_test = configparser.ConfigParser()
    config_to_test.read(os.path.join(str(temp_dir), config.config_filename))

    for section, key, value in config_list:
        assert config_to_test[section][key] == value


def test_init_config_file(temp_config):
    config, temp_dir = temp_config
    config.load()

    # Check if the file exists
    assert os.path.isfile(os.path.join(str(temp_dir), config.config_filename))

    _check_config(config, temp_dir, [
        ('DEFAULT', 'OPENAI_MODEL', 'gpt-4o'),
        ('DEFAULT', 'OPENAI_API_KEY', ''),
    ])


def test_new_default_value_should_be_added(temp_config):
    config, temp_dir = temp_config
    config.load()  # data was written to the file

    new_config = Config(temp_dir)

    # Add a new default value
    new_config.default_config['NEW_DEFAULT'] = 'new_default_value'
    new_config.load()  # Should update config file...

    _check_config(new_config, temp_dir, [
        ('DEFAULT', 'NEW_DEFAULT', 'new_default_value'),
    ])


def test_set_user_config(temp_config):
    config, temp_dir = temp_config

    config.set_user_config('OPENAI_MODEL', 'gpt-3.5')
    config.persist()

    # Read the configuration file and verify its contents
    config_to_test = configparser.ConfigParser()
    config_to_test.read(os.path.join(str(temp_dir), config.config_filename))

    _check_config(config, temp_dir, [
        ('user', 'OPENAI_MODEL', 'gpt-3.5'),
        ('user', 'OPENAI_API_KEY', ''),
    ])


def test_all_values(temp_config):
    config, temp_dir = temp_config

    all_values = config.all_values()

    assert all_values == [
        ('DEFAULT', 'gh_token', ''),
        ('DEFAULT', 'openai_model', 'gpt-4o'),
        ('DEFAULT', 'openai_api_key', ''),
        ('user', 'gh_token', ''),
        ('user', 'openai_model', 'gpt-4o'),
        ('user', 'openai_api_key', ''),
    ]


def test_reset_user_config(temp_config):
    config, temp_dir = temp_config

    config.set_user_config('OPENAI_MODEL', 'gpt-3.5')
    config.persist()

    config.reset_user_config('OPENAI_MODEL')

    # Read the configuration file and verify its contents
    config_to_test = configparser.ConfigParser()
    config_to_test.read(os.path.join(str(temp_dir), config.config_filename))

    _check_config(config, temp_dir, [
        ('user', 'OPENAI_MODEL', 'gpt-4o'),
        ('user', 'OPENAI_API_KEY', ''),
    ])
