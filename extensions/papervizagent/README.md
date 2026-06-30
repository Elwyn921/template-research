# Governed extension: PaperVizAgent

PaperVizAgent is an optional enhancement for academic visual workflows. In this
repository, agents should use it when a figure benefits from multi-candidate
generation, reference-driven style, graphical abstract exploration, or
critic-based refinement.

It is not the default path for exact data figures.

## Agent Routing

- If the task is an exact data figure, use a data-grounded renderer such as the
  local builder, Engineering Figure Agent `plot` mode, Altair/Vega-Lite,
  Plotly, Observable Plot, Quarto, or another audited path.
- If the task is a conceptual figure and one candidate is enough, use
  Engineering Figure Agent `image` mode from a figure brief.
- If the task needs mixed exact data panels and conceptual panels, render data
  panels with a data-grounded renderer first and then compose through `mixed`
  mode.
- If the task needs multiple academic candidates, visual refinement, or
  reference-style exploration, use PaperVizAgent through the adapter.

## Adapter Flow

Build a repository-grounded input before using PaperVizAgent:

```bash
uv run python scripts/build_paperviz_input.py reports/paper/figures/briefs/<brief>.yaml
```

The generated file is written to:

```text
outputs/figures/papervizagent/<brief-name>/input.json
```

Use that JSON as the PaperVizAgent demo input or copy it into a PaperVizAgent
dataset split.

The adapter must not be used for `mode: plot` briefs. The build script refuses
those inputs so exact data figures stay on the data-grounded path.

If the starting point is a loose prompt, agents should convert it into a figure
brief first. If an existing PaperVizAgent output was created from a loose prompt,
agents should treat it as a draft, verify it against the brief and root research
policies, and rebuild it when the mismatch affects the claim.

## Expected PaperVizAgent Fields

The adapter emits:

- `filename`
- `caption`
- `content`
- `visual_intent`
- `additional_info.rounded_ratio`
- `additional_info.source_files`
- `max_critic_rounds`

The `content` and `visual_intent` fields include:

- `RESEARCH.md`
- `TOOLCHAIN.md`
- `PROJECT_BRIEF.yaml`
- `FIGURE_GENERATION_CONTRACT.md`
- `docs/RESEARCH_STACK.md`
- the active figure brief
- data requirements, plot specification, labels, forbidden content, style
  constraints, verification checklist, and output record

## Useful PaperVizAgent Tasks

- graphical abstracts;
- academic workflow diagrams;
- reference-driven figure styling;
- multi-candidate visual exploration;
- critic-based refinement.

## Boundary

PaperVizAgent must not be used as the source of exact values, axes, units,
model metrics, error bars, residuals, SHAP values, factor returns, or
statistical diagnostics. Those must come from source data, committed outputs, or
registered experiment records.

## Installing PaperVizAgent Externally

Keep the upstream PaperVizAgent repository outside this project or add it as a
separate tool checkout. Do not vendor API keys or provider configs into this
template.

Typical external flow:

```bash
git clone https://github.com/google-research/papervizagent.git ../papervizagent
cd ../papervizagent
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp configs/model_config.template.yaml configs/model_config.yaml
```

Then use this repository's compiled input JSON as the source content.
