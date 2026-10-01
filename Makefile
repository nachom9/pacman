.PHONY: all install run debug clean lint lint-strict

all: run

install:
	uv sync

run: install
	uv run python -m src

debug: install
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint: install
	uv run python -m flake8 src
	uv run python -m mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	uv run python -m flake8 src
	uv run python -m mypy src --strict