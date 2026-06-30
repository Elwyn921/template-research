from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.simple_validators import validate_figure_spec


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate figure specs against Foundry gates.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in args.paths:
        errors.extend(
            validate_figure_spec(path, ROOT / "foundation/schemas/figure_spec.schema.yaml")
        )
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Figure asset validation passed: {len(args.paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
