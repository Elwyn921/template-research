.PHONY: setup test lint format foundry-validate tools-list tools-show profiles-list packs-list packs-validate tool-plan export-research-os pack-diff data-figure paperviz-input clean

FIGURE_BRIEF ?= examples/research_os_project/reports/paper/figures/briefs/example_concrete_ai_workflow.yaml
DATA_FIGURE_BRIEF ?= examples/research_os_project/reports/paper/figures/briefs/example_sample_data_figure.yaml
EXTRAS ?=
PROFILE ?= base_research
TOOL ?=
PROJECT_TYPE ?= empirical_materials
TASK ?= "test domain shift and local calibration"
STAGE ?= experiment
DEST ?=
BASE ?= base_research
DOMAIN ?= concrete_ml
ENHANCEMENTS ?= advanced_figure
PACKS ?=
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

foundry-validate:
	uv run python scripts/validate_foundry.py

tools-list:
	uv run python scripts/list_tools.py

tools-show:
	uv run python scripts/list_tools.py --show $(TOOL)

profiles-list:
	uv run python scripts/list_profiles.py

packs-list:
	uv run python scripts/list_packs.py

packs-validate:
	uv run python scripts/validate_pack.py

tool-plan:
	uv run python tool_fabric/resolvers/resolve_tool_plan.py --project-type "$(PROJECT_TYPE)" --task "$(TASK)" --stage "$(STAGE)" --target-output "reproducible result and figure" --profiles "$(DOMAIN),$(ENHANCEMENTS)"

export-research-os:
	uv run python scripts/export_project_capabilities.py --dest $(DEST) --project-type $(PROJECT_TYPE) --base $(BASE) --domain $(DOMAIN) --enhancements "$(ENHANCEMENTS)" --packs "$(PACKS)"

pack-diff:
	uv run python scripts/diff_pack_upgrade.py --dest $(DEST) --packs "$(PACKS)"

data-figure:
	uv run python scripts/build_data_figure.py $(DATA_FIGURE_BRIEF)

paperviz-input:
	uv run python scripts/build_paperviz_input.py $(FIGURE_BRIEF)

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov
