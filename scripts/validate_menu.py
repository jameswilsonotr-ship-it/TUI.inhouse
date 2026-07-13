#!/usr/bin/env python3
"""PR-11 — validate a menu pack (dir or zip) against menu.schema.json.

Usage:
  python scripts/validate_menu.py docs/menu-system/examples/capability-demo
  python scripts/validate_menu.py path/to/pack.zip

Exit 0 = OK, 1 = validation errors, 2 = usage/IO errors.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "menu-system" / "schema" / "menu.schema.json"


def load_json(path: Path) -> Any:
    """Load UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_legacy(doc: dict[str, Any]) -> dict[str, Any]:
    """Map legacy main_script menu.json → v1 shape (MENU-SYSTEM §9.1)."""
    if "schema_version" in doc and "menus" in doc:
        return doc
    if "main_script" in doc or ("name" in doc and "menus" not in doc):
        name = str(doc.get("name") or doc.get("id") or "legacy-menu")
        script = str(doc.get("main_script") or "harness.py")
        return {
            "schema_version": "1.0.0",
            "id": name,
            "title": name,
            "description": doc.get("description", ""),
            "version": doc.get("version", ""),
            "menus": [
                {
                    "id": "root",
                    "label": "Run harness",
                    "action": {"type": "legacy_harness", "target": script},
                }
            ],
        }
    return doc


def basic_validate(doc: dict[str, Any]) -> list[str]:
    """Lightweight required-field checks (no external jsonschema dependency)."""
    errs: list[str] = []
    for key in ("schema_version", "id", "title", "menus"):
        if key not in doc:
            errs.append(f"missing required field: {key}")
    if "menus" in doc:
        if not isinstance(doc["menus"], list) or not doc["menus"]:
            errs.append("menus must be a non-empty array")
        else:
            ids: set[str] = set()

            def walk(nodes: list, prefix: str) -> None:
                for n in nodes:
                    if not isinstance(n, dict):
                        errs.append(f"{prefix}: node not object")
                        continue
                    nid = n.get("id")
                    if not nid:
                        errs.append(f"{prefix}: node missing id")
                    elif nid in ids:
                        errs.append(f"duplicate menu id: {nid}")
                    else:
                        ids.add(str(nid))
                    if "label" not in n:
                        errs.append(f"node {nid!r} missing label")
                    kids = n.get("children")
                    if kids:
                        walk(kids, f"{prefix}/{nid}")

            walk(doc["menus"], "menus")
    return errs


def read_menu_from_pack(path: Path) -> dict[str, Any]:
    """Load menu.json from directory or zip."""
    if path.is_dir():
        menu = path / "menu.json"
        if not menu.is_file():
            raise FileNotFoundError(f"no menu.json in {path}")
        return load_json(menu)
    if path.is_file() and path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            # menu.json at root or single top folder
            candidates = [n for n in names if n.endswith("menu.json") and not n.endswith("/")]
            if not candidates:
                raise FileNotFoundError("zip has no menu.json")
            # prefer shortest path (root-most)
            candidates.sort(key=lambda n: (n.count("/"), len(n)))
            raw = zf.read(candidates[0]).decode("utf-8")
            return json.loads(raw)
    raise FileNotFoundError(f"not a menu pack: {path}")


def main(argv: list[str] | None = None) -> int:
    """CLI entry."""
    ap = argparse.ArgumentParser(description="Validate TUI menu pack (PR-11)")
    ap.add_argument("pack", type=Path, help="Menu pack directory or .zip")
    ap.add_argument(
        "--no-legacy-normalize",
        action="store_true",
        help="Do not normalize legacy main_script packs",
    )
    args = ap.parse_args(argv)

    try:
        doc = read_menu_from_pack(args.pack)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not args.no_legacy_normalize:
        doc = normalize_legacy(doc)

    errs = basic_validate(doc)
    # Optional full schema if jsonschema installed
    try:
        import jsonschema  # type: ignore

        schema = load_json(SCHEMA_PATH)
        validator = jsonschema.Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(doc), key=lambda x: list(x.path)):
            errs.append(e.message)
    except ImportError:
        print("note: jsonschema not installed — basic checks only", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        errs.append(f"schema validation error: {exc}")

    if errs:
        print(f"INVALID {args.pack}")
        for e in errs:
            print(f"  - {e}")
        return 1

    print(f"OK {args.pack}  id={doc.get('id')!r}  schema_version={doc.get('schema_version')!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
