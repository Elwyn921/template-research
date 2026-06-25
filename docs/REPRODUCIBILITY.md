# Reproducibility contract

A reportable result must identify:

1. the research question and target population;
2. the source IDs and dataset version(s);
3. the Git commit or release tag;
4. the configuration file(s) and random seed;
5. the environment lockfile (`uv.lock`);
6. the command that generated the output;
7. the resulting tables, figures, predictions, and diagnostics.

## Re-run convention

A clean clone should be able to reproduce all non-sensitive outputs using:

```bash
uv sync --all-extras --group dev
make test
make demo
```

When data cannot be shared, provide a small sample dataset, a schema, source metadata, and exact acquisition instructions.
