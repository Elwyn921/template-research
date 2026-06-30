.PHONY: setup test lint format demo audit tools-audit tools-list tools-profile data-figure paperviz-input clean

FIGURE_BRIEF ?= reports/paper/figures/briefs/example_concrete_ai_workflow.yaml
DATA_FIGURE_BRIEF ?= reports/paper/figures/briefs/example_sample_data_figure.yaml
EXTRAS ?=
PROFILE ?= base_research
UV_EXTRA_FLAGS := $(foreach extra,$(EXTRAS),--extra $(extra))

setup:
	uv sync --group dev $(UV_EXTRA_FLAGS)

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

tools-audit:
	uv run python scripts/audit_tool_modules.py

tools-list:
	uv run python scripts/audit_tool_modules.py --list

tools-profile:
	uv run python scripts/audit_tool_modules.py --profile $(PROFILE)

data-figure:
	uv run python scripts/build_data_figure.py $(DATA_FIGURE_BRIEF)

paperviz-input:
	uv run python scripts/build_paperviz_input.py $(FIGURE_BRIEF)

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov outputs/figures/* outputs/tables/* outputs/models/* outputs/predictions/* outputs/diagnostics/*
