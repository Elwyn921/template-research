import pandas as pd
import pytest

from research_project.data.validate import validate_duplicate_key, validate_required_columns


def test_required_columns_passes() -> None:
    validate_required_columns(pd.DataFrame({"a": [1], "b": [2]}), ["a", "b"])


def test_required_columns_fails() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(pd.DataFrame({"a": [1]}), ["a", "b"])


def test_duplicate_key_fails() -> None:
    frame = pd.DataFrame({"entity_id": ["A", "A"], "period": ["2026-01", "2026-01"]})
    with pytest.raises(ValueError, match="Duplicate rows"):
        validate_duplicate_key(frame, ["entity_id", "period"])
