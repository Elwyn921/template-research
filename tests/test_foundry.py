from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from research_foundry.exporter import export_project_capabilities
from research_foundry.registry import load_packs_registry, load_profiles, load_tools
from research_foundry.tool_plan import build_plan
from research_foundry.validation import (
    FORBIDDEN_CONTROLLER_NAMES,
    validate_export_boundary_paths,
    validate_foundry,
    validate_pack_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def test_foundry_validation_passes() -> None:
    assert validate_foundry() == []


def test_registry_ids_are_unique_and_non_empty() -> None:
    tools = load_tools()
    packs = load_packs_registry()
    profiles = load_profiles()

    assert len(tools) == len(set(tools))
    assert len(packs) == len(set(packs))
    assert len(profiles) == len(set(profiles))
    assert {"core_research_os", "concrete_ml", "advanced_figure"} <= set(packs)


def test_pack_references_registered_tools() -> None:
    tools = load_tools()
    for pack_path in sorted((ROOT / "packs").glob("*/pack.yaml")):
        pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
        for tool_id in pack["required_tool_ids"] + pack["optional_tool_ids"]:
            assert tool_id in tools
        assert not any((pack_path.parent / name).exists() for name in FORBIDDEN_CONTROLLER_NAMES)
        assert validate_pack_manifest(pack_path) == []


def test_resolver_skips_heavy_tools_without_trigger() -> None:
    plan = build_plan(
        project_type="empirical_materials",
        task="test domain shift and local calibration",
        stage="experiment",
        target_output="reproducible result and figure",
        profiles=["concrete_ml", "advanced_figure"],
    )

    assert "experiment" in plan["primary_tools"]
    assert "scikit_learn" in plan["primary_tools"]["experiment"]
    assert "mlflow" in plan["skipped_heavy_tools"]
    assert "dvc" in plan["skipped_heavy_tools"]


def test_resolver_activates_triggered_heavy_tool() -> None:
    plan = build_plan(
        project_type="empirical_materials",
        task="compare multiple model runs with parameter comparison and artifact tracing",
        stage="experiment",
        target_output="reproducible result and figure",
        profiles=["concrete_ml"],
    )

    assert "mlflow" in plan["conditional_tools"]


def test_export_boundary_rejects_protected_paths() -> None:
    errors = validate_export_boundary_paths(["AGENTS.md", "08_tools/TOOLFLOW.md"])
    assert errors


def test_exporter_writes_only_foundry_area(tmp_path: Path) -> None:
    project = tmp_path / "downstream"
    (project / "08_tools").mkdir(parents=True)
    (project / "AGENTS.md").write_text("# downstream agents\n", encoding="utf-8")
    (project / "08_tools" / "TOOLFLOW.md").write_text("# downstream toolflow\n", encoding="utf-8")

    report = export_project_capabilities(
        destination=project,
        project_type="empirical_materials",
        base_profile="base_research",
        domain_profile="concrete_ml",
        enhancement_profiles=["advanced_figure"],
        packs=["core_research_os", "concrete_ml", "advanced_figure"],
        release="v0.1.0-foundry",
        target="test",
    )

    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# downstream agents\n"
    assert (project / "08_tools" / "TOOLFLOW.md").read_text(
        encoding="utf-8"
    ) == "# downstream toolflow\n"
    assert (project / "08_tools" / "foundation_manifest.yaml").is_file()
    assert (project / "08_tools" / "foundry" / "resolved_tool_plan.md").is_file()
    assert all(
        path.startswith("08_tools/foundry/") or path == "08_tools/foundation_manifest.yaml"
        for path in report["files_exported"]
    )


def test_unknown_profile_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown profiles"):
        build_plan(
            project_type="empirical_materials",
            task="model",
            stage="experiment",
            target_output="result",
            profiles=["not_a_profile"],
        )
