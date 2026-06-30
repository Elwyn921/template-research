from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_profiles, load_tools
from research_foundry.validation import validate_foundry


def main() -> int:
    parser = argparse.ArgumentParser(description="Compatibility wrapper for Tool Fabric audits.")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--profile")
    args = parser.parse_args()
    errors = validate_foundry()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.list:
        for tool_id, tool in load_tools().items():
            print(f"{tool_id}\t{tool.get('status')}\t{tool.get('display_name')}")
        return 0
    if args.profile:
        profiles = load_profiles()
        if args.profile not in profiles:
            raise SystemExit(f"Unknown profile {args.profile!r}")
        print(yaml.safe_dump(profiles[args.profile], sort_keys=False))
        return 0
    print("Compatibility tool module audit passed via Tool Fabric registries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
