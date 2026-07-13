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


def mount_layout(
    root,
    mode: str,
    panel_widgets: Sequence,
    *,
    Grid,
    Horizontal,
    Vertical,
) -> None:
    """Mount `panel_widgets` (len 6) into `root` using a gallery LAYOUT_MODE.

    Shared by GalleryScreen and OliviaSixPanelDemo so layout keys stay in sync.
    Callers pass Textual container classes (avoids hard import at module load).
    """
    root.remove_children()
    panels = list(panel_widgets)
    if len(panels) < 6:
        raise ValueError("mount_layout expects 6 panel widgets")

    if mode == "six_grid":
        grid = Grid(id="gallery-grid")
        root.mount(grid)
        for w in panels:
            grid.mount(w)

    elif mode == "three_vertical":
        cols = Horizontal(id="gallery-cols")
        root.mount(cols)
        for col_i in range(3):
            col = Vertical()
            cols.mount(col)
            for row in range(2):
                col.mount(panels[col_i * 2 + row])

    elif mode == "two_stack_h":
        row = Horizontal(id="gallery-twoh")
        root.mount(row)
        left = Vertical()
        right = Horizontal()
        row.mount(left)
        row.mount(right)
        left.mount(panels[0])
        left.mount(panels[1])
        for i in range(2, 6):
            right.mount(panels[i])

    elif mode == "main_sidebar":
        row = Horizontal(id="gallery-main")
        root.mount(row)
        main = Vertical(id="main-big")
        side = Vertical(id="side-stack")
        row.mount(main)
        row.mount(side)
        main.mount(panels[0])
        for i in range(1, 6):
            side.mount(panels[i])

    else:  # two_plus_row (default fallback)
        top = Horizontal()
        bot = Horizontal()
        root.mount(top)
        root.mount(bot)
        top.mount(panels[0])
        top.mount(panels[1])
        for i in range(2, 6):
            bot.mount(panels[i])
