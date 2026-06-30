from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.validation import validate_foundry


def main() -> int:
    errors = validate_foundry()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Foundry release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
