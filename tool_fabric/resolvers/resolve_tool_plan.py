from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from research_foundry.tool_plan import build_plan, normalize_csv, plan_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve an advisory Research Foundry tool plan.")
    parser.add_argument("--project-type", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--target-output", required=True)
    parser.add_argument("--profiles", default="")
    parser.add_argument("--constraints", default="")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan = build_plan(
        project_type=args.project_type,
        task=args.task,
        stage=args.stage,
        target_output=args.target_output,
        profiles=normalize_csv(args.profiles),
        constraints=args.constraints,
    )
    print(plan_markdown(plan))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(plan_markdown(plan), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
