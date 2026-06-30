from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def root_path(*parts: str) -> Path:
    """Return a path rooted at the repository directory."""
    return ROOT.joinpath(*parts)
