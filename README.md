# Research Foundry

Research Foundry is the upstream capability factory for downstream ResearchOS
projects.

It is the single source of truth for reusable:

- capability packs;
- Tool Fabric registries;
- tool adapters;
- activation rules;
- schemas;
- validators;
- templates;
- figure contracts;
- profile definitions;
- bootstrap and export tooling.

It does not own downstream project conclusions, data, experiments, claims,
figures, manuscripts, or release decisions.

## Architecture

```text
template-research / Research Foundry
        |
        v
versioned capability export
        |
        v
ResearchOS project
        |
        v
project-specific evidence, data, experiments, claims, figures, manuscript
```

The Foundry exports selected assets under a downstream project's
`08_tools/foundry/` directory and writes
`08_tools/foundation_manifest.yaml`. It never overwrites downstream
`AGENTS.md` or `08_tools/TOOLFLOW.md`.

## Canonical Locations

| Location | Role |
|---|---|
| `FOUNDATIONS.md` | Foundry-level orientation |
| `foundation/` | Governance, contracts, schemas, templates, validators |
| `tool_fabric/` | The sole canonical tool layer |
| `tool_fabric/registry/tools.yaml` | The sole canonical tool registry |
| `packs/` | Exportable capability packs |
| `adapters/` | Optional external-tool adapter contracts |
| `blueprints/` | Bootstrap blueprints |
| `examples/` | Demonstration downstream project assets only |
| `legacy/` | Migration notes and archived legacy extension docs |

Deprecated root files such as `RESEARCH.md`, `TOOLCHAIN.md`,
`TOOL_MODULES.md`, `FIGURE_GENERATION_CONTRACT.md`, and `tool_catalog.yaml`
are compatibility pointers only. They are not active controllers.

## Commands

```bash
make setup
make test
make lint
make format
make foundry-validate
make tools-list
make tools-show TOOL=matplotlib
make profiles-list PROFILE=concrete_ml
make packs-list
make packs-validate
make tool-plan PROJECT_TYPE=empirical_materials TASK="test domain shift and local calibration" STAGE=experiment
make export-research-os DEST=/path/to/project BASE=base_research DOMAIN=concrete_ml ENHANCEMENTS="advanced_figure"
make pack-diff DEST=/path/to/project PACKS="core_research_os,concrete_ml"
```

The resolver is advisory. It produces one default primary tool path with
conditional enhancements and never creates a downstream workflow controller.

## Export Boundary

`scripts/export_project_capabilities.py` writes only to:

- `<project>/08_tools/foundry/`
- `<project>/08_tools/foundation_manifest.yaml`

It refuses packs that contain controller files such as `AGENTS.md`,
`TOOLFLOW.md`, `RESEARCH.md`, `TOOLCHAIN.md`, `TOOL_MODULES.md`,
`PROJECT_STATE.yaml`, `WORKFLOW_ROUTER.yaml`, or `TOOL_REGISTRY.yaml`.

## First Release

Recommended first Foundry release tag:

```text
v0.1.0-foundry
```
