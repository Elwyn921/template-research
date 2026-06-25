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

# 3) Install the locked environment.
uv sync --all-extras --group dev

# 4) Verify the template works.
uv run pytest
uv run ruff check .
uv run python -m my_project_slug.pipelines.run_demo
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
make clean       # remove generated local artifacts
```

## Optional extensions

- `extensions/dvc/` — add DVC when datasets or artifacts no longer belong in Git.
- `extensions/mlflow/` — add MLflow when you compare multiple model runs.
- `extensions/quarto/` — add Quarto when reports must be regenerated from code.

Do not enable an extension merely because it is fashionable. Enable it when the project has the corresponding operational need.

## Project status conventions

- `draft`: idea or data reconnaissance
- `active`: main analysis is underway
- `frozen`: analyses are fixed for a report or submission
- `archived`: no active development; reproducibility must remain intact
