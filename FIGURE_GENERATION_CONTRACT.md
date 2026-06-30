# Figure Production Policy

This file defines how agents should produce research figures in this repository.
It covers data figures, conceptual figures, mixed figures, Engineering Figure
Agent, PaperVizAgent, and local plotting. It is a workflow for agents, not a
restriction on the repository owner's manual exploration.

## Context Chain

Before producing a reportable figure, read the relevant subset of:

1. `RESEARCH.md`
2. `PROJECT_BRIEF.yaml`
3. `TOOLCHAIN.md`
4. `docs/PROJECT_SPEC.md`
5. `docs/RESEARCH_STACK.md`
6. `FIGURE_GENERATION_CONTRACT.md`
7. the active figure brief under `reports/paper/figures/briefs/`

For exploratory scratch figures, agents may use a lighter path, but they should
mark the output as exploratory and avoid treating it as evidence in `reports/`.

## Autonomous Figure Loop

Agents should run this loop before asking for owner intervention:

1. Identify the claim the figure is supposed to support.
2. Decide whether the output is a data figure, conceptual figure, or mixed
   figure.
3. Locate the source data, committed output, figure brief, or source note.
4. Select the lightest tool path that preserves traceability.
5. Generate the figure under `outputs/figures/` and any supporting table under
   `outputs/tables/`.
6. Verify labels, units, axes, uncertainty, source grounding, and unsupported
   claims.
7. Record the source files, config, tool path, and verification notes in the
   figure brief, report notes, or experiment registry.

Ask for owner input only when a required dataset/source is missing, the intended
claim is ambiguous, credentials are needed, or two reasonable figure choices
would imply different scientific or investment conclusions.

## Mode Rules

- If the figure contains exact values, axes, units, error bars, model metrics,
  benchmark geometry, SHAP values, residuals, time series, factor returns, or
  statistical diagnostics, create a data figure with local plotting or
  Engineering Figure Agent `plot` mode.
- Else if the figure communicates a workflow, architecture, mechanism
  hypothesis, research pipeline, or graphical abstract, create a conceptual
  figure from a figure brief with Engineering Figure Agent `image` mode.
- Else if exact data panels and conceptual panels are both needed, use `mixed`
  mode: render the exact data panels first, then compose or describe conceptual
  panels around them.
- Else if multi-candidate generation, reference-driven styling, or critic
  refinement would improve an academic illustration, use PaperVizAgent through
  the adapter.

## Professional Data Figure Workflow

For data figures, agents should choose the plot from the claim and data shape:

- Prediction accuracy: observed-vs-predicted scatter, residual-vs-fitted,
  residual distribution, split-aware metrics, and uncertainty intervals when
  available.
- Model comparison: paired or grouped metric plots with validation split,
  confidence intervals, and consistent baselines.
- Explainable AI: SHAP summary/bar/dependence plots, partial dependence,
  sensitivity curves, feature interaction plots when justified, and feature
  names tied to the data dictionary.
- Concrete/materials relationships: response curves or grouped comparisons by
  mix design, binder system, curing age, exposure, testing condition, and target
  unit.
- Statistical modeling: coefficient plots with intervals, diagnostic plots,
  calibration plots, robustness checks, and assumption notes.
- Industrial factor mining: time series, rolling windows, factor distributions,
  quantile spreads, turnover/coverage plots, leakage checks, and out-of-sample
  validation panels.
- AI industry/investment research: sourced time coverage, company/sector/region
  segmentation, indicator construction, uncertainty/caveat annotations, and
  access dates where relevant.

Data figure requirements for agents:

- Use source data or committed outputs for all numeric marks.
- Show units and transformations when they affect interpretation.
- Keep train/validation/test or time split information visible when metrics are
  shown.
- Prefer confidence intervals, error bars, or uncertainty bands when uncertainty
  is material and computable.
- Avoid decorative complexity that hides sample size, outliers, missingness, or
  limitations.
- Save the plotting code, config, output image, and supporting table or summary
  where another agent can reproduce the result.

## Conceptual Figure Workflow

For conceptual figures, agents should:

- start from a figure brief;
- preserve the required vocabulary and `must_keep_labels`;
- keep arrows, modules, and panel order aligned with the brief;
- avoid unsupported mechanisms, numbers, citations, or causal claims;
- use concise labels that a research reader can scan quickly.

## Mixed Figure Workflow

For mixed figures, agents should:

- render exact data panels locally first;
- keep the data panels unchanged during composition except for layout-safe
  resizing;
- make conceptual panels explain the evidence chain rather than replace the
  evidence;
- record both the data-panel source paths and the conceptual prompt or compiled
  input.

## PaperVizAgent Workflow

For PaperVizAgent, compile a repository-grounded input before generation:

```bash
uv run python scripts/build_paperviz_input.py reports/paper/figures/briefs/<brief>.yaml
```

The compiled JSON is the input that should be copied into PaperVizAgent or
placed in a PaperVizAgent dataset split.

If an existing PaperVizAgent image was produced from a loose prompt, agents
should verify it against the brief and either rebuild it or keep it marked as a
draft.

## Figure Output Record

For reportable figures, save or record:

- source figure brief path;
- compiled prompt or PaperVizAgent input JSON path;
- generation tool and mode;
- model/provider and date, if an image model was used;
- final image path under `outputs/figures/`;
- manual verification notes;
- any source data or output tables used by the figure.

## Verification Checklist

Before a figure can be used in a report or paper, confirm:

- the figure claim matches `PROJECT_BRIEF.yaml`;
- all required labels are present and correctly spelled;
- no unsupported numbers or mechanisms were introduced;
- exact plots were generated from local data or committed outputs;
- axes, units, transformations, and split definitions are clear for data figures;
- uncertainty, sample size, and caveats are visible when they affect the claim;
- visual style does not obscure uncertainty or limitations;
- the final figure is referenced from `reports/`, not edited as the only copy of
  a result.
