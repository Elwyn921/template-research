from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_profiles


def main() -> int:
    parser = argparse.ArgumentParser(description="List or show canonical Foundry profiles.")
    parser.add_argument("--show", dest="profile_id")
    args = parser.parse_args()
    profiles = load_profiles()
    if args.profile_id:
        profile = profiles.get(args.profile_id)
        if profile is None:
            available = ", ".join(sorted(profiles))
            raise SystemExit(f"Unknown profile {args.profile_id!r}. Available: {available}")
        print(yaml.safe_dump(profile, sort_keys=False))
        return 0
    for profile_id, profile in profiles.items():
        print(f"{profile_id}\t{profile.get('profile_type')}\t{profile.get('description')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
