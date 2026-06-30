from __future__ import annotations

import argparse
from pathlib import Path

from bootstrap_research_os import PROJECT_DIRS

EXTRA_DIRS = [
    "02_data/entities",
    "02_data/events",
    "04_results/theses",
    "04_results/company_briefs",
    "06_manuscript/memos",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap a minimal AI industry program directory."
    )
    parser.add_argument("dest", type=Path)
    args = parser.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    for relative in [*PROJECT_DIRS, *EXTRA_DIRS]:
        (args.dest / relative).mkdir(parents=True, exist_ok=True)
    print(f"Bootstrapped AI industry program directories under {args.dest.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
