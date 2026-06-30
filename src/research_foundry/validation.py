from __future__ import annotations

from pathlib import Path
from typing import Any

from research_foundry.paths import root_path
from research_foundry.registry import (
    list_pack_manifests,
    load_adapters,
    load_compatibility,
    load_packs_registry,
    load_profiles,
    load_tools,
    read_yaml,
)

CONTROLLED_STATUS = {
    "not_installed",
    "optional",
    "installed",
    "experimental",
    "deprecated",
    "blocked",
}
CONTROLLED_ROLE = {"primary", "secondary", "conditional", "fallback", "audit_only"}
CONTROLLED_SOURCE_TYPE = {
    "local_python",
    "mcp",
    "external_skill",
    "cli",
    "library",
    "manual_tool",
    "cloud_service",
}

REQUIRED_TOOL_FIELDS = {
    "tool_id",
    "display_name",
    "category",
    "sub_category",
    "role",
    "status",
    "source_type",
    "source_repository",
    "source_url",
    "license",
    "version_pin",
    "installation_mode",
    "default_scope",
    "allowed_project_types",
    "primary_tasks",
    "activation_triggers",
    "inputs",
    "outputs",
    "artifact_contracts",
    "permissions",
    "dependencies",
    "overlap_group",
    "default_priority",
    "fallback_tools",
    "conflicts_with",
    "compatibility_notes",
    "risk_notes",
    "human_review_required_when",
    "downstream_export_policy",
}

REQUIRED_PACK_FIELDS = {
    "name",
    "version",
    "scope",
    "description",
    "project_types",
    "activation_triggers",
    "required_tool_ids",
    "optional_tool_ids",
    "required_artifacts",
    "required_validators",
    "compatibility",
    "conflicts",
    "export_paths",
}

REQUIRED_PROFILE_FIELDS = {
    "profile_id",
    "description",
    "valid_project_types",
    "activation_triggers",
    "recommended_packs",
    "default_tools",
    "conditional_tools",
    "prohibited_tools",
    "required_artifacts",
    "required_validators",
    "known_risks",
}

REQUIRED_ADAPTER_FILES = {
    "README.md",
    "adapter.yaml",
    "installation.md",
    "usage.md",
    "limitations.md",
}
FORBIDDEN_CONTROLLER_NAMES = {
    "AGENTS.md",
    "TOOLFLOW.md",
    "RESEARCH.md",
    "TOOLCHAIN.md",
    "TOOL_MODULES.md",
    "PROJECT_STATE.yaml",
    "WORKFLOW_ROUTER.yaml",
    "TOOL_REGISTRY.yaml",
}
PROTECTED_EXPORT_PATHS = {
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
}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def validate_tools() -> list[str]:
    errors: list[str] = []
    tools = load_tools()
    for key, tool in tools.items():
        missing = sorted(REQUIRED_TOOL_FIELDS - set(tool))
        if missing:
            errors.append(f"tools.yaml:{key} missing fields {missing}")
        if tool.get("tool_id") != key:
            errors.append(f"tools.yaml:{key} tool_id mismatch")
        if tool.get("status") not in CONTROLLED_STATUS:
            errors.append(f"tools.yaml:{key} invalid status {tool.get('status')!r}")
        if tool.get("role") not in CONTROLLED_ROLE:
            errors.append(f"tools.yaml:{key} invalid role {tool.get('role')!r}")
        if tool.get("source_type") not in CONTROLLED_SOURCE_TYPE:
            errors.append(f"tools.yaml:{key} invalid source_type {tool.get('source_type')!r}")
        for fallback in as_list(tool.get("fallback_tools")):
            if fallback in {
                "CSV",
                "human_readable_manifests",
                "experiment_registry_csv",
                "manual_grid_search",
                "validate_dataset_inventory",
            }:
                continue
            if fallback not in tools:
                errors.append(f"tools.yaml:{key} unknown fallback tool {fallback!r}")
        for conflict in as_list(tool.get("conflicts_with")):
            if conflict not in tools:
                errors.append(f"tools.yaml:{key} unknown conflict tool {conflict!r}")
    return errors


def validate_pack_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    tools = load_tools()
    try:
        pack = read_yaml(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    missing = sorted(REQUIRED_PACK_FIELDS - set(pack))
    if missing:
        errors.append(f"{path}: missing fields {missing}")
    pack_id = path.parent.name
    if pack.get("name") != pack_id:
        errors.append(f"{path}: name must match directory {pack_id!r}")
    for tool_id in as_list(pack.get("required_tool_ids")) + as_list(pack.get("optional_tool_ids")):
        if tool_id not in tools:
            errors.append(f"{path}: unknown tool {tool_id!r}")
    for forbidden in FORBIDDEN_CONTROLLER_NAMES:
        for candidate in path.parent.rglob(forbidden):
            errors.append(
                f"{path.parent}: forbidden controller file {candidate.relative_to(path.parent)}"
            )
    return errors


def validate_packs() -> list[str]:
    errors: list[str] = []
    registry_packs = load_packs_registry()
    manifest_paths = list_pack_manifests()
    manifest_ids = {path.parent.name for path in manifest_paths}
    if manifest_ids != set(registry_packs):
        errors.append(
            f"pack registry mismatch: manifests={sorted(manifest_ids)} registry={sorted(registry_packs)}"
        )
    for path in manifest_paths:
        errors.extend(validate_pack_manifest(path))
    return errors


def validate_profiles() -> list[str]:
    errors: list[str] = []
    tools = load_tools()
    packs = load_packs_registry()
    profiles = load_profiles()
    for key, profile in profiles.items():
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            errors.append(f"profiles.yaml:{key} missing fields {missing}")
        if profile.get("profile_id") != key:
            errors.append(f"profiles.yaml:{key} profile_id mismatch")
        for pack_id in as_list(profile.get("recommended_packs")):
            if pack_id not in packs:
                errors.append(f"profiles.yaml:{key} unknown pack {pack_id!r}")
        for tool_id in (
            as_list(profile.get("default_tools"))
            + as_list(profile.get("conditional_tools"))
            + as_list(profile.get("prohibited_tools"))
        ):
            if tool_id not in tools:
                errors.append(f"profiles.yaml:{key} unknown tool {tool_id!r}")
    return errors


def validate_adapters() -> list[str]:
    errors: list[str] = []
    tools = load_tools()
    packs = load_packs_registry()
    adapters = load_adapters()
    for key, adapter in adapters.items():
        tool_id = adapter.get("tool_id")
        if tool_id not in tools:
            errors.append(f"adapters.yaml:{key} unknown tool {tool_id!r}")
        for pack_id in as_list(adapter.get("supported_packs")):
            if pack_id not in packs:
                errors.append(f"adapters.yaml:{key} unknown pack {pack_id!r}")
        path = root_path(adapter.get("path", ""))
        missing_files = sorted(
            file for file in REQUIRED_ADAPTER_FILES if not (path / file).is_file()
        )
        if missing_files:
            errors.append(f"{path}: missing adapter files {missing_files}")
        adapter_yaml = path / "adapter.yaml"
        if adapter_yaml.is_file():
            data = read_yaml(adapter_yaml)
            if data.get("adapter_id") != key:
                errors.append(f"{adapter_yaml}: adapter_id mismatch")
            if data.get("tool_id") != tool_id:
                errors.append(f"{adapter_yaml}: tool_id mismatch")
    return errors


def validate_compatibility() -> list[str]:
    errors: list[str] = []
    packs = load_packs_registry()
    compatibility = load_compatibility()
    pack_compat = compatibility.get("pack_compatibility")
    if not isinstance(pack_compat, dict):
        return ["compatibility_matrix.yaml: missing pack_compatibility mapping"]
    for pack_id, entry in pack_compat.items():
        if pack_id not in packs:
            errors.append(f"compatibility_matrix.yaml unknown pack {pack_id!r}")
        for ref in as_list(entry.get("compatible_with")) + as_list(entry.get("conflicts_with")):
            if ref not in packs:
                errors.append(
                    f"compatibility_matrix.yaml:{pack_id} unknown referenced pack {ref!r}"
                )
    return errors


def validate_no_nested_agents() -> list[str]:
    agents = sorted(root_path().glob("**/AGENTS.md"))
    nested = [path for path in agents if path != root_path("AGENTS.md")]
    return [f"Nested AGENTS.md is not allowed: {path}" for path in nested]


def validate_export_boundary_paths(paths: list[str]) -> list[str]:
    errors = []
    for raw in paths:
        normalized = raw.strip("/")
        if normalized in PROTECTED_EXPORT_PATHS or any(
            normalized == protected or normalized.startswith(f"{protected}/")
            for protected in PROTECTED_EXPORT_PATHS
            if protected != "08_tools/TOOLFLOW.md"
        ):
            errors.append(f"Export path is protected: {raw}")
        if not (
            normalized.startswith("08_tools/foundry/")
            or normalized == "08_tools/foundation_manifest.yaml"
            or normalized == "08_tools/foundry"
        ):
            errors.append(f"Export path must stay under 08_tools/foundry/: {raw}")
    return errors


def validate_foundry() -> list[str]:
    errors: list[str] = []
    errors.extend(validate_tools())
    errors.extend(validate_packs())
    errors.extend(validate_profiles())
    errors.extend(validate_adapters())
    errors.extend(validate_compatibility())
    errors.extend(validate_no_nested_agents())
    return errors
