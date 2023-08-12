import subprocess
from setuptools import setup, find_packages


def dependencies_filter(dependency):
    if dependency.startswith('-i'):
        return False

    return True


def get_pipenv_requirements():
    result = subprocess.run(['pipenv', 'requirements'], capture_output=True, text=True)

    if result.returncode == 0:
        dependencies = [dependency
                        for dependency in result.stdout.splitlines()
                        if dependencies_filter(dependency)]
        return dependencies
    else:
        raise RuntimeError(f"'pipenv lock --requirements' failed with error: {result.stderr}")


setup(name='gpt-pr',
      version='0.0.1',
      description='Automate your GitHub workflow with GPT-PR: an OpenAI powered library for streamlined PR generation.',
      url='http://github.com/alissonperez/gpt-pr',
      author='Alisson R. Perez',
      author_email='alissonperez@outlook.com',
      license='MIT',
      entry_points={
          'console_scripts': ['gpt-pr=gptpr.main:main'],
      },
      packages=find_packages('.'),
      install_requires=get_pipenv_requirements(),
      zip_safe=False)
