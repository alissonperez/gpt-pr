
cleanup:
	rm -rf dist
	pip uninstall gpt-pr --yes

requirements:
	pipenv requirements > requirements.txt

install: cleanup requirements
	python setup.py clean --all
	pip install .

build: cleanup requirements
	@echo "Building..."
	python3 -m build

publish-test: build
	pipenv run twine upload --repository testpypi dist/* --verbose

publish: build
	pipenv run twine upload --repository pypi dist/* --verbose

lint:
	pipenv run flake8 .

test:
	pipenv run pytest -vv .
