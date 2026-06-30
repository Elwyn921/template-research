# Tool Module Contract

This is the agent-facing contract for Template Research tool modules. Human
explanations can live under `docs/`, but agents should treat this root file,
`tool_catalog.yaml`, and `configs/modules.yaml` as the active tool-module
interface.

## Source Of Truth

Use these files in this order when selecting or changing optional tools:

1. `AGENTS.md` and `TOOLCHAIN.md` for root agent behavior.
2. `TOOL_MODULES.md` for module activation rules.
3. `tool_catalog.yaml` for modules, candidate tools, GitHub links, local steps,
   and built-in profiles.
4. `configs/modules.yaml` for the current project's active profile and enabled
   modules.
5. The small set of local governed extensions only when they exist under
   `extensions/`.

Files under `docs/` explain the system, but they are not the only enforcement
layer.

## Activation Rules

- Start with the active profile in `configs/modules.yaml`.
- Enable the smallest module set that can answer the current research task.
- Do not install a dependency, MCP server, local app, or external service just
  because it appears in `tool_catalog.yaml`.
- Before enabling a module, confirm the task has a concrete source, dataset,
  model, figure, artifact, report, or publication need.
- Record enabled modules in `configs/modules.yaml`.
- Record heavy dependencies, external services, paid APIs, private accounts, or
  project-wide workflow changes in `docs/DECISIONS.md`.
- Run `make tools-audit` after changing module files.

## Default Enabled Modules

The base template enables only:

- `figure_generation`
- `data_and_database`
- `project_ops`

All other modules are opt-in candidates until a profile or decision enables
them.

## Figure Tool Entry

For `figure_generation`, the governed external entry is:

- upstream repository: `https://github.com/heyu-233/engineering-figure-agent`
- Codex skill entry: upstream `SKILL.md`
- local extension contract: `extensions/engineering-figure-agent/README.md`
- repository figure contract: `FIGURE_GENERATION_CONTRACT.md`

Grounding and rendering rules are mandatory:

- `image` mode: conceptual figures, system architecture diagrams, algorithm
  workflows, graphical abstracts, schematics, and redraws.
- data-grounded rendering: exact bar charts, trend curves, heatmaps, scatter
  plots, ablation plots, benchmark summaries, axes, units, and error bars.
  The renderer can be the local builder, Engineering Figure Agent `plot` mode,
  Vega/Altair, Plotly, Observable Plot, Quarto, or another audited renderer.
- `mixed` mode: render quantitative panels with a data-grounded renderer first,
  then use image generation only for conceptual panels.

Never use image generation as the source of exact values, axes, benchmark
geometry, model metrics, residuals, SHAP values, or other quantitative marks.
AI can help draft chart specifications, code, layout, labels, and styling, but
the marks must be generated from data, committed outputs, or registered
experiment records.

Hard gate for agents: `mode: image` cannot contain `data_requirements`,
`plot_spec`, metrics, axes, or exact numeric panels. `mode: plot` cannot be sent
to PaperVizAgent. Run `make figures-audit` after changing figure briefs or
figure policy.

## Optional Installation

The base environment is installed with:

```bash
make setup
```

Optional Python dependency groups are installed explicitly:

```bash
make setup EXTRAS="data-experiment publication-output"
```

External desktop apps, MCP servers, paid APIs, local paper libraries, and
provider configs stay outside the repository unless a project-specific decision
states otherwise.

## Module Maturity

Do not treat all modules as equally mature:

- M1 means documented routing and boundaries.
- M2 means structured contracts, registries, configs, or templates exist.
- M3 means executable scripts or Makefile targets validate inputs and write
  traceable outputs.
- M4 means reportable project outputs are reproducible from recorded sources,
  configs, commands, and artifacts.

The current maturity map lives in `tool_catalog.yaml` and
should not be duplicated into scattered local docs.

## Guardrails

- Do not invent data, citations, model metrics, mechanisms, financial facts, or
  causal conclusions.
- Do not use image generation as the source of exact quantitative content.
- Do not commit private data, restricted PDFs, API keys, provider configs, local
  Zotero databases, or generated service configuration.
- Keep outputs under `outputs/`, sources under `metadata/`, choices in
  `configs/`, and reportable run records in `experiments/`.
