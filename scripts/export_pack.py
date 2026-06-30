from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.exporter import ensure_pack_exportable
from research_foundry.paths import root_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a single Foundry pack directory.")
    parser.add_argument("pack_id")
    parser.add_argument("--dest", required=True, type=Path)
    args = parser.parse_args()
    ensure_pack_exportable(args.pack_id)
    src = root_path("packs", args.pack_id)
    dst = args.dest.resolve() / args.pack_id
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Exported {args.pack_id} to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
