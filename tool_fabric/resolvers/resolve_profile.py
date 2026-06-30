from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_profiles


def main() -> int:
    parser = argparse.ArgumentParser(description="Show a canonical Tool Fabric profile.")
    parser.add_argument("profile_id")
    args = parser.parse_args()
    profiles = load_profiles()
    if args.profile_id not in profiles:
        available = ", ".join(sorted(profiles))
        raise SystemExit(f"Unknown profile {args.profile_id!r}. Available: {available}")
    print(yaml.safe_dump(profiles[args.profile_id], sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
