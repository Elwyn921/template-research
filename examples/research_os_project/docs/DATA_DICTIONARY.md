# Data dictionary

| Dataset | Field | Type | Unit | Definition | Allowed / expected values | Missingness rule | Source |
|---|---|---|---|---|---|---|---|
| DS-001 | entity_id | string | n/a | Demo entity identifier | unique within period | not allowed | SRC-001 |
| DS-001 | period | string | n/a | Observation period | ISO-like label | not allowed | SRC-001 |
| DS-001 | value | float | project-specific | Demo analytical variable | numeric | document policy | SRC-001 |
