from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.paths import root_path
from research_foundry.registry import list_pack_manifests
from research_foundry.validation import validate_pack_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Foundry pack manifests.")
    parser.add_argument("packs", nargs="*", help="Optional pack IDs or pack.yaml paths.")
    args = parser.parse_args()
    paths = []
    if args.packs:
        for value in args.packs:
            candidate = Path(value)
            if candidate.suffix:
                paths.append(candidate if candidate.is_absolute() else root_path(value))
            else:
                paths.append(root_path("packs", value, "pack.yaml"))
    else:
        paths = list_pack_manifests()
    errors = []
    for path in paths:
        errors.extend(validate_pack_manifest(path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Pack validation passed: {len(paths)} pack(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
