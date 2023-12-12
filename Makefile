REPO = wikiscraper
PACKAGES = ${REPO}/*
#wikiscraper_tests/* bin/*
NO_LINTING = no_linting.grep

all: clean ruff black test

check: ruff lint typecheck tests

test: black check

test-all: black check

setup:
	poetry install --no-ansi

lint: setup
	find . -iname '*.py' | grep -E -v -f $(NO_LINTING) | sort | xargs poetry run pylint -j 0

ruff: setup
	poetry run ruff --fix $(PACKAGES)

typecheck: setup
	find . -iname '*.py' | grep -E -v -f $(NO_LINTING) | sort | xargs poetry run mypy

tests: setup
	poetry run pytest -vvv -n 6 --junitxml pytest-result.xml --log-cli-level DEBUG

black: setup
	poetry run black $(PACKAGES)


clean:
	find . -iname '*.pyc' -delete
	rm -f .coverage
	rm -f pytest-result.xml
	rm -rf .mypy_cache/
	rm -rf *.pytest_cache/
	rm -rf *.ruff_cache/
	rm -rf .venv/
	rm -rf htmlcov/
	rm -rf stubs/
	rm -rf $(SUBPACKAGE)
