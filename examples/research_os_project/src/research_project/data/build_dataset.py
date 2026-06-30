from __future__ import annotations

from pathlib import Path

import pandas as pd

from research_project.data.validate import validate_duplicate_key, validate_required_columns


def build_dataset(
    input_path: Path, output_path: Path, required_columns: list[str], duplicate_key: list[str]
) -> pd.DataFrame:
    """Validate a source table and write a clean, deterministic demo dataset."""
    frame = pd.read_csv(input_path)
    validate_required_columns(frame, required_columns)
    validate_duplicate_key(frame, duplicate_key)
    cleaned = frame.sort_values(duplicate_key).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    return cleaned
