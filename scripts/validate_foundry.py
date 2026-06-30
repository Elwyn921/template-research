from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.validation import validate_foundry


def main() -> int:
    errors = validate_foundry()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Foundry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
