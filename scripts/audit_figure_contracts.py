from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BRIEF_DIR = ROOT / "examples" / "research_os_project" / "reports" / "paper" / "figures" / "briefs"
ALLOWED_MODES = {"image", "plot", "mixed"}
REQUIRED_BRIEF_FIELDS = {
    "id",
    "title",
    "figure_type",
    "mode",
    "paper_claim",
    "figure_goal",
    "panels",
    "must_keep_labels",
    "forbidden_content",
    "style_constraints",
    "verification_checklist",
}
ROOT_CONTRACT_MARKERS = {
    "AGENTS.md": [
        "Research Foundry",
        "tool_fabric/",
        "No nested AGENTS.md",
    ],
    "FOUNDATIONS.md": [
        "Research Foundry",
        "versioned capability export",
        "Tool Fabric",
    ],
    "foundation/contracts/figure_contract.md": [
        "canonical Foundry figure standard",
        "Exact numeric values",
        "AI illustration tools may assist",
    ],
    "tool_fabric/registry/tools.yaml": [
        "matplotlib",
        "papervizagent",
        "shap_plotting",
    ],
}
DATA_PATH_HINTS = (
    "data/",
    "outputs/tables/",
    "outputs/predictions/",
    "outputs/diagnostics/",
    "experiments/",
)
DATA_EXTENSIONS = (
    ".csv",
    ".tsv",
    ".parquet",
    ".xlsx",
    ".xls",
    ".jsonl",
    ".feather",
)


def read_mapping(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw) if path.suffix.lower() == ".json" else yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: figure brief must contain a mapping/object.")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(has_content(item) for item in value.values())
    if isinstance(value, list):
        return any(has_content(item) for item in value)
    return True


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def looks_like_data_reference(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().lower()
    return any(hint in text for hint in DATA_PATH_HINTS) or any(
        extension in text for extension in DATA_EXTENSIONS
    )


def brief_paths(paths: list[Path]) -> list[Path]:
    if paths:
        return [path if path.is_absolute() else ROOT / path for path in paths]
    return sorted(
        path for pattern in ("*.yaml", "*.yml", "*.json") for path in BRIEF_DIR.glob(pattern)
    )


def validate_root_contracts() -> list[str]:
    errors: list[str] = []
    for relative_path, markers in ROOT_CONTRACT_MARKERS.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"{relative_path}: missing root figure contract.")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative_path}: missing hard-gate marker {marker!r}.")
    return errors


def validate_brief(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        brief = read_mapping(path)
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return [str(exc)]

    missing = sorted(REQUIRED_BRIEF_FIELDS - set(brief))
    if missing:
        errors.append(f"{path}: missing required fields {missing}.")

    mode = brief.get("mode")
    if mode not in ALLOWED_MODES:
        errors.append(f"{path}: mode must be one of {sorted(ALLOWED_MODES)}.")
        return errors

    figure_type = str(brief.get("figure_type") or "").strip().lower()
    figure_role = str(brief.get("figure_role") or "").strip().lower()
    data_requirements = mapping(brief.get("data_requirements"))
    plot_spec = mapping(brief.get("plot_spec"))
    output_record = mapping(brief.get("output_record"))

    if mode == "image":
        if figure_type == "data-figure" or figure_role == "data":
            errors.append(f"{path}: mode:image cannot be marked as a data figure.")
        for field_name, value in (
            ("data_requirements", data_requirements),
            ("plot_spec", plot_spec),
        ):
            if has_content(value):
                errors.append(f"{path}: mode:image cannot define {field_name}.")
        if has_content(output_record.get("supporting_tables")):
            errors.append(f"{path}: mode:image cannot require supporting_tables.")
        for index, panel in enumerate(as_list(brief.get("panels")), start=1):
            if isinstance(panel, dict) and looks_like_data_reference(panel.get("evidence_or_data")):
                errors.append(
                    f"{path}: mode:image panel {index} points to data evidence; "
                    "use mode:mixed or mode:plot."
                )

    if mode == "plot":
        if not has_content(data_requirements):
            errors.append(f"{path}: mode:plot requires data_requirements.")
        if not as_list(data_requirements.get("source_paths")):
            errors.append(f"{path}: mode:plot requires data_requirements.source_paths.")
        if not has_content(plot_spec):
            errors.append(f"{path}: mode:plot requires plot_spec.")
        if not has_content(output_record.get("figure_path")):
            errors.append(f"{path}: mode:plot requires output_record.figure_path.")

    if mode == "mixed":
        if not has_content(data_requirements) and not has_content(
            output_record.get("data_panel_paths")
        ):
            errors.append(
                f"{path}: mode:mixed requires data_requirements or output_record.data_panel_paths."
            )
        if not has_content(output_record.get("figure_path")):
            errors.append(f"{path}: mode:mixed requires output_record.figure_path.")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit figure hard gates and briefs.")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional figure brief paths. Defaults to reports/paper/figures/briefs/*.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = brief_paths(args.paths)
    errors = validate_root_contracts()

    if not paths:
        errors.append(f"No figure briefs found under {BRIEF_DIR}.")
    for path in paths:
        errors.extend(validate_brief(path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Figure contract audit passed: {len(paths)} figure brief(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
