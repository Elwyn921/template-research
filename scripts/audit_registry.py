from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    sources = read_csv(ROOT / "metadata" / "source_registry.csv")
    datasets = read_csv(ROOT / "metadata" / "data_manifest.csv")
    source_ids = {row["source_id"] for row in sources if row.get("source_id")}
    errors = []
    for dataset in datasets:
        refs = [item.strip() for item in dataset.get("source_ids", "").split(";") if item.strip()]
        unknown = set(refs) - source_ids
        if unknown:
            errors.append(f"{dataset['dataset_id']}: unknown source IDs {sorted(unknown)}")
    if errors:
        raise SystemExit("Registry audit failed:\n- " + "\n- ".join(errors))
    print(f"Registry audit passed: {len(sources)} source(s), {len(datasets)} dataset(s).")


if __name__ == "__main__":
    main()
