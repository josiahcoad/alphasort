install:
	poetry install

shell:
	poetry shell

run:
	poetry run python -m src.alphasort src --suffix test.py

test:
	poetry run pytest tests

lint:
	poetry run ruff src tests

typing:
	poetry run mypy src tests

format:
	poetry run black src tests

clean:
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +

remove-venv:
	rm -rf .venv

update:
	poetry update

.PHONY: all
all: install run