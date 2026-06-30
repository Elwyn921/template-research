from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Figure brief not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Figure brief must be a YAML object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def slugify(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def has_placeholder(path_text: str) -> bool:
    return "<" in path_text or ">" in path_text


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def existing_source_paths(brief: dict[str, Any]) -> list[Path]:
    data_requirements = brief.get("data_requirements") or {}
    source_paths = as_list(data_requirements.get("source_paths"))
    existing: list[Path] = []
    placeholders: list[str] = []
    missing: list[str] = []
    for raw_path in source_paths:
        path_text = str(raw_path)
        if has_placeholder(path_text):
            placeholders.append(path_text)
            continue
        path = resolve_repo_path(path_text)
        if path.is_file():
            existing.append(path)
        else:
            missing.append(path_text)
    if existing:
        return existing
    detail = []
    if placeholders:
        detail.append(f"placeholder paths: {placeholders}")
    if missing:
        detail.append(f"missing paths: {missing}")
    suffix = "; ".join(detail) if detail else "no source_paths defined"
    raise SystemExit(f"No usable data source found in figure brief ({suffix}).")


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise SystemExit(f"Unsupported table format for data figure: {path}")


def output_path_for(brief: dict[str, Any], out_arg: Path | None) -> Path:
    if out_arg:
        return out_arg if out_arg.is_absolute() else ROOT / out_arg
    output_record = brief.get("output_record") or {}
    figure_path = output_record.get("figure_path")
    if isinstance(figure_path, str) and figure_path and not has_placeholder(figure_path):
        return resolve_repo_path(figure_path)
    brief_id = str(brief.get("id") or brief.get("title") or "data-figure")
    return ROOT / "outputs" / "figures" / f"{slugify(brief_id)}.png"


def column_label(column: str, units: dict[str, Any]) -> str:
    unit = units.get(column)
    return f"{column} ({unit})" if unit else column


def require_columns(frame: pd.DataFrame, columns: list[str]) -> None:
    needed = [column for column in columns if column]
    missing = [column for column in needed if column not in frame.columns]
    if missing:
        raise SystemExit(f"Data figure source is missing required columns: {missing}")


def apply_axes_style(axis: Any) -> None:
    axis.grid(True, color="#d9dee7", linewidth=0.7, alpha=0.7)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def split_groups(frame: pd.DataFrame, color_column: str | None) -> list[tuple[str, pd.DataFrame]]:
    if color_column and color_column in frame.columns:
        return [(str(name), group) for name, group in frame.groupby(color_column, dropna=False)]
    return [("all", frame)]


def annotate_metrics(axis: Any, metrics_frame: pd.DataFrame | None) -> None:
    if metrics_frame is None or metrics_frame.empty:
        return
    text_lines: list[str] = []
    lower_columns = {column.lower(): column for column in metrics_frame.columns}
    metric_col = lower_columns.get("metric")
    value_col = lower_columns.get("value")
    split_col = lower_columns.get("split")
    if metric_col and value_col:
        for _, row in metrics_frame.head(8).iterrows():
            prefix = f"{row[split_col]} " if split_col else ""
            text_lines.append(f"{prefix}{row[metric_col]}={row[value_col]:.3g}")
    elif len(metrics_frame.columns) <= 6:
        text_lines.append(metrics_frame.head(4).to_string(index=False))
    if text_lines:
        axis.text(
            0.03,
            0.97,
            "\n".join(text_lines),
            transform=axis.transAxes,
            va="top",
            ha="left",
            fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#c9d1dc", "alpha": 0.88},
        )


def find_metrics_table(paths: list[Path]) -> pd.DataFrame | None:
    for path in paths:
        if "metric" in path.stem.lower():
            return read_table(path)
    return None


def find_shap_table(paths: list[Path]) -> pd.DataFrame | None:
    for path in paths:
        if "shap" in path.stem.lower():
            return read_table(path)
    return None


def plot_prediction_diagnostics(
    frame: pd.DataFrame,
    source_paths: list[Path],
    brief: dict[str, Any],
    output_path: Path,
) -> None:
    import matplotlib.pyplot as plt

    data_requirements = brief.get("data_requirements") or {}
    units = data_requirements.get("units") or {}
    plot_spec = brief.get("plot_spec") or {}
    x_col = str(plot_spec.get("x") or "y_true")
    y_col = str(plot_spec.get("y") or "y_pred")
    color_col = plot_spec.get("color")
    residual_col = "residual" if "residual" in frame.columns else None
    require_columns(frame, [x_col, y_col])
    if residual_col is None:
        frame = frame.copy()
        residual_col = "residual"
        frame[residual_col] = frame[x_col] - frame[y_col]

    shap_frame = find_shap_table(source_paths)
    metrics_frame = find_metrics_table(source_paths)
    panel_count = 4 if shap_frame is not None and not shap_frame.empty else 3
    fig, axes = plt.subplots(
        1, panel_count, figsize=(5.2 * panel_count, 4.6), constrained_layout=True
    )
    if panel_count == 1:
        axes = [axes]

    groups = split_groups(frame, str(color_col) if color_col else None)
    for label, group in groups:
        axes[0].scatter(group[x_col], group[y_col], s=36, alpha=0.78, label=label)
    low = min(frame[x_col].min(), frame[y_col].min())
    high = max(frame[x_col].max(), frame[y_col].max())
    axes[0].plot([low, high], [low, high], color="#2f3542", linewidth=1.1, linestyle="--")
    axes[0].set_xlabel(column_label(x_col, units))
    axes[0].set_ylabel(column_label(y_col, units))
    axes[0].set_title("Prediction parity")
    if len(groups) > 1:
        axes[0].legend(title=str(color_col), frameon=False, fontsize=8)
    annotate_metrics(axes[0], metrics_frame)

    for label, group in groups:
        axes[1].scatter(group[y_col], group[residual_col], s=32, alpha=0.76, label=label)
    axes[1].axhline(0, color="#2f3542", linewidth=1.0, linestyle="--")
    axes[1].set_xlabel(column_label(y_col, units))
    axes[1].set_ylabel(column_label(residual_col, units))
    axes[1].set_title("Residuals")

    axes[2].hist(frame[residual_col].dropna(), bins="auto", color="#4c78a8", alpha=0.84)
    axes[2].axvline(0, color="#2f3542", linewidth=1.0, linestyle="--")
    axes[2].set_xlabel(column_label(residual_col, units))
    axes[2].set_ylabel("Count")
    axes[2].set_title("Residual distribution")

    if panel_count == 4 and shap_frame is not None:
        numeric = shap_frame.select_dtypes("number")
        if numeric.empty:
            axes[3].text(0.5, 0.5, "No numeric SHAP values", ha="center", va="center")
        else:
            top = numeric.abs().mean().sort_values(ascending=True).tail(12)
            axes[3].barh(top.index, top.values, color="#59a14f", alpha=0.86)
            axes[3].set_xlabel("Mean absolute SHAP value")
        axes[3].set_title("SHAP / XAI")

    for axis in axes:
        apply_axes_style(axis)
    fig.suptitle(str(brief.get("caption") or brief.get("title") or "Data figure"), fontsize=12)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_generic_data_figure(frame: pd.DataFrame, brief: dict[str, Any], output_path: Path) -> None:
    import matplotlib.pyplot as plt

    data_requirements = brief.get("data_requirements") or {}
    units = data_requirements.get("units") or {}
    plot_spec = brief.get("plot_spec") or {}
    chart_family = str(plot_spec.get("chart_family") or "relationship").lower()
    x_col = plot_spec.get("x")
    y_col = plot_spec.get("y")
    color_col = plot_spec.get("color")
    require_columns(frame, [column for column in [x_col, y_col, color_col] if column])

    fig, axis = plt.subplots(figsize=(8.5, 5.2), constrained_layout=True)
    groups = split_groups(frame, str(color_col) if color_col else None)

    if chart_family in {"distribution", "histogram"}:
        value_col = str(y_col or x_col)
        require_columns(frame, [value_col])
        for label, group in groups:
            axis.hist(group[value_col].dropna(), bins="auto", alpha=0.62, label=label)
        axis.set_xlabel(column_label(value_col, units))
        axis.set_ylabel("Count")
    elif chart_family in {"time-series", "timeseries", "line"}:
        require_columns(frame, [str(x_col), str(y_col)])
        for label, group in groups:
            axis.plot(group[str(x_col)], group[str(y_col)], marker="o", linewidth=1.6, label=label)
        axis.set_xlabel(column_label(str(x_col), units))
        axis.set_ylabel(column_label(str(y_col), units))
    elif chart_family in {"bar", "model-comparison"}:
        require_columns(frame, [str(x_col), str(y_col)])
        axis.bar(frame[str(x_col)].astype(str), frame[str(y_col)], color="#4c78a8", alpha=0.86)
        axis.set_xlabel(column_label(str(x_col), units))
        axis.set_ylabel(column_label(str(y_col), units))
        axis.tick_params(axis="x", rotation=30)
    else:
        require_columns(frame, [str(x_col), str(y_col)])
        for label, group in groups:
            axis.scatter(group[str(x_col)], group[str(y_col)], s=36, alpha=0.78, label=label)
        axis.set_xlabel(column_label(str(x_col), units))
        axis.set_ylabel(column_label(str(y_col), units))

    if len(groups) > 1:
        axis.legend(title=str(color_col), frameon=False)
    axis.set_title(str(brief.get("caption") or brief.get("title") or "Data figure"))
    apply_axes_style(axis)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_sidecar(brief: dict[str, Any], source_paths: list[Path], output_path: Path) -> None:
    record = {
        "figure_id": brief.get("id"),
        "figure_type": brief.get("figure_type"),
        "mode": brief.get("mode"),
        "source_paths": [path.relative_to(ROOT).as_posix() for path in source_paths],
        "output_path": output_path.relative_to(ROOT).as_posix(),
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "verification_checklist": as_list(brief.get("verification_checklist")),
    }
    sidecar_path = output_path.with_suffix(output_path.suffix + ".json")
    sidecar_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local data figure from a figure brief.")
    parser.add_argument("brief", type=Path, help="Figure brief YAML path.")
    parser.add_argument("--out", type=Path, help="Output image path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brief_path = args.brief if args.brief.is_absolute() else ROOT / args.brief
    brief = read_yaml(brief_path)
    if brief.get("mode") not in {"plot", "mixed"}:
        raise SystemExit("Data figure builder expects a figure brief with mode: plot or mixed.")
    source_paths = existing_source_paths(brief)
    frame = read_table(source_paths[0])
    data_requirements = brief.get("data_requirements") or {}
    require_columns(
        frame, [str(column) for column in as_list(data_requirements.get("required_columns"))]
    )
    output_path = output_path_for(brief, args.out)
    chart_family = str((brief.get("plot_spec") or {}).get("chart_family") or "").lower()
    if chart_family == "prediction-diagnostics":
        plot_prediction_diagnostics(frame, source_paths, brief, output_path)
    else:
        plot_generic_data_figure(frame, brief, output_path)
    write_sidecar(brief, source_paths, output_path)
    print(f"Wrote data figure: {output_path}")
    print(f"Wrote data figure record: {output_path.with_suffix(output_path.suffix + '.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
