# Governed extension: Quarto

Agents should enable Quarto when a report, memo, or manuscript must be rebuilt
from code and generated outputs rather than copied manually from notebooks. If
an agent enables Quarto earlier, it should record the reporting need and keep
model logic outside the report.

`reports/*.qmd` should consume material from `outputs/`, not reproduce model logic inline.
