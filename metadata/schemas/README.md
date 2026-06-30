# Schemas

Put machine-readable contracts here when data structures stabilize.

Recommended progression:

1. Begin with `docs/DATA_DICTIONARY.md`.
2. Add a CSV/JSON schema when a table is reused.
3. Add Pandera, Pydantic, or Great Expectations only when repeated validation justifies it.

Current repository contracts:

- `figure-brief.schema.json` for governed data, conceptual, and mixed figures.
- `paperviz-input.schema.json` for constrained PaperVizAgent inputs.
