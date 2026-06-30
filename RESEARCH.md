# Research Grounding Policy

This file gives agents the research context they should use before changing
analysis logic, evidence records, reports, or figures. It is an operating policy
for automated work, not a restriction on how the repository owner may explore
ideas manually.

## Research Directions

1. Concrete and materials prediction using machine learning and explainable AI.
2. AI industry research and investment research.
3. Future industrial data factor mining and statistical modeling.

## Agent Operating Defaults

- Agents should follow `TOOLCHAIN.md` and `docs/RESEARCH_STACK.md` unless the
  current task gives a more specific instruction.
- Agents should proceed autonomously when the evidence, data path, and output
  type are clear.
- Agents should ask for owner input only when a required source is missing, a
  conclusion would change, credentials or private data are needed, or a heavy
  dependency would be introduced.
- Reportable claims should be traceable to `PROJECT_BRIEF.yaml`,
  `metadata/source_registry.csv`, `metadata/data_manifest.csv`, an experiment
  record, a committed output, or a cited literature source.

## Research Integrity Guardrails

- Do not invent material mechanisms, benchmark values, company facts, market data,
  financial metrics, causal relationships, or experimental results.
- Do not use image generation or PaperVizAgent as the source of exact values,
  axes, error bars, statistical diagnostics, benchmark geometry, or model
  metrics.
- Do not present scratch work as reportable evidence until the source, dataset,
  configuration, code path, and output artifact are recorded.
- Generated or agent-composed figures remain drafts until checked for scientific
  meaning, label accuracy, layout, and source grounding.

## Figure Priorities

For concrete and materials AI work, agents should check whether the figure needs
to show these relationships:

- data source and material system;
- mix design or composition features;
- processing, curing, exposure, or test conditions when relevant;
- prediction target and unit;
- model family and validation protocol;
- XAI output such as SHAP, feature importance, partial dependence, or sensitivity;
- final decision supported by the analysis.

For AI industry and investment research, agents should check whether the figure
needs to show these relationships:

- source type and access date;
- company, sector, region, and time coverage;
- raw indicators and engineered factors;
- statistical model, assumptions, and validation checks;
- investment or strategy claim supported by the evidence;
- uncertainty, caveats, and known source limitations.

For industrial factor mining, agents should check whether the figure needs to
show these relationships:

- unit of analysis;
- time window and refresh cadence;
- factor construction logic;
- leakage controls and validation split;
- statistical diagnostics and robustness checks;
- factor interpretation and downstream decision.

## Figure Decision Rules

- If exact data, axes, error bars, residuals, SHAP values, benchmark numbers, or
  statistical diagnostics are needed, create a figure with a data-grounded
  renderer from source data, committed outputs, or registered experiment
  records.
- Else if the figure communicates a workflow, mechanism hypothesis, architecture,
  or graphical abstract, create a conceptual figure from a figure brief.
- Else if exact evidence and conceptual structure are both needed, render the
  data panels with a data-grounded renderer first and then compose them with
  conceptual panels as a mixed figure.
- Else if multiple academic visual candidates, reference-style refinement, or
  critic feedback would help, use the PaperVizAgent adapter.

## Figure Revision Triggers

Treat a figure as draft and revise it if it:

- adds unsupported numbers, labels, arrows, mechanisms, or causal statements;
- omits required labels from the figure brief;
- treats generated visual style as evidence;
- uses a conceptual image for exact quantitative results;
- hides uncertainty or limitations that are central to the research claim;
- contradicts `PROJECT_BRIEF.yaml` or the active figure brief.
