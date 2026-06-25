from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "research_project"


def validate_slug(value: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", value):
        raise ValueError("Slug must start with a lowercase letter and contain only lowercase letters, digits, and underscores.")
    return value


def replace_text(path: Path, slug: str, title: str) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    updated = content.replace(PLACEHOLDER, slug).replace("Research Project", title)
    if updated != content:
        path.write_text(updated, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python scripts/rename_project.py <project_slug> "<Project Title>"')
    slug = validate_slug(sys.argv[1])
    title = sys.argv[2]
    old_package, new_package = ROOT / "src" / PLACEHOLDER, ROOT / "src" / slug
    if new_package.exists() and new_package != old_package:
        raise SystemExit(f"Destination package already exists: {new_package}")
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.name != "rename_project.py":
            replace_text(path, slug, title)
    if old_package.exists() and old_package != new_package:
        shutil.move(str(old_package), str(new_package))
    print(f"Renamed template package to '{slug}' and title to '{title}'.")
    print("Now run: uv lock && uv sync --all-extras --group dev")


if __name__ == "__main__":
    main()
