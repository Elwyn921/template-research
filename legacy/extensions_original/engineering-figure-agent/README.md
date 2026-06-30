# Governed extension: Engineering Figure Agent

Engineering Figure Agent is the default agent-native figure tool for this
repository when a task needs publication-style engineering or scientific
figures.

Use it as a workflow choice, not as a blanket requirement.

Upstream entry:

- Repository: https://github.com/heyu-233/engineering-figure-agent
- Codex skill entry: upstream `SKILL.md`
- Upstream schemas: `schemas/figure-brief.schema.json` and
  `schemas/plot-request.schema.json`
- Upstream examples: `examples/figure-briefs/`

## Agent Routing

- If the figure needs exact values, axes, units, error bars, benchmark geometry,
  SHAP values, residuals, or statistical diagnostics, use a data-grounded
  renderer: Engineering Figure Agent `plot` mode, the local builder, or another
  audited chart backend from a figure brief.
- If the figure is a workflow, architecture diagram, schematic, or graphical
  abstract, use `image` mode from a figure brief.
- If the figure combines exact data panels and conceptual panels, use `mixed`
  mode: render exact data panels with a data-grounded renderer first, then
  compose or describe the conceptual panels.
- If the task needs multiple academic candidates, reference-driven style, or
  critic refinement, hand off to the PaperVizAgent adapter after the brief is
  complete.

The upstream skill's mode boundary is binding in this repository too:

- `image` mode is for conceptual engineering or scientific figures.
- `plot` mode is one approved route for exact publication-style charts from
  numeric data; it is not the only possible renderer.
- `mixed` mode renders exact quantitative panels with a data-grounded renderer
  before any conceptual composition.
- Image generation must never supply exact values, axes, benchmark geometry,
  residuals, SHAP values, or model metrics.

## Data Figure Path

For local data figures, agents can use this repository's lightweight builder:

```bash
uv run python scripts/build_data_figure.py reports/paper/figures/briefs/<brief>.yaml
```

The builder is intentionally conservative:

- it reads only source data, committed outputs, or registered experiment records
  named in the brief;
- it fails on placeholder paths or missing columns;
- it writes a sidecar JSON record next to the figure;
- it does not invent metrics, uncertainty intervals, SHAP values, or scientific
  interpretations.

## External Tool Checkout

Keep the upstream tool outside this repository or install it as a user-level
Codex skill. Do not vendor API keys, provider configs, or private relay details
into this template.

Reference checkout:

```bash
git clone https://github.com/heyu-233/engineering-figure-agent ../engineering-figure-agent
```

When the upstream skill is installed in Codex, call it through its `SKILL.md`
workflow and bring only figure briefs, plot requests, generated figures, and
verification records back into this repository.

## Output Locations

- Figure briefs: `reports/paper/figures/briefs/`
- Generated figures: `outputs/figures/`
- Supporting tables: `outputs/tables/`
- Verification notes: figure brief, sidecar JSON, report notes, or experiment
  registry
