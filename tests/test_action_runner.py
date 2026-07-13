"""PR-13 runtime tests — action_runner invoke protocol."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tui_chrome.action_runner import (  # noqa: E402
    build_argv,
    map_exit_level,
    run_action,
)
from tui_chrome.menu_model import load_pack_from_dir, leaf_items, merge_output_defaults, resolve_action  # noqa: E402


class TestActionRunner(unittest.TestCase):
    def test_map_exit_level(self) -> None:
        self.assertEqual(map_exit_level(0), 0)
        self.assertEqual(map_exit_level(2), 2)
        self.assertEqual(map_exit_level(1), 1)
        self.assertEqual(map_exit_level(99), 1)

    def test_build_argv_run_python(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        action = {
            "type": "run_python",
            "target": "scripts/wave.py",
            "args": {"frames": 2, "width": 10},
        }
        argv = build_argv(action, demo)
        self.assertEqual(argv[0], sys.executable)
        self.assertTrue(argv[1].endswith("wave.py"))
        self.assertIn("--frames", argv)
        self.assertIn("2", argv)

    def test_path_escape_rejected(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        action = {"type": "run_python", "target": "../secrets.py"}
        with self.assertRaises(ValueError):
            build_argv(action, demo)

    def test_run_wave_script(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        pack = load_pack_from_dir(demo)
        wave = next(n for n in leaf_items(pack.doc) if n.get("id") == "wave")
        action = merge_output_defaults(
            resolve_action(wave, pack.actions_registry) or {},
            pack.defaults,
        )
        # speed up
        action = dict(action)
        action["args"] = {"frames": 2, "width": 12, "delay": 0}
        lines: list[tuple[str, str]] = []
        with tempfile.TemporaryDirectory() as tmp:
            result = run_action(
                pack_root=pack.pack_root,
                menu_id=pack.id,
                item_id="wave",
                action=action,
                log_dir=Path(tmp),
                session_id="test",
                on_line=lambda s, t: lines.append((s, t)),
            )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.exit_level, 0)
        self.assertTrue(any(s == "out" for s, _ in lines))

    def test_run_file_picker_path(self) -> None:
        demo = ROOT / "docs" / "menu-system" / "examples" / "capability-demo"
        action = {
            "type": "run_python",
            "target": "scripts/file_picker.py",
            "args": {"path": str(demo / "menu.json")},
            "output": {"window": "main_output", "render_as": "markdown", "clear": True},
            "timeout_sec": 30,
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = run_action(
                pack_root=demo,
                menu_id="capability-demo",
                item_id="file_picker",
                action=action,
                log_dir=Path(tmp),
                session_id="test",
            )
        self.assertEqual(result.returncode, 0)
        self.assertIn("menu.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
