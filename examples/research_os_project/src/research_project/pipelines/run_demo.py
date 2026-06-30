from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from research_project.data.build_dataset import build_dataset
from research_project.utils.paths import root_path


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run() -> None:
    config = load_yaml(root_path("configs", "data.yaml"))["data"]
    frame = build_dataset(
        input_path=root_path(config["input_file"]),
        output_path=root_path("data", "processed", "demo_processed.csv"),
        required_columns=config["required_columns"],
        duplicate_key=config["duplicate_key"],
    )
    table_path = root_path("outputs", "tables", "demo_dataset_summary.csv")
    table_path.parent.mkdir(parents=True, exist_ok=True)
    frame.describe(include="all").transpose().to_csv(table_path)
    print("Demo pipeline complete.")


if __name__ == "__main__":
    argparse.ArgumentParser(description="Run the template demo pipeline.").parse_args()
    run()
