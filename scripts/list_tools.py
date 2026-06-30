from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_tools


def main() -> int:
    parser = argparse.ArgumentParser(description="List or show canonical Tool Fabric tools.")
    parser.add_argument("--show", dest="tool_id")
    args = parser.parse_args()
    tools = load_tools()
    if args.tool_id:
        tool = tools.get(args.tool_id)
        if tool is None:
            available = ", ".join(sorted(tools))
            raise SystemExit(f"Unknown tool {args.tool_id!r}. Available: {available}")
        print(yaml.safe_dump(tool, sort_keys=False))
        return 0
    for tool_id, tool in tools.items():
        print(f"{tool_id}\t{tool.get('status')}\t{tool.get('role')}\t{tool.get('display_name')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
