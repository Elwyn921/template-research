# Toolchain Policy

This root file tells agents how to route research work autonomously. It is not a
restriction on how the repository owner may explore ideas manually.

The detailed policy lives in `docs/RESEARCH_STACK.md`.

## Required Context For Agents

Load the relevant subset of these files before changing research logic, data
records, experiment records, reportable figures, or reports:

- `RESEARCH.md`
- `PROJECT_BRIEF.yaml`
- `FIGURE_GENERATION_CONTRACT.md`
- `AGENTS.md`
- `TOOL_MODULES.md`
- `docs/RESEARCH_STACK.md`
- `tool_catalog.yaml`
- `configs/modules.yaml`

Before enabling optional research tools or changing module interfaces, also load:

- `TOOL_MODULES.md`
- the relevant module and built-in profile in `tool_catalog.yaml`
- the relevant extension README under `extensions/`, if one exists

## Autonomous Execution Loop

Agents should run this loop without asking the owner unless a blocker appears:

1. Classify the task as literature, data audit, modeling, data figure,
   conceptual figure, report writing, artifact versioning, tool module, or
   environment work.
2. Read the smallest necessary context from the root policies, registries,
   configs, experiment records, and active figure brief.
3. Choose the lightest tool path that can produce a traceable output.
4. Create or update the artifact in the expected repository location.
5. Verify that claims, numbers, labels, citations, and data paths are grounded.
6. Record the source, config, output path, and any important exception.

Ask for owner input only when:

- a required source, dataset, credential, or domain definition is unavailable;
- two plausible interpretations would lead to different research claims;
- private data, paid APIs, or external accounts are needed;
- a heavy tool or project restructure would be introduced;
- the task asks for a scientific, investment, or causal conclusion that is not
  supported by the available evidence.

## Tool Routing If/Else

### Tool Modules

- If the task asks what tools to use, inspect `tool_catalog.yaml` before adding
  dependencies.
- Treat `TOOL_MODULES.md`, `tool_catalog.yaml`, and `configs/modules.yaml` as
  the active module interface; `docs/` files are explanatory support.
- If the task enables a module, update `configs/modules.yaml`; read upstream
  GitHub docs from `tool_catalog.yaml` before adding local setup.
- If a module requires a heavy dependency, external app, paid API, MCP server,
  or private account, document the reason in `docs/DECISIONS.md` before
  adopting it.
- If the task only needs a capability temporarily, prefer a documented candidate
  tool path over installing a permanent dependency.

### Literature

- If the task is collecting, reading, or citing papers, use Zotero as the local
  reference spine.
- Else if semantic retrieval over the local library is needed and ZotSeek is
  available, use ZotSeek.
- Else if external discovery is needed, use only the relevant K-Dense skills,
  usually `paper-lookup` and `citation-management`.
- Record reportable sources in `metadata/source_registry.csv` or report notes.

### Modeling And Statistical Work

- If the task is concrete/materials ML, start with pandas, `scikit-learn`, SHAP,
  and focused statistical diagnostics.
- Else if the task is AI industry or investment research, start with sourced
  indicators, time coverage, assumptions, and `statsmodels`-style checks.
- Else if the task is industrial factor mining, start with factor construction,
  leakage controls, validation splits, diagnostics, and robustness checks.
- If pandas becomes too slow or memory-bound, consider `polars`, `dask`, or
  `zarr-python` and document the reason.
- If materials composition or structure logic is needed, consider `pymatgen`.

### Professional Data Figures

- If the figure contains exact data, axes, units, error bars, model metrics,
  residuals, SHAP values, factor returns, or statistical diagnostics, use local
  plotting or Engineering Figure Agent `plot` mode.
- If the task is model prediction quality, default to observed-vs-predicted,
  residual-vs-fitted, residual distribution, split-aware metric annotations, and
  uncertainty where available.
- If the task is explainable AI, default to SHAP summary/bar/dependence plots,
  partial dependence or sensitivity plots, and feature names tied to the data
  dictionary.
- If the task is factor mining or investment research, default to time-series
  coverage, rolling statistics, quantile/group comparisons, source dates, and
  robustness notes.
- If the chart type is unclear, inspect the data shape and claim first, then
  choose the plot that best shows the unit of analysis, comparison, uncertainty,
  and limitation.
- Save exact data figures under `outputs/figures/` and supporting tables under
  `outputs/tables/`.

### Conceptual And Mixed Figures

- If the figure is a workflow, architecture diagram, mechanism hypothesis, or
  graphical abstract, use a figure brief and Engineering Figure Agent `image`
  mode.
- Else if exact evidence panels and conceptual panels both matter, use `mixed`
  mode: render exact panels locally first, then compose or describe conceptual
  panels around them.
- Else if multiple academic candidates, reference-driven styling, or critic
  refinement would help, use the PaperVizAgent adapter.

### PaperVizAgent

- If using PaperVizAgent, compile the repository-grounded input first:

  ```bash
  uv run python scripts/build_paperviz_input.py reports/paper/figures/briefs/<brief>.yaml
  ```

- If the starting point is a loose prompt, convert it into a figure brief before
  compiling.
- If an image was generated without the adapter, treat it as a draft, verify it
  against the active brief and research policies, and rebuild when the mismatch
  matters.
- Do not use PaperVizAgent as the source of exact quantitative plots.

### DVC And Quarto

- If Git plus registries can track artifacts comfortably, keep DVC disabled.
- If data, model, prediction, or experiment artifacts outgrow Git, enable DVC
  for those artifacts while keeping human-readable manifests.
- If reports are still exploratory memos, keep them as Markdown.
- If a report needs one-command regeneration from committed outputs, add Quarto
  as a reporting layer.

### Heavy Orchestration

- For normal research projects, avoid Kedro, MLflow, Kubeflow, Airflow, Prefect,
  Dagster, feature stores, model registries, service dashboards, and long-running
  orchestration.
- If one of those tools becomes necessary, document the concrete need in
  `docs/DECISIONS.md` before adding it.

## Integrity Guardrails

- Do not invent data, citations, mechanisms, financial facts, model metrics, or
  experimental results.
- Do not use image generation as the source of exact quantitative content.
- Do not commit Zotero databases, restricted PDFs, API keys, provider configs, or
  private data.
- Do not install the full K-Dense skill collection when a selected subset solves
  the task.
