
cleanup:
	rm -rf dist
	pip uninstall gpt-pr --yes

install: cleanup
	python setup.py clean --all
	pip install .

build: cleanup
	@echo "Building..."
	poetry build

publish-test: build
	poetry publish -r test-pypi

publish: build
	poetry publish

lint:
	poetry run flake8 .

test:
	poetry run pytest -vv .
