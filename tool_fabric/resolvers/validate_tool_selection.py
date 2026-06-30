from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_tools
from research_foundry.tool_plan import normalize_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a comma-separated tool selection.")
    parser.add_argument("--tools", required=True)
    parser.add_argument("--project-type", required=True)
    args = parser.parse_args()
    registry = load_tools()
    errors = []
    for tool_id in normalize_csv(args.tools):
        tool = registry.get(tool_id)
        if tool is None:
            errors.append(f"Unknown tool: {tool_id}")
            continue
        if args.project_type not in set(tool.get("allowed_project_types") or []):
            errors.append(f"{tool_id} is not allowed for project type {args.project_type}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Tool selection is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
