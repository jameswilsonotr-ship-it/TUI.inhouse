"""PR-11 runtime — load and normalize menu packs (JSON v1 + legacy).

See docs/menu-system/MENU-SYSTEM.md and schema/menu.schema.json.
"""
from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union


ActionSpec = Dict[str, Any]
MenuNode = Dict[str, Any]


@dataclass
class MenuPack:
    """Loaded menu pack ready for the host UI."""

    pack_root: Path
    doc: Dict[str, Any]
    layout: Optional[Dict[str, Any]] = None
    windows: Optional[Dict[str, Any]] = None
    source: str = "dir"  # dir | zip

    @property
    def schema_version(self) -> str:
        return str(self.doc.get("schema_version") or "1.0.0")

    @property
    def id(self) -> str:
        return str(self.doc.get("id") or self.pack_root.name)

    @property
    def title(self) -> str:
        return str(self.doc.get("title") or self.id)

    @property
    def actions_registry(self) -> Dict[str, ActionSpec]:
        raw = self.doc.get("actions") or {}
        return raw if isinstance(raw, dict) else {}

    @property
    def defaults(self) -> Dict[str, Any]:
        d = self.doc.get("defaults") or {}
        return d if isinstance(d, dict) else {}


def normalize_legacy(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Map legacy ``main_script`` menu.json → v1 shape (MENU-SYSTEM §9.1)."""
    if isinstance(doc.get("menus"), list) and doc.get("schema_version"):
        return doc
    if "main_script" in doc or ("name" in doc and "menus" not in doc):
        name = str(doc.get("name") or doc.get("id") or "legacy-menu")
        script = str(doc.get("main_script") or "harness.py")
        return {
            "schema_version": "1.0.0",
            "id": name,
            "title": name,
            "description": doc.get("description", ""),
            "version": str(doc.get("version") or ""),
            "content_format": "markdown",
            "defaults": {
                "layout_id": "standard_menu",
                "output_window": "main_output",
                "render_as": "log",
            },
            "menus": [
                {
                    "id": "root",
                    "label": "Run harness",
                    "help": doc.get("description") or "Legacy harness",
                    "action": {
                        "type": "legacy_harness",
                        "target": script,
                        "output": {
                            "window": "main_output",
                            "render_as": "log",
                            "clear": True,
                            "stream": "both",
                        },
                    },
                }
            ],
        }
    # Ensure minimum fields
    out = dict(doc)
    out.setdefault("schema_version", "1.0.0")
    out.setdefault("id", "unnamed")
    out.setdefault("title", out["id"])
    out.setdefault("menus", [])
    return out


def basic_validate(doc: Dict[str, Any]) -> List[str]:
    """Required-field checks; returns list of error strings."""
    errs: List[str] = []
    for key in ("schema_version", "id", "title", "menus"):
        if key not in doc:
            errs.append(f"missing required field: {key}")
    menus = doc.get("menus")
    if not isinstance(menus, list) or not menus:
        errs.append("menus must be a non-empty array")
    return errs


def load_json_file(path: Path) -> Any:
    """Load UTF-8 JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON object file if present."""
    if path.is_file():
        data = load_json_file(path)
        return data if isinstance(data, dict) else None
    return None


def load_pack_from_dir(pack_root: Path) -> MenuPack:
    """Load a menu pack directory (must contain menu.json)."""
    pack_root = pack_root.resolve()
    menu_path = pack_root / "menu.json"
    if not menu_path.is_file():
        raise FileNotFoundError(f"no menu.json in {pack_root}")
    doc = normalize_legacy(load_json_file(menu_path))
    errs = basic_validate(doc)
    if errs:
        raise ValueError(f"invalid menu pack: {'; '.join(errs)}")
    layout = load_optional_json(pack_root / "layout.json")
    windows = load_optional_json(pack_root / "windows.json")
    return MenuPack(
        pack_root=pack_root,
        doc=doc,
        layout=layout,
        windows=windows,
        source="dir",
    )


def extract_and_load_zip(zip_path: Path, menus_dir: Path) -> MenuPack:
    """Extract zip into menus_dir/<stem>/ and load as MenuPack."""
    zip_path = zip_path.resolve()
    menus_dir = menus_dir.resolve()
    menus_dir.mkdir(parents=True, exist_ok=True)
    name = zip_path.stem
    target = menus_dir / name
    if target.exists():
        import shutil

        shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target)
    # If zip had a single top-level folder, descend into it when menu.json is there
    menu_json = target / "menu.json"
    if not menu_json.is_file():
        subs = [p for p in target.iterdir() if p.is_dir()]
        for sub in subs:
            if (sub / "menu.json").is_file():
                target = sub
                break
    pack = load_pack_from_dir(target)
    pack.source = "zip"
    return pack


def iter_menu_nodes(nodes: List[MenuNode], *, prefix: str = "") -> Iterator[Tuple[str, MenuNode]]:
    """Yield (path_id, node) depth-first."""
    for n in nodes:
        if not isinstance(n, dict):
            continue
        nid = str(n.get("id") or "")
        path = f"{prefix}/{nid}" if prefix else nid
        yield path, n
        kids = n.get("children")
        if isinstance(kids, list):
            yield from iter_menu_nodes(kids, prefix=path)


def leaf_items(doc: Dict[str, Any]) -> List[MenuNode]:
    """Runnable / navigable leaf items (not groups with only children)."""
    menus = doc.get("menus") or []
    if not isinstance(menus, list):
        return []
    leaves: List[MenuNode] = []
    for _path, node in iter_menu_nodes(menus):
        kind = node.get("kind") or "item"
        if kind == "separator":
            continue
        if kind == "group" and node.get("children"):
            continue
        if node.get("visible") is False:
            continue
        leaves.append(node)
    return leaves


def resolve_action(
    node: MenuNode,
    registry: Dict[str, ActionSpec],
) -> Optional[ActionSpec]:
    """Resolve node.action string id or inline ActionSpec."""
    action = node.get("action")
    if action is None:
        return None
    if isinstance(action, str):
        return dict(registry.get(action) or {})
    if isinstance(action, dict):
        return dict(action)
    return None


def merge_output_defaults(
    action: ActionSpec,
    pack_defaults: Dict[str, Any],
) -> ActionSpec:
    """Ensure action.output has window/render_as/stream/clear defaults."""
    out = dict(action)
    output = dict(out.get("output") or {})
    output.setdefault("window", pack_defaults.get("output_window") or "main_output")
    output.setdefault("render_as", pack_defaults.get("render_as") or "log")
    output.setdefault("stream", "both")
    output.setdefault("clear", True)
    output.setdefault("append", False)
    out["output"] = output
    if "timeout_sec" not in out and pack_defaults.get("action_timeout_sec") is not None:
        out["timeout_sec"] = pack_defaults["action_timeout_sec"]
    return out


def default_layout_doc() -> Dict[str, Any]:
    """Built-in standard_menu layout (PR-12)."""
    root = Path(__file__).resolve().parents[1]
    candidate = (
        root
        / "docs"
        / "menu-system"
        / "examples"
        / "layout.standard_menu.json"
    )
    if candidate.is_file():
        return load_json_file(candidate)
    return {
        "schema_version": "1.0.0",
        "id": "standard_menu",
        "panels": [
            {"id": "app_title", "role": "chrome"},
            {"id": "menu_tree", "role": "menu"},
            {"id": "item_help", "role": "content"},
            {"id": "main_output", "role": "output"},
            {"id": "key_help", "role": "chrome"},
        ],
        "bindings": [
            {"slot": "menu_tree", "panel": "menu_tree"},
            {"slot": "item_help", "panel": "item_help"},
            {"slot": "main_output", "panel": "main_output"},
        ],
    }


def default_windows_doc() -> Dict[str, Any]:
    """Default single main_output window (PR-13)."""
    return {
        "schema_version": "1.0.0",
        "windows": [
            {
                "id": "main_output",
                "panel": "main_output",
                "title": "Output",
                "streams": ["stdout", "stderr"],
                "render_as": "log",
                "buffer_lines": 5000,
                "show_exit_banner": True,
            }
        ],
    }
