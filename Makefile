.PHONY: setup test lint format demo audit data-figure paperviz-input clean

FIGURE_BRIEF ?= reports/paper/figures/briefs/example_concrete_ai_workflow.yaml
DATA_FIGURE_BRIEF ?= reports/paper/figures/briefs/example_sample_data_figure.yaml

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

data-figure:
	uv run python scripts/build_data_figure.py $(DATA_FIGURE_BRIEF)

paperviz-input:
	uv run python scripts/build_paperviz_input.py $(FIGURE_BRIEF)

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov outputs/figures/* outputs/tables/* outputs/models/* outputs/predictions/* outputs/diagnostics/*
