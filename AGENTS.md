# Agent Playbook

This repository is a reproducible research template. Agents should preserve
traceability while still doing useful work autonomously.

## Operating Loop

For each task, agents should:

1. Classify the task: literature, data audit, modeling, data figure, conceptual
   figure, mixed figure, report writing, artifact versioning, tool module, or
   environment work.
2. Read the smallest necessary context from the files below.
3. Choose the lightest workflow that can produce a traceable result.
4. Create or update the artifact in the expected repository location.
5. Verify claims, numbers, units, labels, citations, and output paths.
6. Record important choices in the relevant brief, registry, config, experiment
   record, report note, or decision log.

Ask the owner only when a needed source or dataset is missing, a conclusion is
ambiguous, credentials or private data are required, a heavy dependency would be
introduced, or a project restructure is unavoidable.

## Context Files

Before changing research logic, data records, experiment records, reports, or
reportable figures, read the relevant subset of:

- `README.md`
- `RESEARCH.md`
- `TOOLCHAIN.md`
- `TOOL_MODULES.md`
- `PROJECT_BRIEF.yaml`
- `docs/REPRODUCIBILITY.md`
- `docs/RESEARCH_STACK.md`
- `tool_catalog.yaml`
- `configs/modules.yaml`

Before enabling or changing a tool module, also read:

- `TOOL_MODULES.md`
- the relevant module and built-in profile in `tool_catalog.yaml`
- the relevant extension README under `extensions/`, if one exists

Before generating or revising figures, also read:

- `FIGURE_GENERATION_CONTRACT.md`
- the active figure brief under `reports/paper/figures/briefs/`, if one exists

## Figure Hard Gates

These gates are mandatory for agents. If a figure violates one of them, keep it
as a draft and do not reference it as reportable evidence.

- If a figure contains exact values, axes, units, error bars, benchmark
  geometry, model metrics, residuals, SHAP values, factor returns, or
  statistical diagnostics, use a data-grounded renderer. The renderer may be
  local code, Engineering Figure Agent `plot` mode, Altair/Vega-Lite, Plotly,
  Observable Plot, Quarto, or another audited renderer.
- Image generation and PaperVizAgent must not create exact quantitative marks.
  They may only help with conceptual panels, composition, style exploration,
  labels, or chart/code specifications.
- `mode: image` is only for conceptual figures. A brief with data requirements,
  plot specifications, metrics, axes, or exact numeric panels must use `plot` or
  `mixed`.
- `mode: plot` must not be sent to PaperVizAgent. Use `scripts/build_data_figure.py`
  or another data-grounded renderer.
- `mode: mixed` must render exact data panels first, then compose conceptual
  panels around those generated assets.
- Run `make figures-audit` after changing figure briefs or figure generation
  policy.

## Tool Routing

- If the task is literature retrieval, use Zotero/ZotSeek when local library
  search is relevant, and selected K-Dense skills for external paper lookup or
  citation cleanup.
- If the task is concrete/materials ML, use pandas, scikit-learn, SHAP/XAI, and
  focused diagnostics before considering heavier tools.
- If the task is AI industry or investment research, track source dates,
  company/sector/region scope, indicator construction, assumptions, and caveats.
- If the task is industrial factor mining, track unit of analysis, time window,
  leakage controls, validation split, robustness checks, and downstream decision.
- If artifacts outgrow Git, use DVC for those artifacts and keep the manifests
  readable.
- If reports need one-command regeneration, add Quarto as a reporting layer.
- If a task needs optional tools, select the smallest module/profile from
  `tool_catalog.yaml`, then record enabled modules in `configs/modules.yaml`.

## Data Figure Workflow

Agents should treat data figures as first-class research outputs.

1. Identify the claim, unit of analysis, target/outcome, comparison, and intended
   reader.
2. Locate the source dataset or committed output and check columns, units,
   missingness, sample size, split definitions, and transformations.
3. Choose the plot type from the claim:
   - Distribution: histogram, density, box, violin, empirical CDF, or grouped
     distribution with sample sizes.
   - Relationship: scatter, hexbin, line, smooth trend, grouped response curve,
     or partial dependence with units and uncertainty where available.
   - Prediction: observed-vs-predicted parity plot, residual-vs-fitted,
     residual distribution, calibration, split-aware metric annotations, and
     uncertainty intervals when available.
   - Model comparison: point/range plots or paired comparisons with validation
     split, baseline, metric definition, and confidence interval where
     computable.
   - Explainable AI: SHAP summary/bar/dependence, partial dependence,
     sensitivity curves, or feature interaction plots tied to the data
     dictionary.
   - Concrete/materials analysis: plots grouped by mix design, binder system,
     curing age, exposure, testing condition, and target unit.
   - Factor or investment research: time-series coverage, rolling statistics,
     quantile spreads, turnover, information coefficient, drawdown, source date,
     and robustness notes.
4. Generate exact numeric marks from source data, committed outputs, or
   registered experiment records only.
5. Save figures under `outputs/figures/` and supporting tables under
   `outputs/tables/`.
6. Verify axes, units, transformations, split labels, uncertainty, caveats, and
   source grounding before referencing the figure in `reports/`.

## Conceptual, Mixed, And PaperVizAgent Figures

- If the figure is a workflow, architecture diagram, schematic, or graphical
  abstract, use a figure brief and Engineering Figure Agent `image` mode.
- If exact data panels and conceptual panels both matter, use `mixed` mode:
  render data panels with a data-grounded renderer first, then compose or
  describe the conceptual panels around them.
- If multi-candidate generation, reference-driven style, or critic refinement is
  useful, compile PaperVizAgent input first:

  ```bash
  uv run python scripts/build_paperviz_input.py reports/paper/figures/briefs/<brief>.yaml
  ```

- If a PaperVizAgent image already exists from a loose prompt, verify it against
  `RESEARCH.md`, `FIGURE_GENERATION_CONTRACT.md`, and the active brief before
  treating it as reportable.

## Integrity Guardrails

- Do not invent data, citations, mechanisms, financial facts, model metrics, or
  experimental results.
- Do not use image generation or PaperVizAgent as the source of exact numerical
  plots.
- Do not commit private data, restricted PDFs, API keys, or generated provider
  configs.
- Keep choices that affect results in `configs/`.
- Record reportable runs in `experiments/experiment_registry.csv`.
- Save generated artifacts under `outputs/`.
