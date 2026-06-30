from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.paths import root_path
from research_foundry.registry import read_yaml
from research_foundry.tool_plan import normalize_csv


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare exported pack versions with this Foundry."
    )
    parser.add_argument("--dest", required=True, type=Path)
    parser.add_argument("--packs", required=True)
    args = parser.parse_args()
    for pack_id in normalize_csv(args.packs):
        current = read_yaml(root_path("packs", pack_id, "pack.yaml")).get("version")
        exported_path = args.dest / "08_tools" / "foundry" / "packs" / pack_id / "pack.yaml"
        if not exported_path.is_file():
            print(f"{pack_id}: not exported")
            continue
        exported = read_yaml(exported_path).get("version")
        status = "same" if current == exported else "diff"
        print(f"{pack_id}: exported={exported} foundry={current} status={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
