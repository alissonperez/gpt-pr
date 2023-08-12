
cleanup:
	rm -rf dist

requirements:
	pipenv requirements > requirements.txt

build: cleanup requirements
	@echo "Building..."
	python3 -m build

publish: build
	python3 -m twine upload --repository pypi dist/* --verbose

lint:
	pipenv run flake8 .
