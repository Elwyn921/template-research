from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_script_module(name: str) -> ModuleType:
    spec = spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_figure_contracts = load_script_module("audit_figure_contracts")
build_paperviz_input = load_script_module("build_paperviz_input")
validate_brief = audit_figure_contracts.validate_brief
require_paperviz_compatible_mode = build_paperviz_input.require_paperviz_compatible_mode


def minimal_brief(mode: str = "image") -> dict[str, object]:
    return {
        "id": "FIG-TEST",
        "title": "Test figure",
        "figure_type": "graphical-abstract",
        "mode": mode,
        "paper_claim": "A traceable figure must preserve source grounding.",
        "figure_goal": "Create a test figure.",
        "panels": [{"name": "Panel", "content": "Conceptual content only."}],
        "must_keep_labels": ["Panel"],
        "forbidden_content": ["invented values"],
        "style_constraints": ["publication style"],
        "verification_checklist": ["No unsupported claims are introduced."],
    }


def write_brief(tmp_path: Path, brief: dict[str, object]) -> Path:
    path = tmp_path / "brief.yaml"
    path.write_text(yaml.safe_dump(brief, sort_keys=False), encoding="utf-8")
    return path


def test_existing_image_brief_passes_hard_gate() -> None:
    path = ROOT / "reports" / "paper" / "figures" / "briefs" / "example_concrete_ai_workflow.yaml"
    assert validate_brief(path) == []


def test_image_brief_with_data_requirements_fails(tmp_path: Path) -> None:
    brief = minimal_brief()
    brief["data_requirements"] = {"source_paths": ["data/raw/source.csv"]}
    errors = validate_brief(write_brief(tmp_path, brief))

    assert any("mode:image cannot define data_requirements" in error for error in errors)


def test_plot_brief_requires_source_paths(tmp_path: Path) -> None:
    brief = minimal_brief(mode="plot")
    brief["figure_type"] = "data-figure"
    brief["plot_spec"] = {"chart_family": "bar"}
    brief["output_record"] = {"figure_path": "outputs/figures/test.png"}
    errors = validate_brief(write_brief(tmp_path, brief))

    assert any("mode:plot requires data_requirements" in error for error in errors)
    assert any("mode:plot requires data_requirements.source_paths" in error for error in errors)


def test_paperviz_rejects_plot_mode() -> None:
    brief = minimal_brief(mode="plot")

    with pytest.raises(SystemExit, match="mode: plot"):
        require_paperviz_compatible_mode(brief, Path("brief.yaml"))
