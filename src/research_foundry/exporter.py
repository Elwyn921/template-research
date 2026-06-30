from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from research_foundry.paths import root_path
from research_foundry.registry import load_packs_registry
from research_foundry.tool_plan import build_plan, plan_markdown
from research_foundry.validation import FORBIDDEN_CONTROLLER_NAMES, validate_export_boundary_paths


def ensure_pack_exportable(pack_id: str) -> None:
    pack_dir = root_path("packs", pack_id)
    if not pack_dir.is_dir():
        raise ValueError(f"Unknown pack directory: {pack_id}")
    for forbidden in FORBIDDEN_CONTROLLER_NAMES:
        matches = list(pack_dir.rglob(forbidden))
        if matches:
            rel = [path.relative_to(pack_dir).as_posix() for path in matches]
            raise ValueError(f"Pack {pack_id} contains forbidden controller files: {rel}")


def copy_tree_contents(src: Path, dst: Path) -> list[str]:
    written: list[str] = []
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return [dst.as_posix()]
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        written.append(target.as_posix())
    return written


def build_manifest(
    project_type: str,
    target: str,
    profiles: list[str],
    packs: list[str],
    plan: dict[str, Any],
    release: str,
) -> dict[str, Any]:
    primary_by_family = {category: tools for category, tools in plan["primary_tools"].items()}
    return {
        "foundry": {
            "repository": "Elwyn921/template-research",
            "release": release,
            "exported_at": datetime.now(UTC).date().isoformat(),
        },
        "project": {
            "type": project_type,
            "target": target,
        },
        "profiles": profiles,
        "packs": packs,
        "resolved_tools": {
            "primary": primary_by_family,
            "conditional": plan["conditional_tools"],
        },
        "local_overrides": [],
        "notes": [
            "This manifest records selected capabilities and provenance.",
            "It is not a project controller.",
            "Downstream AGENTS.md and TOOLFLOW.md remain authoritative.",
        ],
    }


def export_project_capabilities(
    destination: Path,
    project_type: str,
    base_profile: str,
    domain_profile: str,
    enhancement_profiles: list[str],
    packs: list[str],
    release: str,
    target: str = "",
    task: str = "export selected Research Foundry capabilities",
    stage: str = "bootstrap",
) -> dict[str, Any]:
    destination = destination.resolve()
    foundry_root = destination / "08_tools" / "foundry"
    manifest_path = destination / "08_tools" / "foundation_manifest.yaml"

    protected = [
        "AGENTS.md",
        "08_tools/TOOLFLOW.md",
        "00_discovery",
        "01_framing",
        "02_data",
        "03_experiments",
        "04_results",
        "05_figures",
        "06_manuscript",
        "07_review_release",
    ]
    untouched = [path for path in protected if (destination / path).exists()]

    selected_profiles = [base_profile, domain_profile, *enhancement_profiles]
    plan = build_plan(
        project_type=project_type,
        task=task,
        stage=stage,
        target_output="capability manifest and resolved tool plan",
        profiles=[profile for profile in selected_profiles if profile != "base_research"],
    )

    selected_packs = list(dict.fromkeys(packs or plan["packs"]))
    registry = load_packs_registry()
    for pack_id in selected_packs:
        if pack_id not in registry:
            raise ValueError(f"Unknown pack: {pack_id}")
        ensure_pack_exportable(pack_id)

    planned_export_paths = [
        "08_tools/foundation_manifest.yaml",
        "08_tools/foundry/resolved_tool_plan.md",
        *[f"08_tools/foundry/packs/{pack}" for pack in selected_packs],
    ]
    boundary_errors = validate_export_boundary_paths(planned_export_paths)
    if boundary_errors:
        raise ValueError("; ".join(boundary_errors))

    written: list[str] = []
    foundry_root.mkdir(parents=True, exist_ok=True)
    for pack_id in selected_packs:
        src = root_path("packs", pack_id)
        dst = foundry_root / "packs" / pack_id
        written.extend(copy_tree_contents(src, dst))

    registry_out = foundry_root / "tool_fabric" / "registry"
    registry_out.mkdir(parents=True, exist_ok=True)
    for filename in [
        "tools.yaml",
        "packs.yaml",
        "profiles.yaml",
        "adapters.yaml",
        "compatibility_matrix.yaml",
        "dependency_matrix.yaml",
        "deprecation_registry.yaml",
    ]:
        src = root_path("tool_fabric", "registry", filename)
        dst = registry_out / filename
        shutil.copy2(src, dst)
        written.append(dst.as_posix())

    plan_path = foundry_root / "resolved_tool_plan.md"
    plan_path.write_text(plan_markdown(plan), encoding="utf-8")
    written.append(plan_path.as_posix())

    manifest = build_manifest(
        project_type, target, selected_profiles, selected_packs, plan, release
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    written.append(manifest_path.as_posix())

    report = {
        "selected_profiles": selected_profiles,
        "selected_packs": selected_packs,
        "resolved_primary_tools": plan["primary_tools"],
        "conditional_tools": plan["conditional_tools"],
        "skipped_heavy_tools": plan["skipped_heavy_tools"],
        "dependencies_not_installed": plan["dependency_warnings"],
        "known_conflicts": plan["known_conflicts"],
        "files_exported": [str(Path(path).relative_to(destination)) for path in written],
        "protected_paths_untouched": untouched,
    }
    report_path = foundry_root / "export_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
