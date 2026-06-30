from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from research_foundry.registry import read_yaml


def load_structured(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(raw)
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(raw)
    if suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    raise ValueError(f"Unsupported validation input format: {path}")


def load_schema(schema_path: Path) -> dict[str, Any]:
    schema = read_yaml(schema_path)
    required = schema.get("required_fields")
    if not isinstance(required, list) or not required:
        raise ValueError(f"Schema must define required_fields: {schema_path}")
    return schema


def records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    raise ValueError("Validation input must be an object or a list of objects")


def validate_required_fields(data_path: Path, schema_path: Path) -> list[str]:
    schema = load_schema(schema_path)
    required = [str(field) for field in schema["required_fields"]]
    errors: list[str] = []
    for index, record in enumerate(records(load_structured(data_path)), start=1):
        missing = [
            field for field in required if field not in record or record[field] in (None, "")
        ]
        if missing:
            errors.append(f"{data_path}: record {index} missing required fields {missing}")
    return errors


def validate_figure_spec(data_path: Path, schema_path: Path) -> list[str]:
    errors = validate_required_fields(data_path, schema_path)
    for index, record in enumerate(records(load_structured(data_path)), start=1):
        mode = record.get("mode")
        source_paths = record.get("source_paths") or []
        renderer = str(record.get("renderer") or "").lower()
        if mode == "conceptual" and any(
            key in record for key in ["metrics", "axes", "error_bars", "shap_values"]
        ):
            errors.append(
                f"{data_path}: record {index} conceptual figure contains quantitative fields"
            )
        if mode == "data" and not source_paths:
            errors.append(f"{data_path}: record {index} data figure requires source_paths")
        if mode == "data" and renderer in {"papervizagent", "image_generation"}:
            errors.append(f"{data_path}: record {index} data figure cannot use {renderer}")
    return errors
