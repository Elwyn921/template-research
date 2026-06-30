# Compatibility Policy

Compatibility is defined by `tool_fabric/registry/compatibility_matrix.yaml`.

Profiles are advisory bundles, not workflow controllers. A downstream project
may activate:

- one base profile;
- one domain profile;
- at most two conditional enhancement profiles.

If tool or pack conflicts occur, downstream project `TOOLFLOW.md` wins. If no
project override exists, the Tool Fabric uses `default_priority` in
`tools.yaml`. If neither resolves the conflict, human selection is required.
