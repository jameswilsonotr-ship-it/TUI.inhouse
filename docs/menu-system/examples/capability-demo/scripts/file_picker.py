#!/usr/bin/env python3
"""PR-14 sample — file path selection (prompt / --path).

Obeys docs/menu-system/CODE-CALL-DISPLAY.md.
Host may pass --path for non-interactive tests.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Resolve a path and print markdown result."""
    p = argparse.ArgumentParser(description="File picker demo for TUI menu output")
    p.add_argument("--path", default=None, help="Non-interactive path (tests/CI)")
    args = p.parse_args(argv)

    print("TUI_RENDER: markdown", flush=True)
    print("TUI_TITLE: File picker", flush=True)

    pack = Path(os.environ.get("TUI_PACK_ROOT", ".")).resolve()
    chosen: Path | None = None

    if args.path:
        chosen = Path(args.path).expanduser()
    else:
        # Simple listing of pack root (no Textual modal in v1 subprocess)
        entries = sorted(pack.iterdir(), key=lambda x: x.name.lower())[:30]
        print("## File picker (sample)\n", flush=True)
        print(f"Pack root: `{pack}`\n", flush=True)
        print("Pass `--path PATH` for non-interactive use.\n", flush=True)
        print("| # | Name | Type |", flush=True)
        print("|---|------|------|", flush=True)
        for i, e in enumerate(entries, 1):
            kind = "dir" if e.is_dir() else "file"
            print(f"| {i} | `{e.name}` | {kind} |", flush=True)
        # Default pick: first file or pack root
        files = [e for e in entries if e.is_file()]
        chosen = files[0] if files else pack
        print(f"\n_Auto-selected for demo:_ `{chosen}`\n", flush=True)

    chosen = chosen.resolve()
    exists = chosen.exists()
    print("## Result\n", flush=True)
    print(f"- **path:** `{chosen}`", flush=True)
    print(f"- **exists:** {exists}", flush=True)
    print(f"- **is_file:** {chosen.is_file() if exists else False}", flush=True)
    return 0 if exists or args.path else 0


if __name__ == "__main__":
    raise SystemExit(main())
