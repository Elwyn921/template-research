# Tool Fabric

Tool Fabric is the single canonical Research Foundry tool layer.

It decides:

- what tools exist;
- what each tool can do;
- when each tool is appropriate;
- what inputs it expects;
- what outputs it produces;
- what packs or profiles may use it;
- what dependencies it needs;
- what risks or overlaps it has;
- whether it is optional, installed, experimental, deprecated, or blocked.

It does not decide a downstream project's research question, stage progression,
core claim, manuscript logic, final result, or release decision.

Canonical registries:

- `tool_fabric/registry/tools.yaml`
- `tool_fabric/registry/packs.yaml`
- `tool_fabric/registry/profiles.yaml`
- `tool_fabric/registry/adapters.yaml`
- `tool_fabric/registry/compatibility_matrix.yaml`
- `tool_fabric/registry/dependency_matrix.yaml`
- `tool_fabric/registry/deprecation_registry.yaml`

Resolvers are advisory. They produce a recommended capability plan without
creating a project-level workflow controller.
