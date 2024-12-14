install:
	poetry install

activate:
	poetry shell

run:
	poetry run alphasort

test:
	poetry run pytest -sxv

lint:
	poetry run ruff check --fix

type-check:
	poetry run mypy .

format:
	poetry run ruff format

clean:
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +

remove-venv:
	rm -rf .venv

update:
	poetry update

add-dev:
	poetry add --group dev $(package)

bump:
	poetry version patch

deploy:
	poetry build
	poetry publish

checks:
	pre-commit run --all-files

.PHONY: all pre-deploy

all: install run

pre-deploy: lint type-check test
