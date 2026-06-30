from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.tool_plan import plan_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain a saved JSON tool plan.")
    parser.add_argument("plan_json", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan_json.read_text(encoding="utf-8"))
    print(plan_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
