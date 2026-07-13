"""Unit tests for tui_chrome.effects (stdlib, pure)."""
from __future__ import annotations

import unittest

from tui_chrome import effects


class TestEffects(unittest.TestCase):
    """PR-09 — ANSI / sparkle helpers stay deterministic and safe."""

    def test_strip_ansi_removes_sgr(self) -> None:
        raw = effects.strobe_frame("HI", 0)
        self.assertIn("\033[", raw)
        clean = effects.strip_ansi(raw)
        self.assertEqual(clean, "HI")
        self.assertNotIn("\033[", clean)

    def test_glitter_line_length_and_seed(self) -> None:
        a = effects.glitter_line(20, tick=1, seed=42)
        b = effects.glitter_line(20, tick=1, seed=42)
        c = effects.glitter_line(20, tick=1, seed=99)
        self.assertEqual(len(a), 20)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_sparkle_field_shape(self) -> None:
        field = effects.sparkle_field(rows=3, width=10, tick=0)
        lines = field.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(line) == 10 for line in lines))

    def test_banner_crawl_width(self) -> None:
        s = effects.banner_crawl("TEST", width=16, tick=3)
        self.assertEqual(len(s), 16)

    def test_ascii_box_contains_title(self) -> None:
        box = effects.ascii_box("TITLE", "body line", width=24)
        self.assertIn("TITLE", box)
        self.assertIn("body line", box)
        self.assertTrue(box.startswith("╔"))

    def test_panel_effect_modes(self) -> None:
        for mode in ("sparkle", "strobe", "crawl", "glitter"):
            text = effects.panel_effect_text(0, tick=2, mode=mode)
            self.assertIsInstance(text, str)
            self.assertGreater(len(text), 0)

    def test_gutter_banner_has_content(self) -> None:
        self.assertTrue(len(effects.strip_ansi(effects.gutter_banner(0))) > 0)


if __name__ == "__main__":
    unittest.main()
