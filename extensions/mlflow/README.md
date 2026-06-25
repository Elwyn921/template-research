# Optional extension: MLflow

Enable when multiple model runs make manual experiment logs unreliable.

```bash
uv sync --extra tracking
uv run mlflow ui --backend-store-uri ./mlruns
```

Log dataset version, config, seed, metrics, diagnostics, artifacts, and Git commit.
