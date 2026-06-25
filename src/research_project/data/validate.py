from __future__ import annotations

import pandas as pd


def validate_required_columns(frame: pd.DataFrame, required_columns: list[str]) -> None:
    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_duplicate_key(frame: pd.DataFrame, key: list[str]) -> None:
    duplicates = frame.duplicated(subset=key, keep=False)
    if duplicates.any():
        examples = frame.loc[duplicates, key].head(5).to_dict(orient="records")
        raise ValueError(f"Duplicate rows under key {key}; examples: {examples}")
