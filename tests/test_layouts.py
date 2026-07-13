"""Unit tests for tui_chrome.layouts (no Textual App)."""
from __future__ import annotations

import unittest

from tui_chrome import layouts


class TestLayouts(unittest.TestCase):
    """PR-09 — layout mode cycling and panel math."""

    def test_layout_modes_nonempty(self) -> None:
        self.assertGreaterEqual(len(layouts.LAYOUT_MODES), 2)
        self.assertIn("six_grid", layouts.LAYOUT_MODES)

    def test_next_layout_cycles(self) -> None:
        first = layouts.LAYOUT_MODES[0]
        second = layouts.next_layout(first)
        self.assertEqual(second, layouts.LAYOUT_MODES[1])
        # full cycle returns to first
        cur = first
        for _ in range(len(layouts.LAYOUT_MODES)):
            cur = layouts.next_layout(cur)
        self.assertEqual(cur, first)

    def test_next_layout_unknown_resets(self) -> None:
        self.assertEqual(layouts.next_layout("not-a-mode"), layouts.LAYOUT_MODES[0])

    def test_circle_index(self) -> None:
        self.assertEqual(layouts.circle_index(0, 1, 6), 1)
        self.assertEqual(layouts.circle_index(5, 1, 6), 0)
        self.assertEqual(layouts.circle_index(0, -1, 6), 5)

    def test_default_panels_count(self) -> None:
        self.assertEqual(len(layouts.DEFAULT_PANELS), 6)
        self.assertEqual(layouts.DEFAULT_PANELS[0].id, "p0")

    def test_layout_description_known(self) -> None:
        desc = layouts.layout_description("six_grid")
        self.assertIn("grid", desc.lower())

    def test_mount_layout_requires_six(self) -> None:
        class DummyRoot:
            def remove_children(self) -> None:
                pass

            def mount(self, _w) -> None:
                pass

        with self.assertRaises(ValueError):
            layouts.mount_layout(
                DummyRoot(),
                "six_grid",
                [object()] * 3,
                Grid=object,
                Horizontal=object,
                Vertical=object,
            )


if __name__ == "__main__":
    unittest.main()
