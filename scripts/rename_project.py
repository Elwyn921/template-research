from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deprecated compatibility entrypoint. Use bootstrap/export scripts instead."
    )
    parser.add_argument("args", nargs="*")
    parser.parse_args()
    print(
        "scripts/rename_project.py is deprecated in Research Foundry. "
        "Use scripts/bootstrap_research_os.py and scripts/export_project_capabilities.py."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
