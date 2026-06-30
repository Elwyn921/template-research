from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.simple_validators import validate_required_fields


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an experiment plan.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_required_fields(
        args.path, ROOT / "foundation/schemas/experiment_plan.schema.yaml"
    )
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Experiment plan validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
