#!/usr/bin/env python3
"""Full Olivia Dev + template enforcer (standalone-safe)."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "FOLDER-STANDARDS.md",
    "STANDALONE.md",
    "CHANGELOG.md",
    "TODO.md",
    "SUMMARY.md",
    "GHOST.0L1V.md",
    "OLIV.DIVA_GOES_HERE.md",
    ".research/dev-process-codified.md",
    "docs/DOCUMENTATION-STANDARDS.md",
    "docs/LINTING-STANDARDS.md",
    "docs/ARCHITECTURE.md",
    "specs/README.md",
    "specs/manifest.json",
    "src/README.md",
    "state/state.json",
    "state/state.md",
    "kanban/liv-kanban.md",
    "kanban/bunny-kanban.md",
    "backlog-wishlist/wishlist.md",
    "references/folder-discipline.md",
    "mermaid/folder-structure.mmd",
]

REQUIRED_DIRS = [
    ".aux/plans",
    ".aux/archive",
    ".aux/scratch",
    ".aux/logs",
    ".research/templates",
    "docs",
    "specs",
    "src",
    "scripts",
    "state",
    "versions/main",
    "backlog-wishlist",
    "kanban",
    "mermaid",
    "gutter-mode",
    "pirate-mode",
    "connectors",
    "imports",
    "tarballs",
    "references",
    "assets",
]


def main() -> int:
    issues: list[str] = []
    for f in REQUIRED_FILES:
        if not (ROOT / f).exists():
            issues.append(f"Missing file: {f}")
    for d in REQUIRED_DIRS:
        if not (ROOT / d).is_dir():
            issues.append(f"Missing dir: {d}")
    # standalone: no required absolute monorepo paths in config if present
    print(f"# enforcer  {datetime.now().isoformat(timespec='seconds')}")
    print(f"root: {ROOT}")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("OK: full Olivia Dev + template presence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
