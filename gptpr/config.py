from copy import deepcopy
import configparser
import os


def config_command_example(name, value_sample):
    return f'gpt-pr-config set {name} {value_sample}'


CONFIG_README_SECTION = 'https://github.com/alissonperez/gpt-pr?tab=readme-ov-file#authentication--api-keys'


class Config:

    config_filename = '.gpt-pr.ini'

    _default_config = {
        # Github
        'GH_TOKEN': '',

        # Open AI info
        'OPENAI_MODEL': 'gpt-4o',
        'OPENAI_API_KEY': '',
    }

    def __init__(self, config_dir=None):
        self.default_config = deepcopy(self._default_config)
        self._config_dir = config_dir or os.path.expanduser('~')
        self._config = configparser.ConfigParser()
        self._initialized = False

    def load(self):
        if self._initialized:
            return

        config_file_path = self.get_filepath()

        if os.path.exists(config_file_path):
            self._config.read(config_file_path)
            self._ensure_default_values()
        else:
            self._config['user'] = {}
            self._config['DEFAULT'] = deepcopy(self.default_config)
            self.persist()

        self._initialized = True

    def _ensure_default_values(self):
        added = False
        for key, value in self.default_config.items():
            if key not in self._config['DEFAULT']:
                self._config['DEFAULT'][key] = value
                added = True

        if added:
            self.persist()

    def persist(self):
        config_file_path = self.get_filepath()

        with open(config_file_path, 'w') as configfile:
            self._config.write(configfile)

    def get_filepath(self):
        return os.path.join(self._config_dir, self.config_filename)

    def set_user_config(self, name, value):
        self.load()
        self._config['user'][name] = value

    def reset_user_config(self, name):
        self.load()
        self._config['user'][name] = self.default_config[name]
        self.persist()

    def get_user_config(self, name):
        self.load()
        return self._config['user'][name]

    def all_values(self):
        self.load()

        # iterate over all sections and values and return them in a list
        result = []

        # add default section
        for option in self._config['DEFAULT']:
            result.append(('DEFAULT', option, self._config['DEFAULT'][option]))

        for section in self._config.sections():
            for option in self._config[section]:
                result.append((section, option, self._config[section][option]))

        return result


config = Config()
