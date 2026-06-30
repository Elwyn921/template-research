# AI-Native Research Stack

This document is the operating workflow for agents working in this repository.
It should make agents more autonomous: classify the task, choose the lightest
tool path, create the artifact, verify it, and leave enough trace for another
agent to reproduce the work.

It is not a rule that limits the repository owner. It is the default behavior
agents should follow unless the current task gives a better instruction.

## Agent Decision Order

Agents should resolve decisions in this order:

1. The owner's current request.
2. `RESEARCH.md`
3. `PROJECT_BRIEF.yaml`
4. `FIGURE_GENERATION_CONTRACT.md`
5. `TOOL_MODULES.md`
6. `docs/RESEARCH_STACK.md`
7. `tool_catalog.yaml` and `configs/modules.yaml`
8. Active configs, registries, experiment records, and figure briefs.

If these sources conflict, agents should preserve research integrity first:
do not invent data, citations, mechanisms, financial facts, model metrics, or
experimental results.

## Autonomous Work Loop

For every research task, agents should run this loop before asking for help:

1. Classify the task: literature, source registry, data audit, modeling,
   explainability, data figure, conceptual figure, mixed figure, report writing,
   artifact versioning, tool module, or environment setup.
2. Load the minimum context needed from the root policies, project brief,
   registries, configs, experiments, and active figure brief.
3. Choose the lightest workflow that can produce a traceable output.
4. Create or update files in the expected repository location.
5. Verify claims, values, labels, units, citations, data paths, and output paths.
6. Record the reason for important choices in a registry, config, experiment
   record, figure brief, report note, or `docs/DECISIONS.md`.

Agents should interrupt the owner only when:

- a required source, dataset, credential, or domain definition is missing;
- two plausible interpretations would lead to different claims;
- private data, paid APIs, or external accounts are needed;
- adding a heavy tool or restructuring the project is the only reasonable path;
- the available evidence cannot support the requested scientific, investment, or
  causal conclusion.

## Research Scope

Agent work should default to these directions:

1. Concrete/materials prediction using machine learning and explainable AI.
2. AI industry research and investment research.
3. Future industrial data factor mining and statistical modeling.

If a task falls outside the scope, agents should still help when the owner asks,
but keep outputs separated and avoid silently changing the research direction.

## Recommended Installation Order

Start light and add tools only when the workflow needs them.

1. Base repository environment:
   - `uv sync --group dev`
   - `uv run pytest`
   - `uv run ruff check .`
2. Local literature layer:
   - Zotero for the reference library.
   - ZotSeek only when local semantic retrieval over Zotero becomes useful.
3. Selected K-Dense skills:
   - install only task-relevant skills, not the full collection.
   - first choices: `paper-lookup`, `citation-management`,
     `scientific-writing`, `scientific-visualization`,
     `statistical-analysis`, `statsmodels`, `scikit-learn`, `shap`,
     `exploratory-data-analysis`, `experimental-design`,
     `statistical-power`, and `database-lookup`.
4. Figure tooling:
   - Engineering Figure Agent for `plot`, `image`, and `mixed` figure work.
   - PaperVizAgent adapter when multi-candidate academic illustration,
     reference-driven style, or critic refinement is useful.
5. DVC:
   - add only when datasets, model artifacts, predictions, or experiment outputs
     outgrow Git or need artifact checkout.
6. Quarto:
   - add later when reports need one-command regeneration from committed
     outputs.

For module selection, use `tool_catalog.yaml` and `configs/modules.yaml`.
Install optional dependency groups with `make setup EXTRAS="..."` only after the
selected profile or task justifies them.

This stack intentionally avoids Kedro, MLflow, Kubeflow, Airflow, Prefect,
Dagster, feature stores, model registries, dashboards, and long-running
orchestration unless a concrete need is documented.

## Repository Architecture

```text
template-research/
├── AGENTS.md                         # agent playbook
├── FIGURE_GENERATION_CONTRACT.md     # figure production workflow
├── PROJECT_BRIEF.yaml                # research scope and claims
├── RESEARCH.md                       # root research context
├── TOOLCHAIN.md                      # root tool routing policy
├── TOOL_MODULES.md                   # root tool-module activation contract
├── configs/                          # parameters that affect results
├── data/                             # raw, interim, processed, sample data
├── docs/                             # workflow, decisions, reproducibility
├── experiments/                      # run registry and failed experiments
├── extensions/
│   ├── dvc/                          # optional artifact versioning guide
│   ├── engineering-figure-agent/     # data, conceptual, and mixed figure guide
│   ├── papervizagent/                # constrained PaperVizAgent adapter
│   └── quarto/                       # optional reporting layer guide
├── metadata/                         # source/data registries and schemas
├── notebooks/                        # exploration, not the only pipeline copy
├── outputs/                          # generated figures/tables/models/etc.
├── reports/                          # memos, manuscript sources, slides
├── scripts/                          # repository utilities
├── src/                              # reusable research code
├── tests/                            # checks for reusable code
└── tool_catalog.yaml                 # opt-in modules, profiles, and upstream links
```

Agents should keep this architecture stable. Add subfolders when they clarify
research outputs; avoid broad restructuring for a single task.

## Tool-To-Task Mapping

| Task | Agent default | Repository record |
|---|---|---|
| Research scope | Update project brief/spec | `PROJECT_BRIEF.yaml`, `docs/PROJECT_SPEC.md` |
| Source tracking | Register sources as evidence | `metadata/source_registry.csv` |
| Dataset release | Register dataset and lineage | `metadata/data_manifest.csv` |
| Literature library | Zotero | Zotero collection/export as needed |
| Local semantic retrieval | ZotSeek | Search note in `reports/memos/` |
| External paper discovery | K-Dense `paper-lookup` | source registry and citation notes |
| Citation cleanup | Zotero plus `citation-management` | report-local BibTeX/CSL when needed |
| Concrete/materials ML | pandas, scikit-learn, SHAP, stats checks | `configs/`, `src/`, `experiments/`, `outputs/` |
| AI industry/investment research | sourced indicators, Zotero/ZotSeek, statsmodels | `metadata/`, `reports/memos/`, `outputs/tables/` |
| Industrial factor mining | statsmodels/statistical-analysis, leakage checks | `configs/`, `experiments/`, `outputs/` |
| Experimental design | K-Dense `experimental-design`, `statistical-power` | `docs/PROJECT_SPEC.md`, `reports/memos/` |
| Data figures | data-grounded renderer | `outputs/figures/`, `outputs/tables/` |
| Conceptual figures | Engineering Figure Agent `image` | figure brief, output image, verification note |
| Mixed figures | data-grounded panels plus conceptual composition | data panel paths, brief, final figure |
| PaperVizAgent figures | compiled adapter input | `outputs/figures/papervizagent/.../input.json` |
| Reproducible reports | Markdown first, Quarto later | `reports/` |
| Large artifacts | Git first, DVC when needed | manifest plus optional `*.dvc` |
| Tool module selection | Catalog plus profile | `tool_catalog.yaml`, `configs/modules.yaml` |

## Literature Workflow

- If the task is collecting papers, add them to Zotero and keep collections
  aligned with research questions.
- If the task is finding papers already in the local library, use ZotSeek when
  available and summarize query, top hits, and relevance.
- If the task needs external discovery, use selected K-Dense literature skills
  and record useful results in `metadata/source_registry.csv`.
- If the paper supports a reportable claim, capture citation key, title, year,
  DOI/URL, source type, access date, and the claim it supports.
- If a result is only background reading, keep it in memo notes rather than
  inflating the source registry.

## Data And Modeling Workflow

- If data arrives, put immutable copies under `data/raw/` or `data/external/`
  and register them in `metadata/data_manifest.csv`.
- If data are cleaned or transformed, write code in `src/` or `scripts/`, store
  parameters in `configs/`, and write outputs under `data/interim/` or
  `data/processed/`.
- If a result becomes reportable, add an experiment record before presenting it
  as evidence.
- If the workflow is concrete/materials prediction, track material system,
  mix-design features, processing/curing/test conditions, target unit, split
  strategy, model family, metrics, uncertainty, and XAI outputs.
- If the workflow is industry/investment research, track company, sector,
  region, time coverage, source dates, raw indicators, factor construction,
  assumptions, caveats, and validation checks.
- If the workflow is factor mining, track unit of analysis, time window, refresh
  cadence, leakage controls, validation split, diagnostics, robustness, and the
  downstream decision.

## Professional Data Figure Workflow

Data figures are first-class outputs. Agents should not treat them as generic
images.

### General Data Figure If/Else

- If the figure supports a numeric claim, inspect the data and claim before
  choosing the chart.
- If the figure compares groups, show group definitions, sample sizes, metric
  units, and uncertainty where computable.
- If the figure shows a relationship, show axes with units, transformations, and
  outlier/missingness handling when relevant.
- If the figure reports model performance, show split definitions, baseline,
  metric formula or name, and uncertainty or variability when available.
- If the figure supports a causal or investment interpretation, show assumptions,
  time coverage, caveats, and robustness checks instead of relying on a single
  decorative chart.
- If exact numeric content is needed, generate marks from source data, committed
  outputs, or registered experiment records only.

### Concrete/Materials AI Figures

- If the claim is prediction accuracy, use observed-vs-predicted parity plots,
  residual-vs-fitted plots, residual distributions, split-aware metrics, and
  uncertainty intervals when available.
- If the claim is material insight, use SHAP summary/bar/dependence plots,
  partial dependence, sensitivity curves, and grouped response curves tied to
  mix-design variables.
- If the claim involves material conditions, facet or color by binder system,
  curing age, exposure, test condition, or material class when data supports it.
- If the claim involves comparison across models, use consistent validation
  splits and paired/grouped metric plots with baselines.
- If the model is used for decision support, include uncertainty, constraints,
  and the decision boundary or screening rule when available.

### AI Industry And Investment Figures

- If the claim is market or company trend, show source date, time coverage,
  company/sector/region segmentation, and missing data notes.
- If the claim is factor construction, show raw indicator coverage, normalized
  factor distribution, transformation, and outlier treatment.
- If the claim is strategy or investment relevance, show rolling performance,
  drawdown, quantile spread, information coefficient, turnover, and robustness
  rather than a single cumulative line.
- If the data source may revise, show access date and version where possible.

### Industrial Factor Mining Figures

- If the claim is factor validity, show factor distribution, coverage,
  correlation, leakage checks, out-of-sample validation, and robustness panels.
- If the claim is temporal stability, show rolling statistics, regime changes,
  refresh cadence, and missingness.
- If the claim supports downstream operations, show threshold logic, error bands,
  confusion/cost matrix, or decision table when relevant.

### Data Figure Output Record

For reportable data figures, agents should save or record:

- input dataset or committed output path;
- code path or notebook path used to generate the plot;
- config path and run/experiment id when relevant;
- final image path under `outputs/figures/`;
- supporting table path under `outputs/tables/` when metrics are shown;
- units, transformations, split definitions, and uncertainty method;
- verification notes for missingness, outliers, labels, and claim alignment.

## Conceptual, Mixed, And PaperVizAgent Workflow

- If the output is a workflow, architecture diagram, schematic, or graphical
  abstract, create or update a figure brief under
  `reports/paper/figures/briefs/`.
- If Engineering Figure Agent is available, use it as the default tool for
  `plot`, `image`, and `mixed` figure modes.
- If the output has exact data panels and conceptual panels, render exact data
  panels with a data-grounded renderer first and use `mixed` mode for the
  composition.
- If the output benefits from multiple candidates, reference-driven style, or
  critic refinement, use PaperVizAgent through the adapter:

  ```bash
  uv run python scripts/build_paperviz_input.py reports/paper/figures/briefs/<brief>.yaml
  ```

- If the starting point is a loose visual idea, convert it into a brief before
  using PaperVizAgent.
- If PaperVizAgent output does not match the brief, keep it as draft and revise
  the brief or generated image before report use.
- PaperVizAgent and image-generation tools must not create exact numeric data
  plots from imagination. `mode: plot` briefs must use a data-grounded renderer,
  not PaperVizAgent.

## Tool Risks And Maintenance Costs

| Tool | Useful for | Main risks | Maintenance cost |
|---|---|---|---|
| Zotero | reference library and citation spine | local database is not a Git artifact; PDFs may be restricted | low |
| ZotSeek | semantic retrieval over local papers | index drift; results depend on local library quality | low-medium |
| K-Dense selected skills | targeted paper lookup, writing, statistics, SHAP, visualization | installing too many skills creates prompt/tool noise | medium |
| Engineering Figure Agent | data plots, conceptual diagrams, mixed figures | wrong mode can blur data vs concept boundaries | medium |
| PaperVizAgent adapter | graphical abstracts, multi-candidate academic visuals | loose prompts may ignore research context; output still needs verification | medium |
| DVC | large datasets, model artifacts, predictions | remote setup, storage permissions, metadata churn | medium |
| Quarto | reproducible reporting | can hide analysis logic inside reports if introduced too early | medium |

## Minimal First Implementation

The current repository should start with this minimal stack:

1. Keep the base Python/uv workflow and existing registries.
2. Use Zotero manually for library organization; add ZotSeek only when local
   semantic paper retrieval is needed.
3. Use selected K-Dense skills only for the task at hand.
4. Use data-grounded rendering for exact data figures.
5. Use figure briefs for conceptual or mixed figures.
6. Use `scripts/build_paperviz_input.py` only when PaperVizAgent is useful.
7. Keep DVC and Quarto as opt-in layers until artifacts or reports require them.

This gives agents enough structure to work intelligently without turning the
repository into a heavy MLOps system.

## Output Quality Checklist

Before calling an output reportable, agents should check:

- The claim links back to the project brief or a clearly recorded task.
- Sources are registered or cited in report notes.
- Datasets and derived outputs have paths and versions.
- Configs and experiment choices are not hidden in notebook state.
- Figures distinguish exact data marks from conceptual graphics.
- Data figures include units, split definitions, uncertainty/caveats, and
  supporting tables when needed.
- Generated conceptual figures preserve required labels and avoid unsupported
  scientific or financial claims.
- Private data, restricted PDFs, API keys, provider configs, and local Zotero
  databases are not committed.
