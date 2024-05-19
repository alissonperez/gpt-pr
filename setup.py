import os
from setuptools import setup, find_packages


def dependencies_filter(dependency):
    if dependency.startswith('-i'):
        return False

    return True


def get_requirements():
    with open('requirements.txt') as f:
        dependencies = [dependency
                        for dependency in f.read().splitlines()
                        if dependencies_filter(dependency)]
        return dependencies


version = os.environ.get('VERSION')
if not version:
    raise Exception('VERSION environment variable not set')


def write_version(current_version):
    with open('gptpr/version.py', 'w') as f:
        f.write(f'__version__ = "{current_version}"\n')


write_version(version)

setup(name='gpt-pr',
      version=version,
      python_requires='>=3.7',
      description=('Automate your GitHub workflow with GPT-PR: '
                   'an OpenAI powered library for streamlined PR generation.'),
      url='http://github.com/alissonperez/gpt-pr',
      author='Alisson R. Perez',
      author_email='alissonperez@outlook.com',
      license='MIT',
      entry_points={
          'console_scripts': [
              'gpt-pr=gptpr.main:main',
              'gpt-pr-config=gptpr.main:run_config',
          ],
      },
      packages=find_packages('.'),
      include_package_data=True,
      install_requires=get_requirements(),
      zip_safe=False)
