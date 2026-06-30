from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.registry import load_packs_registry


def main() -> int:
    parser = argparse.ArgumentParser(description="List or show canonical Foundry packs.")
    parser.add_argument("--show", dest="pack_id")
    args = parser.parse_args()
    packs = load_packs_registry()
    if args.pack_id:
        pack = packs.get(args.pack_id)
        if pack is None:
            available = ", ".join(sorted(packs))
            raise SystemExit(f"Unknown pack {args.pack_id!r}. Available: {available}")
        print(yaml.safe_dump(pack, sort_keys=False))
        return 0
    for pack_id, pack in packs.items():
        print(f"{pack_id}\t{pack.get('status')}\t{pack.get('scope')}\t{pack.get('display_name')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
