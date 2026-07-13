"""PR-04 — Layout presets & panel chrome (Textual-oriented helpers).

Pattern ports inspired by Textual multi-pane apps / BBS window chrome —
not a vendored third-party tree. See docs/PR-04-layout-chrome.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

# Layout mode ids cycled by gallery
LAYOUT_MODES: List[str] = [
    "six_grid",        # 2×3
    "three_vertical",  # 3 columns, 2 rows stacked in each mentally
    "two_stack_h",     # 2 stacked left + horizontal band
    "main_sidebar",    # big main + side stack
    "two_plus_row",    # 2 on top, 4 in row
]


@dataclass(frozen=True)
class PanelSpec:
    id: str
    title: str
    index: int


DEFAULT_PANELS: List[PanelSpec] = [
    PanelSpec("p0", "① MENUS", 0),
    PanelSpec("p1", "② NESTED", 1),
    PanelSpec("p2", "③ LOGS", 2),
    PanelSpec("p3", "④ EFFECTS", 3),
    PanelSpec("p4", "⑤ LAYOUT", 4),
    PanelSpec("p5", "⑥ ABOUT", 5),
]


def next_layout(current: str) -> str:
    try:
        i = LAYOUT_MODES.index(current)
    except ValueError:
        return LAYOUT_MODES[0]
    return LAYOUT_MODES[(i + 1) % len(LAYOUT_MODES)]


def circle_index(i: int, delta: int, n: int = 6) -> int:
    return (i + delta) % n


# Shared TCSS fragment (also in chrome.tcss)
CHROME_CSS = """
/* PR-04 layout chrome */
.panel {
    border: heavy #664466;
    background: #120810;
    margin: 0 1;
    padding: 0 1;
    height: 1fr;
}
.panel.focused {
    border: double #ff44aa;
    background: #1a0a14;
}
.panel-title {
    text-style: bold;
    color: #ff88cc;
    background: #220018;
    padding: 0 1;
}
.panel-body {
    color: #e8d0e0;
    height: 1fr;
}
#gallery-help {
    dock: bottom;
    height: 3;
    background: #0a0a12;
    color: #88ffaa;
    padding: 0 1;
}
#gallery-status {
    dock: top;
    height: 1;
    background: #180012;
    color: #ffcc00;
    text-style: bold;
}
LayoutScreen, GalleryScreen {
    background: #0a0610;
}
"""


def layout_description(mode: str) -> str:
    return {
        "six_grid": "2×3 grid — six equal panels",
        "three_vertical": "three vertical columns (2 panels stacked each)",
        "two_stack_h": "two stacked on left · four in horizontal band",
        "main_sidebar": "one large main (p0) · sidebar stack p1–p5",
        "two_plus_row": "two on top · four along bottom row",
    }.get(mode, mode)
