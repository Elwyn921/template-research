from __future__ import annotations

import argparse
from pathlib import Path

PROJECT_DIRS = [
    "00_discovery",
    "01_framing",
    "02_data",
    "03_experiments",
    "04_results",
    "05_figures",
    "06_manuscript",
    "07_review_release",
    "08_tools/foundry",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap a minimal downstream ResearchOS directory."
    )
    parser.add_argument("dest", type=Path)
    args = parser.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    for relative in PROJECT_DIRS:
        (args.dest / relative).mkdir(parents=True, exist_ok=True)
    print(f"Bootstrapped ResearchOS directories under {args.dest.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
