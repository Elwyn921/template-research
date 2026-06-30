from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.exporter import export_project_capabilities
from research_foundry.tool_plan import normalize_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export selected Foundry capabilities.")
    parser.add_argument("--dest", required=True, type=Path)
    parser.add_argument("--project-type", required=True)
    parser.add_argument("--base", default="base_research")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--enhancements", default="")
    parser.add_argument("--packs", default="")
    parser.add_argument("--release", default="v0.1.0-foundry")
    parser.add_argument("--target", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = export_project_capabilities(
        destination=args.dest,
        project_type=args.project_type,
        base_profile=args.base,
        domain_profile=args.domain,
        enhancement_profiles=normalize_csv(args.enhancements),
        packs=normalize_csv(args.packs),
        release=args.release,
        target=args.target,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
