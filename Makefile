.PHONY: all install run debug clean lint lint-strict package

all: run

install:
	uv sync

run: install
	uv run python pac-man.py config.json

debug: install
	uv run python -m pdb pac-man.py config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint: install
	uv run python -m flake8 .
	uv run python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	uv run python -m flake8 .
	uv run python -m mypy . --strict

package: install
	uv run pyinstaller --clean --name Pacman --onedir --add-data "assets:assets" pac-man.py
