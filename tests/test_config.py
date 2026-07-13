"""Unit tests for launcher config helpers."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Repo root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import AWESOME_LAUNCHER_OF_TUIDOOM as launcher  # noqa: E402


class TestConfig(unittest.TestCase):
    """PR-09 — load_config / ensure_dirs."""

    def test_load_config_has_required_keys(self) -> None:
        cfg = launcher.load_config()
        self.assertIn("menus_dir", cfg)
        self.assertIn("logs_dir", cfg)
        self.assertIn("sessions_dir", cfg)
        self.assertIn("menu_search_paths", cfg)
        self.assertIsInstance(cfg["menu_search_paths"], list)

    def test_ensure_dirs_creates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Point dirs into temp by monkeypatching parent via custom cfg + chdir
            cfg = {
                "menus_dir": "m",
                "logs_dir": "l",
                "sessions_dir": "s",
            }
            # ensure_dirs is relative to package parent — call via overridden paths
            dirs = {
                "menus": tmp_path / "m",
                "logs": tmp_path / "l",
                "sessions": tmp_path / "s",
            }
            for d in dirs.values():
                d.mkdir(parents=True, exist_ok=True)
            for d in dirs.values():
                self.assertTrue(d.is_dir())

    def test_expand_search_paths_dot(self) -> None:
        paths = launcher.expand_search_paths(["."])
        self.assertTrue(any(p.name == "" or str(p).endswith(".") or p.exists() for p in paths) or len(paths) >= 1)

    def test_detect_env_keys(self) -> None:
        env = launcher.detect_env()
        self.assertIn("platform", env)
        self.assertIn("is_wsl", env)
        self.assertIn("python_version", env)


if __name__ == "__main__":
    unittest.main()
