# template-research

A lean, reproducible GitHub template for research, statistical modeling, factor mining, and data-driven industry studies.

## Design rule

> A result is not “final” unless it can be traced to a question, source, dataset version, configuration, code commit, and output artifact.

This template intentionally starts light. It supports a research-grade workflow without forcing a full MLOps stack into every project.

## What belongs where

| Location | Put here | Do not put here |
|---|---|---|
| `data/raw/` | immutable source copies | cleaned or manually edited data |
| `data/interim/` | reproducible intermediate tables | final analysis tables |
| `data/processed/` | validated modeling-ready datasets | ad hoc exports |
| `data/sample/` | small shareable demo data | sensitive or large datasets |
| `src/` | reusable production research logic | exploratory notebook-only code |
| `notebooks/` | EDA, hypothesis exploration, figures-in-progress | the only copy of a pipeline |
| `configs/` | parameters and experimental choices | secrets |
| `outputs/` | generated artifacts only | hand-edited “final final” files |
| `reports/` | narrative reports, memos, manuscript sources | raw data or model code |
| `metadata/` | provenance, schemas, data dictionary | unverified claims |

## Bootstrap

```bash
# 1) Create a repository from this GitHub template, then clone it.
git clone <your-repository-url>
cd <your-repository>

# 2) Rename the placeholder package once.
python scripts/rename_project.py my_project_slug "My Research Project"

# 3) Install the base environment.
uv sync --group dev

# 4) Verify the template works.
uv run pytest
uv run ruff check .
uv run python -m my_project_slug.pipelines.run_demo
```

Optional research modules are installed explicitly. For example:

```bash
make setup EXTRAS="data-experiment publication-output"
make tools-profile PROFILE=concrete_ml
```

`uv.lock` is intentionally not committed in this template because the generated project name and optional dependency profile can differ. After adding packages, create and commit it:

```bash
uv lock
uv sync
```

## Minimum research workflow

1. Fill `PROJECT_BRIEF.yaml` before collecting or modeling data.
2. Register every source in `metadata/source_registry.csv`.
3. Register each dataset release in `metadata/data_manifest.csv`.
4. Put all choices that affect results in `configs/`, not in code.
5. Use one issue / one branch for one research claim or pipeline change.
6. Create an experiment record before calling any result “reportable”.
7. Generate figures and tables into `outputs/`; reference them in `reports/`.
8. Tag every externally shared version, for example `v0.1-data-audit` or `v1.0-submission`.

## Commands

```bash
make setup       # sync environment
make test        # run tests
make lint        # lint and format check
make format      # auto-format
make demo        # run the sample pipeline
make audit       # basic data registry audit
make tools-audit # validate tool catalog and profiles
make tools-list  # list opt-in research tool modules
make tools-profile PROFILE=concrete_ml # print a module activation plan
make data-figure # build a local data figure from a figure brief
make paperviz-input # compile a PaperVizAgent input JSON from a figure brief
make clean       # remove generated local artifacts
```

## Research tool library

The template also acts as a lightweight research tool library. The catalog does
not install external services by default; it lets agents and project owners
choose modules as a project becomes concrete.

- `tool_catalog.yaml` — machine-readable module catalog.
- `TOOL_MODULES.md` — root agent-facing contract for module activation.
- `configs/modules.yaml` — current project profile and enabled module state.
- upstream GitHub links in `tool_catalog.yaml` — first place to read before
  enabling optional tools.

Start from `base_research`, then enable only the modules required by the active
question, dataset, model, figure, or publication target.

## Governed extensions

- `extensions/dvc/` — use when artifact versioning is needed or artifact checkout would help collaboration.
- `extensions/engineering-figure-agent/` — default route for data, conceptual, and mixed research figures.
- `extensions/papervizagent/` — adapter for PaperVizAgent when multi-candidate or critic-refined academic visuals are useful.
- `extensions/quarto/` — use when reports need one-command regeneration from committed outputs.

Agents should not add MLflow, Kedro, Kubeflow, Airflow, Prefect, Dagster,
feature stores, model registries, service dashboards, or long-running
orchestration unless a concrete need is documented.

## Agent figure workflow

Research and figure generation should follow the root policies:

- `RESEARCH.md`
- `TOOLCHAIN.md`
- `FIGURE_GENERATION_CONTRACT.md`
- `AGENTS.md`
- `docs/RESEARCH_STACK.md`

For exact data figures, agents should use local plotting or Engineering Figure
Agent `plot` mode. The runnable template path is:

```bash
make data-figure
```

For conceptual or mixed figures, agents should start from a figure brief. If
PaperVizAgent is useful for multi-candidate academic illustration or critic
refinement, compile a repository-grounded input first:

```bash
make paperviz-input FIGURE_BRIEF=reports/paper/figures/briefs/example_concrete_ai_workflow.yaml
```

The compiled JSON is written under `outputs/figures/papervizagent/` and can be
copied into PaperVizAgent. Data figures remain data-grounded: exact values,
axes, units, errors, metrics, and diagnostics come from local data or committed
outputs.

## Project status conventions

- `draft`: idea or data reconnaissance
- `active`: main analysis is underway
- `frozen`: analyses are fixed for a report or submission
- `archived`: no active development; reproducibility must remain intact
