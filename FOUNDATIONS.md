# Research Foundry Foundations

Research Foundry is the upstream capability factory for downstream ResearchOS
projects. It owns reusable contracts, schemas, validators, templates, adapters,
tool registries, capability packs, profiles, and controlled export tooling.

It does not own downstream project conclusions, data, claims, manuscripts, or
release decisions.

## One-way relationship

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

A downstream project keeps one root `AGENTS.md` and one project `TOOLFLOW.md`.
Foundry exports selected capability assets only under
`08_tools/foundry/` and a manifest under `08_tools/foundation_manifest.yaml`.

## Canonical layers

- `foundation/` stores reusable governance, contracts, schemas, templates, and
  validators.
- `tool_fabric/` is the only canonical tool layer.
- `packs/` stores exportable capability packs.
- `adapters/` stores adapter contracts for optional external tools.
- `blueprints/` stores project bootstrap blueprints.
- `examples/` stores non-authoritative downstream examples.

No pack, adapter, or exported asset may become a downstream workflow controller.
