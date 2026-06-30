# Governed extension: DVC

Agents should enable DVC when data, model artifacts, or intermediates no longer
belong in Git, or when collaborators need artifact checkout. If an agent enables
DVC before those conditions appear, it should record the concrete reason in
`docs/DECISIONS.md`.

```bash
make setup EXTRAS="data-versioning"
uv run dvc init
uv run dvc add data/raw/<dataset>
git add .dvc .gitignore
```

Then translate reproducible steps into `dvc.yaml`; keep parameters in `configs/` and commit `dvc.lock`.
