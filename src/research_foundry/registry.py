from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from research_foundry.paths import root_path

REGISTRY_DIR = root_path("tool_fabric", "registry")


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def registry_path(name: str) -> Path:
    return REGISTRY_DIR / name


def load_tools() -> dict[str, dict[str, Any]]:
    data = read_yaml(registry_path("tools.yaml"))
    tools = data.get("tools")
    if not isinstance(tools, dict):
        raise ValueError("tools.yaml must contain a tools mapping")
    return tools


def load_packs_registry() -> dict[str, dict[str, Any]]:
    data = read_yaml(registry_path("packs.yaml"))
    packs = data.get("packs")
    if not isinstance(packs, dict):
        raise ValueError("packs.yaml must contain a packs mapping")
    return packs


def load_profiles() -> dict[str, dict[str, Any]]:
    data = read_yaml(registry_path("profiles.yaml"))
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("profiles.yaml must contain a profiles mapping")
    return profiles


def load_adapters() -> dict[str, dict[str, Any]]:
    data = read_yaml(registry_path("adapters.yaml"))
    adapters = data.get("adapters")
    if not isinstance(adapters, dict):
        raise ValueError("adapters.yaml must contain an adapters mapping")
    return adapters


def load_compatibility() -> dict[str, Any]:
    return read_yaml(registry_path("compatibility_matrix.yaml"))


def load_dependency_matrix() -> dict[str, Any]:
    return read_yaml(registry_path("dependency_matrix.yaml"))


def list_pack_manifests() -> list[Path]:
    return sorted(root_path("packs").glob("*/pack.yaml"))
