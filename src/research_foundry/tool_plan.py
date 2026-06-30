from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from research_foundry.registry import (
    load_compatibility,
    load_dependency_matrix,
    load_packs_registry,
    load_profiles,
    load_tools,
)

TASK_CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "discovery": ("literature", "paper", "source", "web", "company", "policy", "news"),
    "synthesis": ("survey", "synthesis", "review", "contradiction", "citation"),
    "data": ("data", "dataset", "table", "sql", "parquet", "audit"),
    "experiment": ("model", "experiment", "prediction", "calibration", "diagnostic", "shift"),
    "figures": ("figure", "plot", "chart", "visual", "shap", "residual"),
    "manuscript": ("paper", "manuscript", "report", "memo", "publication", "submission"),
    "audit": ("audit", "validate", "release", "check", "citation"),
}

DEFAULT_PRIMARY_BY_CATEGORY: dict[str, list[str]] = {
    "discovery": ["paper_search_mcp", "zotero_mcp"],
    "synthesis": ["literature_survey_skill", "evidence_matrix_builder"],
    "data": ["python", "pandas", "duckdb", "parquet"],
    "experiment": ["scikit_learn", "statsmodels", "scipy", "shap"],
    "figures": ["matplotlib", "graphviz", "svg"],
    "manuscript": ["paperspine", "markdown", "quarto", "latex"],
    "audit": ["academic_research_skills", "citation_check_skill", "refchecker"],
}

INDUSTRY_PRIMARY_BY_CATEGORY: dict[str, list[str]] = {
    "discovery": ["tavily_mcp", "official_source_verifier"],
    "synthesis": ["entity_registry_builder", "event_ledger_builder", "thesis_ledger_builder"],
    "data": ["python", "pandas", "duckdb", "parquet"],
    "experiment": ["statsmodels", "scipy"],
    "figures": ["matplotlib", "graphviz", "svg"],
    "manuscript": ["markdown", "quarto"],
    "audit": ["official_source_verifier", "valuation_assumption_audit", "academic_research_skills"],
}

HEAVY_TRIGGER_PATTERNS: dict[str, tuple[str, ...]] = {
    "mlflow": ("multiple model runs", "parameter comparison", "artifact tracing", "many runs"),
    "dvc": (
        "large data",
        "large artifact",
        "data versions",
        "artifact checkout",
        "pipeline reproducibility",
    ),
    "optuna": ("hyperparameter", "systematic search", "optimization search"),
    "paperqa2": (
        "20 pdf",
        "contradiction",
        "page-level",
        "systematic review",
        "equation comparison",
    ),
    "papervizagent": ("multi-candidate", "critic", "reference-driven", "graphical abstract"),
}


def normalize_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def task_categories(task: str, stage: str, target_output: str) -> list[str]:
    haystack = f"{task} {stage} {target_output}".lower()
    categories = [
        category
        for category, keywords in TASK_CATEGORY_KEYWORDS.items()
        if any(keyword in haystack for keyword in keywords)
    ]
    if not categories:
        categories = ["data"]
    return categories


def heavy_tool_triggered(
    tool_id: str, task: str, stage: str, target_output: str, constraints: str
) -> bool:
    haystack = f"{task} {stage} {target_output} {constraints}".lower()
    return any(pattern in haystack for pattern in HEAVY_TRIGGER_PATTERNS.get(tool_id, ()))


def merge_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def filter_known_tools(tool_ids: list[str], tools: dict[str, Any], project_type: str) -> list[str]:
    selected: list[str] = []
    for tool_id in tool_ids:
        tool = tools.get(tool_id)
        if not tool:
            continue
        allowed = set(tool.get("allowed_project_types") or [])
        if allowed and project_type not in allowed:
            continue
        selected.append(tool_id)
    return selected


def build_plan(
    project_type: str,
    task: str,
    stage: str,
    target_output: str,
    profiles: list[str],
    constraints: str = "",
) -> dict[str, Any]:
    tools = load_tools()
    profile_registry = load_profiles()
    pack_registry = load_packs_registry()
    compatibility = load_compatibility()
    dependency_matrix = load_dependency_matrix()

    selected_profiles = merge_unique(["base_research", *profiles])
    unknown_profiles = [profile for profile in selected_profiles if profile not in profile_registry]
    if unknown_profiles:
        raise ValueError(f"Unknown profiles: {unknown_profiles}")

    invalid_profiles = [
        profile
        for profile in selected_profiles
        if project_type not in set(profile_registry[profile].get("valid_project_types") or [])
    ]
    if invalid_profiles:
        raise ValueError(f"Profiles not valid for {project_type}: {invalid_profiles}")

    selected_packs = merge_unique(
        [
            pack
            for profile in selected_profiles
            for pack in profile_registry[profile].get("recommended_packs", [])
        ]
    )
    unknown_packs = [pack for pack in selected_packs if pack not in pack_registry]
    if unknown_packs:
        raise ValueError(f"Unknown packs referenced by profiles: {unknown_packs}")

    categories = task_categories(task, stage, target_output)
    default_map = (
        INDUSTRY_PRIMARY_BY_CATEGORY
        if project_type in {"ai_industry", "investment_due_diligence"}
        else DEFAULT_PRIMARY_BY_CATEGORY
    )

    profile_defaults = merge_unique(
        [
            tool
            for profile in selected_profiles
            for tool in profile_registry[profile].get("default_tools", [])
        ]
    )
    profile_conditionals = merge_unique(
        [
            tool
            for profile in selected_profiles
            for tool in profile_registry[profile].get("conditional_tools", [])
        ]
    )
    prohibited = set(
        tool
        for profile in selected_profiles
        for tool in profile_registry[profile].get("prohibited_tools", [])
    )

    primary: dict[str, list[str]] = {}
    for category in categories:
        defaults = default_map.get(category, [])
        candidates = [tool for tool in defaults if tool in profile_defaults or tool in tools]
        selected = filter_known_tools(candidates, tools, project_type)
        selected = [tool for tool in selected if tool not in prohibited]
        if not selected and category == "data":
            selected = ["python", "pandas"]
        primary[category] = selected[:4]

    conditional: list[str] = []
    not_activated: list[str] = []
    for tool_id in profile_conditionals:
        if tool_id in prohibited:
            not_activated.append(tool_id)
            continue
        if tool_id not in tools:
            continue
        if project_type not in set(tools[tool_id].get("allowed_project_types") or []):
            not_activated.append(tool_id)
            continue
        if tool_id in HEAVY_TRIGGER_PATTERNS:
            if heavy_tool_triggered(tool_id, task, stage, target_output, constraints):
                conditional.append(tool_id)
            else:
                not_activated.append(tool_id)
        else:
            conditional.append(tool_id)

    heavy_tools = set(dependency_matrix.get("heavy_tools") or [])
    skipped_heavy = sorted(tool for tool in not_activated if tool in heavy_tools)

    required_artifacts = merge_unique(
        [
            artifact
            for profile in selected_profiles
            for artifact in profile_registry[profile].get("required_artifacts", [])
        ]
    )
    required_validators = merge_unique(
        [
            validator
            for profile in selected_profiles
            for validator in profile_registry[profile].get("required_validators", [])
        ]
    )

    selected_tool_ids = merge_unique(
        [tool for values in primary.values() for tool in values] + conditional
    )
    dependency_warnings = []
    for tool_id in selected_tool_ids:
        tool = tools.get(tool_id, {})
        if tool.get("status") in {"optional", "experimental", "not_installed"}:
            dependency_warnings.append(
                f"{tool_id}: {tool.get('status')} and must be explicitly enabled"
            )

    overlap_groups: dict[str, list[str]] = defaultdict(list)
    for tool_id in selected_tool_ids:
        overlap = tools[tool_id].get("overlap_group")
        if overlap:
            overlap_groups[overlap].append(tool_id)
    known_overlaps = {group: ids for group, ids in overlap_groups.items() if len(ids) > 1}

    pack_conflicts = []
    pack_compat = compatibility.get("pack_compatibility") or {}
    for left in selected_packs:
        conflicts = set((pack_compat.get(left) or {}).get("conflicts_with") or [])
        for right in selected_packs:
            if left != right and right in conflicts:
                pack_conflicts.append(f"{left} conflicts with {right}")

    output_paths = [
        "08_tools/foundry/",
        "08_tools/foundation_manifest.yaml",
        "08_tools/foundry/resolved_tool_plan.md",
    ]

    return {
        "project_type": project_type,
        "task": task,
        "stage": stage,
        "target_output": target_output,
        "profiles": selected_profiles,
        "packs": selected_packs,
        "task_categories": categories,
        "primary_tools": primary,
        "conditional_tools": merge_unique(conditional),
        "tools_explicitly_not_activated": merge_unique(not_activated),
        "skipped_heavy_tools": skipped_heavy,
        "required_artifacts": required_artifacts,
        "required_validators": required_validators,
        "required_human_review_points": merge_unique(
            [
                review
                for tool_id in selected_tool_ids
                for review in tools[tool_id].get("human_review_required_when", [])
            ]
        ),
        "known_overlaps": known_overlaps,
        "dependency_warnings": dependency_warnings,
        "known_conflicts": sorted(set(pack_conflicts)),
        "expected_output_paths": output_paths,
        "notes": [
            "This plan is advisory and does not create a downstream workflow controller.",
            "Downstream AGENTS.md and TOOLFLOW.md remain authoritative.",
        ],
    }


def plan_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Resolved Tool Plan",
        "",
        f"- Project type: {plan['project_type']}",
        f"- Stage: {plan['stage']}",
        f"- Task: {plan['task']}",
        f"- Target output: {plan['target_output']}",
        f"- Profiles: {', '.join(plan['profiles'])}",
        f"- Packs: {', '.join(plan['packs'])}",
        "",
        "## Primary Tools",
    ]
    for category, tool_ids in plan["primary_tools"].items():
        lines.append(f"- {category}: {', '.join(tool_ids) if tool_ids else 'none'}")
    lines.extend(["", "## Conditional Tools"])
    lines.extend(f"- {tool}" for tool in plan["conditional_tools"] or ["none"])
    lines.extend(["", "## Not Activated"])
    lines.extend(f"- {tool}" for tool in plan["tools_explicitly_not_activated"] or ["none"])
    lines.extend(["", "## Required Artifacts"])
    lines.extend(f"- {artifact}" for artifact in plan["required_artifacts"])
    lines.extend(["", "## Required Validators"])
    lines.extend(f"- {validator}" for validator in plan["required_validators"])
    if plan["dependency_warnings"]:
        lines.extend(["", "## Dependency Warnings"])
        lines.extend(f"- {warning}" for warning in plan["dependency_warnings"])
    if plan["known_conflicts"]:
        lines.extend(["", "## Known Conflicts"])
        lines.extend(f"- {conflict}" for conflict in plan["known_conflicts"])
    lines.extend(["", "## Notes"])
    lines.extend(f"- {note}" for note in plan["notes"])
    return "\n".join(lines) + "\n"


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower() or "tool-plan"
