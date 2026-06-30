# Pack Policy

Capability packs may contain reusable tools, schemas, templates, validators,
scripts, figures, checklists, and documentation.

Capability packs must not contain:

- `AGENTS.md`;
- `TOOLFLOW.md`;
- `RESEARCH.md`;
- `TOOLCHAIN.md`;
- `TOOL_MODULES.md`;
- `PROJECT_STATE.yaml`;
- `WORKFLOW_ROUTER.yaml`;
- `TOOL_REGISTRY.yaml`;
- project-specific claims;
- project-specific manuscript conclusions;
- a stage controller or workflow router.

Every pack must map its required and optional tools to
`tool_fabric/registry/tools.yaml`.
