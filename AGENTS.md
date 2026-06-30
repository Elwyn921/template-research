# Research Foundry Agent Guide

This repository is an upstream Research Foundry.

It does not control downstream projects. Its job is to maintain reusable packs,
tools, schemas, validators, adapters, templates, profile definitions, figure
contracts, and bootstrap/export mechanisms for downstream ResearchOS projects.

Foundry exports capability assets only. A downstream ResearchOS project keeps
one root `AGENTS.md`, one project `TOOLFLOW.md`, and its own evidence, data,
experiments, claims, figures, manuscript, and release decisions.

## Operating Loop

For each Foundry task:

1. Classify the task as governance, contract, schema, validator, tool registry,
   adapter, pack, profile, blueprint, export tooling, test, or documentation.
2. Read the smallest necessary context from `FOUNDATIONS.md`, `foundation/`,
   `tool_fabric/`, `packs/`, `adapters/`, and `legacy/migration_notes.md`.
3. Change the canonical Foundry asset in its expected location.
4. Verify registry references, export boundaries, pack restrictions, tests, and
   command behavior.
5. Record migration or release-impacting choices in `legacy/migration_notes.md`
   or `release_notes/`.

Ask the owner only when an action is destructive, credentials or private data
are required, an external dependency must be installed, or a project
restructure is unavoidable.

## Canonical Sources

- Foundry scope: `FOUNDATIONS.md` and `foundation/governance/`.
- Research integrity and figure rules: `foundation/contracts/`.
- Tool layer: `tool_fabric/`.
- Capability packs: `packs/`.
- Optional external integrations: `adapters/`.
- Example downstream assets: `examples/`.

`tool_fabric/registry/tools.yaml` is the sole canonical tool registry. Packs,
profiles, adapters, compatibility, dependencies, and deprecations have their
own canonical registries under `tool_fabric/registry/`.

## Guardrails

- No nested `AGENTS.md`.
- No pack may introduce a controller file.
- No adapter may become a workflow controller.
- No tool registry may be duplicated outside `tool_fabric/registry/`.
- No external skill may be installed automatically without explicit request.
- No heavy MLOps stack may be mandatory without documented need.
- No downstream project may dynamically inherit Foundry governance files.
- Export tooling must never overwrite downstream `AGENTS.md` or
  `08_tools/TOOLFLOW.md`.
