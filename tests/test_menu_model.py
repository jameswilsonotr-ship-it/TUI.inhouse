"""PR-11 runtime tests — menu_model load/normalize."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tui_chrome.menu_model import (  # noqa: E402
    extract_and_load_zip,
    leaf_items,
    load_pack_from_dir,
    merge_output_defaults,
    normalize_legacy,
    resolve_action,
)


class TestMenuModel(unittest.TestCase):
    def test_normalize_legacy(self) -> None:
        doc = normalize_legacy(
            {"name": "x", "main_script": "harness.py", "description": "d"}
        )
        self.assertEqual(doc["schema_version"], "1.0.0")
        self.assertEqual(doc["id"], "x")
        self.assertTrue(doc["menus"])
        action = doc["menus"][0]["action"]
        self.assertEqual(action["type"], "legacy_harness")

    def test_load_capability_demo_dir(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        pack = load_pack_from_dir(demo)
        self.assertEqual(pack.id, "capability-demo")
        leaves = leaf_items(pack.doc)
        self.assertGreaterEqual(len(leaves), 3)
        ids = {n.get("id") for n in leaves}
        self.assertIn("wave", ids)
        self.assertIn("web_search", ids)

    def test_resolve_and_merge_output(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        pack = load_pack_from_dir(demo)
        wave = next(n for n in leaf_items(pack.doc) if n.get("id") == "wave")
        action = resolve_action(wave, pack.actions_registry)
        assert action is not None
        merged = merge_output_defaults(action, pack.defaults)
        self.assertIn("output", merged)
        self.assertEqual(merged["output"]["window"], "main_output")

    def test_extract_zip_roundtrip(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        with tempfile.TemporaryDirectory() as tmp:
            zpath = Path(tmp) / "cap.zip"
            with zipfile.ZipFile(zpath, "w") as zf:
                zf.write(demo / "menu.json", "menu.json")
                for sp in (demo / "scripts").glob("*.py"):
                    zf.write(sp, f"scripts/{sp.name}")
            menus = Path(tmp) / "menus"
            pack = extract_and_load_zip(zpath, menus)
            self.assertEqual(pack.id, "capability-demo")
            self.assertTrue((pack.pack_root / "scripts" / "wave.py").is_file())


if __name__ == "__main__":
    unittest.main()
