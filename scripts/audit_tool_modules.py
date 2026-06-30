from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tool_catalog.yaml"
MODULE_CONFIG_PATH = ROOT / "configs" / "modules.yaml"
ROOT_CONTRACT_PATH = ROOT / "TOOL_MODULES.md"

REQUIRED_MODULE_FIELDS = {
    "title",
    "status",
    "maturity_level",
    "use_when",
    "local_steps",
    "primary_outputs",
    "verification",
    "tools",
}

REQUIRED_PROFILE_FIELDS = {"title", "default_modules", "optional_modules", "first_commands"}
MATURITY_LEVELS = {"M0", "M1", "M2", "M3", "M4"}


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"YAML file must contain an object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_catalog() -> dict[str, Any]:
    catalog = read_yaml(CATALOG_PATH)
    if not isinstance(catalog.get("modules"), dict) or not catalog["modules"]:
        raise SystemExit("tool_catalog.yaml must define a non-empty modules mapping.")
    if not isinstance(catalog.get("profiles"), dict) or not catalog["profiles"]:
        raise SystemExit("tool_catalog.yaml must define a non-empty profiles mapping.")
    return catalog


def validate_root_contract() -> list[str]:
    errors: list[str] = []
    if not ROOT_CONTRACT_PATH.is_file():
        return ["Missing root tool module contract: TOOL_MODULES.md."]
    text = ROOT_CONTRACT_PATH.read_text(encoding="utf-8")
    for required in ["tool_catalog.yaml", "configs/modules.yaml"]:
        if required not in text:
            errors.append(f"TOOL_MODULES.md must reference {required}.")
    if "tool_profiles/" in text or "docs/TOOL_MODULE_ROADMAP.md" in text:
        errors.append("TOOL_MODULES.md still references removed scattered module files.")
    return errors


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status_values = set((catalog.get("status_values") or {}).keys())

    for module_id, module in catalog["modules"].items():
        if not isinstance(module, dict):
            errors.append(f"{module_id}: module entry must be an object.")
            continue
        missing = sorted(REQUIRED_MODULE_FIELDS - set(module))
        if missing:
            errors.append(f"{module_id}: missing fields {missing}.")
        if status_values and module.get("status") not in status_values:
            errors.append(f"{module_id}: unknown status {module.get('status')!r}.")
        if module.get("maturity_level") not in MATURITY_LEVELS:
            errors.append(f"{module_id}: unknown maturity_level {module.get('maturity_level')!r}.")
        for field in ["use_when", "local_steps", "primary_outputs", "verification"]:
            if field in module and not as_list(module[field]):
                errors.append(f"{module_id}: {field} must not be empty.")
        tools = module.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append(f"{module_id}: tools must be a non-empty list.")
            continue
        for index, tool in enumerate(tools, start=1):
            if not isinstance(tool, dict) or "name" not in tool or "status" not in tool:
                errors.append(f"{module_id}: tools[{index}] needs name and status.")
                continue
            external = tool.get("github_url") or tool.get("docs_url") or tool.get("local_package")
            if not external and tool.get("status") != "reserved":
                errors.append(
                    f"{module_id}: tools[{index}] needs github_url, docs_url, or local_package."
                )
    return errors


def validate_profiles(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    module_ids = set(catalog["modules"])
    for profile_id, profile in catalog["profiles"].items():
        if not isinstance(profile, dict):
            errors.append(f"{profile_id}: profile must be an object.")
            continue
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            errors.append(f"{profile_id}: missing fields {missing}.")
        selected = as_list(profile.get("default_modules")) + as_list(
            profile.get("optional_modules")
        )
        for module_id in selected:
            if module_id not in module_ids:
                errors.append(f"{profile_id}: references unknown module {module_id!r}.")
    return errors


def validate_module_config(catalog: dict[str, Any], module_config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    profiles = catalog["profiles"]
    module_ids = set(catalog["modules"])

    active_profile = module_config.get("active_profile")
    if active_profile not in profiles:
        errors.append(f"configs/modules.yaml: unknown active_profile {active_profile!r}.")

    enabled_modules = module_config.get("enabled_modules")
    if not isinstance(enabled_modules, dict) or not enabled_modules:
        return ["configs/modules.yaml: enabled_modules must be a non-empty mapping."]

    for module_id, enabled in enabled_modules.items():
        if module_id not in module_ids:
            errors.append(f"configs/modules.yaml: unknown module {module_id!r}.")
        if not isinstance(enabled, bool):
            errors.append(f"configs/modules.yaml: {module_id} must be true or false.")

    missing_modules = sorted(module_ids - set(enabled_modules))
    if missing_modules:
        errors.append(f"configs/modules.yaml: missing module states {missing_modules}.")
    return errors


def print_module_list(catalog: dict[str, Any]) -> None:
    print("Research tool modules:")
    defaults = set((catalog.get("local_policy") or {}).get("default_enabled_modules") or [])
    for module_id, module in catalog["modules"].items():
        marker = "default" if module_id in defaults else "opt-in"
        print(f"- {module_id}: {module.get('status')} ({marker}) - {module.get('title')}")


def print_profile_plan(profile_id: str, catalog: dict[str, Any]) -> None:
    profile = catalog["profiles"].get(profile_id)
    if profile is None:
        available = ", ".join(sorted(catalog["profiles"]))
        raise SystemExit(f"Unknown profile {profile_id!r}. Available: {available}")
    print(f"Profile: {profile_id} - {profile['title']}")
    print()
    print("Default modules:")
    for module_id in as_list(profile.get("default_modules")):
        module = catalog["modules"][module_id]
        print(f"- {module_id}: {module['title']} ({module['maturity_level']})")
    optional = as_list(profile.get("optional_modules"))
    if optional:
        print()
        print("Optional modules:")
        for module_id in optional:
            module = catalog["modules"][module_id]
            print(f"- {module_id}: {module['title']} ({module['status']})")
    first_commands = as_list(profile.get("first_commands"))
    if first_commands:
        print()
        print("First commands:")
        for command in first_commands:
            print(f"- {command}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Template Research tool modules.")
    parser.add_argument("--list", action="store_true", help="Print catalog modules.")
    parser.add_argument("--profile", help="Print an activation plan for a profile id.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_catalog()
    module_config = read_yaml(MODULE_CONFIG_PATH)

    errors = validate_root_contract()
    errors.extend(validate_catalog(catalog))
    errors.extend(validate_profiles(catalog))
    errors.extend(validate_module_config(catalog, module_config))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.list:
        print_module_list(catalog)
    if args.profile:
        print_profile_plan(args.profile, catalog)
    if not args.list and not args.profile:
        print(
            "Tool module audit passed: "
            f"{len(catalog['modules'])} modules, {len(catalog['profiles'])} profiles."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
