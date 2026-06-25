.PHONY: setup test lint format demo audit clean

setup:
	uv sync --all-extras --group dev

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

demo:
	uv run python -m research_project.pipelines.run_demo

audit:
	uv run python scripts/audit_registry.py

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov outputs/figures/* outputs/tables/* outputs/models/* outputs/predictions/* outputs/diagnostics/*
