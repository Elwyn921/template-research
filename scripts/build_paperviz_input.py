from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = [
    "AGENTS.md",
    "RESEARCH.md",
    "TOOL_MODULES.md",
    "TOOLCHAIN.md",
    "PROJECT_BRIEF.yaml",
    "FIGURE_GENERATION_CONTRACT.md",
]


def read_text(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_yaml_or_json(path: Path) -> dict[str, Any]:
    raw = read_text(path)
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
    elif path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(raw)
    else:
        data = {
            "id": path.stem,
            "title": path.stem.replace("-", " ").replace("_", " "),
            "figure_type": "diagram",
            "mode": "image",
            "paper_claim": "",
            "figure_goal": raw.strip(),
            "caption": raw.strip().splitlines()[0] if raw.strip() else path.stem,
            "panels": [{"name": "Figure", "content": raw.strip()}],
            "must_keep_labels": [],
            "forbidden_content": [],
            "style_constraints": [],
            "verification_checklist": [],
        }
    if not isinstance(data, dict):
        raise SystemExit(f"Figure brief must be an object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(has_content(item) for item in value.values())
    if isinstance(value, list):
        return any(has_content(item) for item in value)
    return True


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower()
    return slug or "figure"


def require_brief_fields(brief: dict[str, Any], path: Path) -> None:
    required = [
        "id",
        "title",
        "figure_type",
        "mode",
        "paper_claim",
        "figure_goal",
        "panels",
        "must_keep_labels",
        "forbidden_content",
        "style_constraints",
        "verification_checklist",
    ]
    missing = [key for key in required if key not in brief]
    if missing:
        raise SystemExit(f"Figure brief {path} is missing required fields: {missing}")
    if brief["mode"] not in {"image", "plot", "mixed"}:
        raise SystemExit("Figure brief mode must be one of: image, plot, mixed")
    if not as_list(brief["panels"]):
        raise SystemExit("Figure brief must define at least one panel")


def require_paperviz_compatible_mode(brief: dict[str, Any], path: Path) -> None:
    mode = brief["mode"]
    if mode == "plot":
        raise SystemExit(
            f"PaperVizAgent input is not valid for mode: plot ({path}). "
            "Use scripts/build_data_figure.py or another data-grounded renderer."
        )

    figure_type = str(brief.get("figure_type") or "").strip().lower()
    figure_role = str(brief.get("figure_role") or "").strip().lower()
    if mode == "image" and (figure_type == "data-figure" or figure_role == "data"):
        raise SystemExit(
            f"Image-mode brief is marked as data figure ({path}). Use mode: plot or mode: mixed."
        )

    data_fields = [
        field for field in ("data_requirements", "plot_spec") if has_content(brief.get(field))
    ]
    if mode == "image" and data_fields:
        raise SystemExit(
            f"Image-mode brief contains data-grounded fields {data_fields} ({path}). "
            "Use mode: plot or mode: mixed."
        )


def format_panels(panels: list[Any]) -> str:
    lines: list[str] = []
    for index, panel in enumerate(panels, start=1):
        if isinstance(panel, dict):
            name = panel.get("name", f"Panel {index}")
            purpose = panel.get("purpose", "")
            content = panel.get("content", "")
            evidence = panel.get("evidence_or_data", "")
            lines.append(f"{index}. {name}")
            if purpose:
                lines.append(f"   Purpose: {purpose}")
            lines.append(f"   Content: {content}")
            if evidence:
                lines.append(f"   Evidence/data: {evidence}")
        else:
            lines.append(f"{index}. {panel}")
    return "\n".join(lines)


def format_mapping(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if value is None:
        return f"{prefix}- None specified"
    if isinstance(value, dict):
        if not value:
            return f"{prefix}- None specified"
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(format_mapping(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {item}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{prefix}- None specified"
        return "\n".join(f"{prefix}- {item}" for item in value)
    return f"{prefix}{value}"


def bullet_list(items: list[Any]) -> str:
    if not items:
        return "- None specified"
    return "\n".join(f"- {item}" for item in items)


def build_content(
    brief: dict[str, Any],
    brief_path: Path,
    agents: str,
    project_brief: str,
    research: str,
    tool_modules: str,
    toolchain: str,
    figure_contract: str,
    research_stack: str,
) -> str:
    panels = format_panels(as_list(brief.get("panels")))
    must_keep = bullet_list(as_list(brief.get("must_keep_labels")))
    forbidden = bullet_list(as_list(brief.get("forbidden_content")))
    style = bullet_list(as_list(brief.get("style_constraints")))
    verification = bullet_list(as_list(brief.get("verification_checklist")))
    data_requirements = format_mapping(brief.get("data_requirements"))
    plot_spec = format_mapping(brief.get("plot_spec"))
    output_record = format_mapping(brief.get("output_record"))

    return f"""REPOSITORY RESEARCH CONTEXT AND AGENT GUARDRAILS
Use this context as the source-of-truth for the figure's scientific meaning,
tool routing, labels, and verification steps. If a requested visual element is
not supported by the repository context or figure brief, keep it out of the
figure or mark the result as a draft for review.

Source: RESEARCH.md
{research}

Source: AGENTS.md
{agents}

Source: PROJECT_BRIEF.yaml
{project_brief}

Source: TOOL_MODULES.md
{tool_modules}

Source: TOOLCHAIN.md
{toolchain}

Source: FIGURE_GENERATION_CONTRACT.md
{figure_contract}

Source: docs/RESEARCH_STACK.md
{research_stack}

ACTIVE FIGURE BRIEF
Source: {brief_path.as_posix()}
ID: {brief.get("id")}
Title: {brief.get("title")}
Figure type: {brief.get("figure_type")}
Mode: {brief.get("mode")}
Figure role: {brief.get("figure_role", brief.get("mode"))}
Audience: {brief.get("audience", "research readers")}
Paper claim: {brief.get("paper_claim")}
Figure goal: {brief.get("figure_goal")}

Data requirements:
{data_requirements}

Plot specification:
{plot_spec}

Panel plan:
{panels}

Labels that must appear exactly:
{must_keep}

Forbidden content:
{forbidden}

Style constraints:
{style}

Verification checklist:
{verification}

Output record:
{output_record}

AGENT GENERATION GUIDANCE
- Do not invent exact values, model metrics, material mechanisms, market facts, or citations.
- Preserve every required label from the figure brief.
- Do not include a figure title inside the generated image.
- Use short, readable labels and clear arrows.
- If exact quantitative panels are needed, use pre-rendered data-grounded panels
  supplied by the repository or describe placeholders only.
- PaperVizAgent must not create exact quantitative marks, axes, metrics,
  residuals, SHAP values, or statistical diagnostics.
- The output should support the paper claim without adding claims beyond the
  brief.
"""


def build_visual_intent(brief: dict[str, Any]) -> str:
    labels = ", ".join(str(item) for item in as_list(brief.get("must_keep_labels")))
    forbidden = ", ".join(str(item) for item in as_list(brief.get("forbidden_content")))
    figure_role = str(brief.get("figure_role") or brief.get("mode") or "figure")
    return (
        f"{brief.get('caption') or brief.get('figure_goal')}\n\n"
        f"Figure role: {figure_role}. "
        "Agent guidance: follow AGENTS.md, TOOL_MODULES.md, RESEARCH.md, "
        "TOOLCHAIN.md, docs/RESEARCH_STACK.md, and FIGURE_GENERATION_CONTRACT.md; "
        f"preserve these labels exactly: {labels or 'none specified'}; "
        f"avoid: {forbidden or 'none specified'}; "
        "do not invent numerical results or unsupported scientific/financial claims."
    )


def build_records(
    brief: dict[str, Any],
    content: str,
    source_files: list[str],
    num_candidates: int,
    max_critic_rounds: int,
) -> list[dict[str, Any]]:
    brief_id = str(brief.get("id") or brief.get("title") or "figure")
    filename_base = slugify(brief_id)
    caption = str(brief.get("caption") or brief.get("figure_goal") or brief.get("title"))
    visual_intent = build_visual_intent(brief)
    aspect_ratio = str(brief.get("aspect_ratio") or "16:9")
    records = []
    for candidate_id in range(num_candidates):
        suffix = f"-candidate-{candidate_id}" if num_candidates > 1 else ""
        records.append(
            {
                "filename": f"{filename_base}{suffix}",
                "caption": caption,
                "content": content,
                "visual_intent": visual_intent,
                "candidate_id": candidate_id,
                "max_critic_rounds": max_critic_rounds,
                "additional_info": {
                    "rounded_ratio": aspect_ratio,
                    "source_files": source_files,
                    "contract": "FIGURE_GENERATION_CONTRACT.md",
                    "compiled_at_utc": datetime.now(UTC).isoformat(),
                },
            }
        )
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build constrained PaperVizAgent input from a repository figure brief."
    )
    parser.add_argument("brief", type=Path, help="Figure brief YAML, JSON, or Markdown path.")
    parser.add_argument("--out", type=Path, help="Output JSON path.")
    parser.add_argument("--num-candidates", type=int, default=1)
    parser.add_argument("--max-critic-rounds", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.num_candidates < 1:
        raise SystemExit("--num-candidates must be >= 1")
    if args.max_critic_rounds < 0:
        raise SystemExit("--max-critic-rounds must be >= 0")

    brief_path = args.brief if args.brief.is_absolute() else ROOT / args.brief
    brief = load_yaml_or_json(brief_path)
    require_brief_fields(brief, brief_path)
    require_paperviz_compatible_mode(brief, brief_path)

    agents = read_text(ROOT / "AGENTS.md")
    research = read_text(ROOT / "RESEARCH.md")
    tool_modules = read_text(ROOT / "TOOL_MODULES.md")
    toolchain = read_text(ROOT / "TOOLCHAIN.md")
    project_brief = read_text(ROOT / "PROJECT_BRIEF.yaml")
    figure_contract = read_text(ROOT / "FIGURE_GENERATION_CONTRACT.md")
    research_stack_path = ROOT / "docs" / "RESEARCH_STACK.md"
    research_stack = read_text(research_stack_path) if research_stack_path.exists() else ""

    source_files = [
        "AGENTS.md",
        "RESEARCH.md",
        "TOOL_MODULES.md",
        "TOOLCHAIN.md",
        "PROJECT_BRIEF.yaml",
        "FIGURE_GENERATION_CONTRACT.md",
        "docs/RESEARCH_STACK.md",
        brief_path.relative_to(ROOT).as_posix(),
    ]
    for root_file in REQUIRED_ROOT_FILES:
        if not (ROOT / root_file).is_file():
            raise SystemExit(f"Required root contract file is missing: {root_file}")

    content = build_content(
        brief=brief,
        brief_path=brief_path.relative_to(ROOT),
        agents=agents,
        project_brief=project_brief,
        research=research,
        tool_modules=tool_modules,
        toolchain=toolchain,
        figure_contract=figure_contract,
        research_stack=research_stack,
    )
    records = build_records(
        brief=brief,
        content=content,
        source_files=source_files,
        num_candidates=args.num_candidates,
        max_critic_rounds=args.max_critic_rounds,
    )

    if args.out:
        out_path = args.out if args.out.is_absolute() else ROOT / args.out
    else:
        out_dir = ROOT / "outputs" / "figures" / "papervizagent" / slugify(brief_path.stem)
        out_path = out_dir / "input.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote constrained PaperVizAgent input: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
