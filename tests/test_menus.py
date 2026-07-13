"""Contract tests: zip menus + harness subprocess (PR-09)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import AWESOME_LAUNCHER_OF_TUIDOOM as launcher  # noqa: E402


class TestMenusAndHarness(unittest.TestCase):
    """Zip find/extract + demo harness exit contract."""

    def test_create_and_extract_demo_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            zip_path = tmp_path / "sample_menu.zip"
            launcher.create_demo_menu_zip(zip_path)
            self.assertTrue(zip_path.is_file())

            menus = tmp_path / "menus"
            menus.mkdir()
            extracted, main_script = launcher.extract_menu_zip(zip_path, menus)
            self.assertTrue(extracted.is_dir())
            self.assertEqual(main_script, "harness.py")
            self.assertTrue((extracted / "harness.py").is_file())
            self.assertTrue((extracted / "menu.json").is_file())

    def test_run_harness_once_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            zip_path = tmp_path / "sample_menu.zip"
            launcher.create_demo_menu_zip(zip_path)
            menus = tmp_path / "menus"
            menus.mkdir()
            extracted, main_script = launcher.extract_menu_zip(zip_path, menus)
            log_dir = tmp_path / "run_logs"
            result = launcher.run_harness_once(
                extracted,
                main_script,
                chunk="2026-06-20",
                log_dir=log_dir,
            )
            self.assertEqual(result["exit_level"], 0, msg=result)
            self.assertEqual(result["returncode"], 0, msg=result)
            self.assertTrue((log_dir / "processing.log").is_file())

    def test_run_harness_missing_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty"
            empty.mkdir()
            log_dir = Path(tmp) / "logs"
            result = launcher.run_harness_once(empty, "harness.py", None, log_dir)
            self.assertEqual(result["exit_level"], 1)
            self.assertIn("No harness", result["stderr"])

    def test_find_menu_zips_in_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            z = tmp_path / "a.zip"
            launcher.create_demo_menu_zip(z)
            found = launcher.find_menu_zips([str(tmp_path)])
            names = {p.name for p in found}
            self.assertIn("a.zip", names)

    def test_chunked_range_two_days(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            zip_path = tmp_path / "sample_menu.zip"
            launcher.create_demo_menu_zip(zip_path)
            menus = tmp_path / "menus"
            menus.mkdir()
            extracted, main_script = launcher.extract_menu_zip(zip_path, menus)
            log_dir = tmp_path / "run_logs"
            results = launcher.run_chunked_harness(
                extracted,
                main_script,
                start_chunk="2026-06-20",
                end_chunk="2026-06-21",
                log_dir=log_dir,
            )
            self.assertEqual(len(results), 2)
            self.assertTrue(all(r["exit_level"] == 0 for r in results), msg=results)


if __name__ == "__main__":
    unittest.main()
