# Figure Contract

This is the canonical Foundry figure standard.

## Figure modes

- Data figures contain exact values, axes, units, confidence intervals, error
  bars, model metrics, residuals, SHAP values, time series, factor returns, or
  quantitative annotations.
- Conceptual figures communicate workflow, architecture, mechanism hypotheses,
  system diagrams, or graphical abstracts without exact quantitative marks.
- Mixed figures combine exact data panels and conceptual panels.

## Non-negotiable gates

Exact numeric values, axes, confidence intervals, error bars, metrics,
residuals, SHAP values, time series, factor returns, and quantitative
annotations must be produced by data-grounded rendering from source data,
committed outputs, or registered experiment records.

Conceptual figures may use illustration tools, but final assets must remain
editable through SVG, Graphviz, draw.io, Figma, Inkscape, or another editable
source path.

Mixed figures must render quantitative panels separately before conceptual
composition. Quantitative panels may only be resized or arranged during
composition; their data marks must not be redrawn by image generation.

AI illustration tools may assist with layout, style, mechanism sketches, and
concept drafting. They must never fabricate:

- data values;
- axes;
- experimental measurements;
- error bars;
- model performance metrics;
- statistical significance;
- quantitative evidence.

## Reportable figure record

Publication quantitative figures must preserve:

- source code;
- source data;
- PDF;
- SVG;
- PNG preview;
- caption;
- linked result ID;
- linked claim ID.

Use `foundation/validators/validate_figure_assets.py` or
`make foundry-validate` after changing figure policy, figure schemas, or
reportable figure assets.
