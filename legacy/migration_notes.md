# Research Foundry migration notes

Date: 2026-06-30

This repository was migrated from a downstream-style reproducible research
template into the upstream Research Foundry for reusable ResearchOS capability
packs, tool registry entries, adapters, validators, schemas, templates, and
export tooling.

## Current-state diagnosis

The pre-migration repository mixed reusable template assets with active
project-runtime controls:

- `AGENTS.md` governed downstream research execution, tool routing, data figure
  workflow, and project artifact locations.
- `RESEARCH.md` stored reusable integrity rules together with project research
  directions.
- `TOOLCHAIN.md` duplicated tool routing policy already represented in
  `TOOL_MODULES.md`, `tool_catalog.yaml`, and `configs/modules.yaml`.
- `TOOL_MODULES.md` duplicated figure routing, module activation, optional
  dependency policy, and module maturity rules.
- `tool_catalog.yaml` was the closest machine-readable source, but it modeled
  modules rather than individual tools, adapters, profiles, packs, dependency
  risks, and export policy.
- `configs/modules.yaml` represented project runtime state, which does not
  belong in an upstream Foundry.
- `FIGURE_GENERATION_CONTRACT.md` duplicated figure hard gates across
  `AGENTS.md`, `RESEARCH.md`, `TOOLCHAIN.md`, `TOOL_MODULES.md`,
  `docs/RESEARCH_STACK.md`, and figure brief validation.
- `extensions/` held useful adapter guidance but was not normalized into a
  canonical adapter registry.
- `data/`, `metadata/`, `experiments/`, and `reports/` contained useful
  demonstration assets, but those are example downstream assets rather than
  Foundry-level state.

Useful assets preserved during migration:

- Local data figure builder: `scripts/build_data_figure.py`.
- Constrained PaperVizAgent input compiler: `scripts/build_paperviz_input.py`.
- Existing figure brief hard gates and tests.
- Registry audit ideas from `scripts/audit_registry.py` and
  `scripts/audit_tool_modules.py`.
- Demo dataset validation helpers from `src/research_project/`.
- Extension documentation for DVC, Engineering Figure Agent, PaperVizAgent, and
  Quarto.
- Metadata schemas for figure briefs and PaperVizAgent input.
- Sample data, experiment registry shape, and source/data manifest examples.

## Migration map

| Legacy location | New canonical location | New role |
|---|---|---|
| `RESEARCH.md` | `foundation/contracts/research_integrity.md` | Reusable integrity contract |
| `TOOLCHAIN.md` | `tool_fabric/TOOL_FABRIC.md` | Tool Fabric explanation only |
| `TOOL_MODULES.md` | `tool_fabric/registry/*.yaml` | Pointer to canonical registries |
| `tool_catalog.yaml` | `tool_fabric/registry/tools.yaml` | Canonical tool registry |
| `configs/modules.yaml` | `tool_fabric/registry/profiles.yaml` and examples | Profile examples, not runtime state |
| `FIGURE_GENERATION_CONTRACT.md` | `foundation/contracts/figure_contract.md` | Canonical Foundry figure contract |
| `extensions/` | `adapters/` | Reusable adapter specifications |
| `data/`, `metadata/`, `experiments/`, `reports/` | `examples/research_os_project/` | Demonstration downstream assets |
| `src/research_project/` | `src/research_foundry/` | Reusable Foundry code |
| `scripts/audit_tool_modules.py` | `scripts/validate_foundry.py`, `scripts/list_tools.py` | Foundry validation and listing |
| `scripts/audit_figure_contracts.py` | `foundation/validators/validate_figure_assets.py` | Foundry figure asset validation |

## Deprecated root controllers

The following root files are retained only as compatibility pointers and must
not define active tool routing or project-runtime policy:

- `RESEARCH.md`
- `TOOLCHAIN.md`
- `TOOL_MODULES.md`
- `FIGURE_GENERATION_CONTRACT.md`
- `tool_catalog.yaml`
- `configs/modules.yaml`

Canonical policy now lives under:

- `foundation/`
- `tool_fabric/`
- `packs/`
- `adapters/`
- `blueprints/`

No nested `AGENTS.md` files were introduced.
