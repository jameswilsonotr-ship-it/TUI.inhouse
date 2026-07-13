"""PR-15 — default demo zip contains capability pack."""
from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import AWESOME_LAUNCHER_OF_TUIDOOM as launcher  # noqa: E402
from tui_chrome.menu_model import extract_and_load_zip, leaf_items  # noqa: E402


class TestDemoZip(unittest.TestCase):
    def test_create_demo_has_v1_menu_and_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "sample_menu.zip"
            launcher.create_demo_menu_zip(dest)
            self.assertTrue(dest.is_file())
            with zipfile.ZipFile(dest) as zf:
                names = set(zf.namelist())
            self.assertIn("menu.json", names)
            self.assertIn("scripts/wave.py", names)
            self.assertIn("scripts/file_picker.py", names)
            self.assertIn("scripts/web_search.py", names)
            self.assertIn("harness.py", names)
            self.assertIn("layout.json", names)
            self.assertIn("windows.json", names)

            menus = Path(tmp) / "menus"
            pack = extract_and_load_zip(dest, menus)
            self.assertEqual(pack.id, "capability-demo")
            ids = {n.get("id") for n in leaf_items(pack.doc)}
            self.assertIn("wave", ids)
            self.assertIn("legacy_chunk", ids)


if __name__ == "__main__":
    unittest.main()
