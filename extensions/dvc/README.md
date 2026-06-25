# Optional extension: DVC

Enable when data, model artifacts, or intermediates no longer belong in Git.

```bash
uv sync --extra data-versioning
uv run dvc init
uv run dvc add data/raw/<dataset>
git add .dvc .gitignore
```

Then translate reproducible steps into `dvc.yaml`; keep parameters in `configs/` and commit `dvc.lock`.
