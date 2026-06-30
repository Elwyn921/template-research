# Experiment Contract

Every reportable experiment must record:

- experiment ID;
- question or hypothesis;
- dataset ID and version;
- configuration paths;
- random seed where applicable;
- split definition;
- method and baseline;
- metrics and uncertainty where computable;
- generated artifacts;
- conclusion and caveats.

MLflow, DVC, and Optuna are conditional tools. They are activated only when
their trigger conditions in `tool_fabric/registry/tools.yaml` are met.
