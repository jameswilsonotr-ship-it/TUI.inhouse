"""PR-06 — ANSI/ASCII strobe, glitter, sparkle (stdlib only).

Classic BBS energy. No Textual dependency so install.sh can reuse later.
"""
from __future__ import annotations

import random
import time
from typing import Iterator, List

# ANSI helpers
RESET = "\033[0m"
BOLD = "\033[1m"
COLORS = [
    "\033[31m",  # red
    "\033[35m",  # magenta
    "\033[91m",  # bright red
    "\033[95m",  # bright magenta
    "\033[33m",  # yellow
    "\033[96m",  # cyan
]
SPARKLE_CHARS = list(".*+·✦✧★☆✦*·+.")
GLITTER_CHARS = list("░▒▓█·✦*+☆")


def strip_ansi(s: str) -> str:
    import re
    return re.sub(r"\033\[[0-9;]*m", "", s)


def strobe_frame(text: str, tick: int) -> str:
    """Alternate high-heat colors around text."""
    c = COLORS[tick % len(COLORS)]
    return f"{BOLD}{c}{text}{RESET}"


def glitter_line(width: int = 40, tick: int = 0, seed: int | None = None) -> str:
    rng = random.Random((seed or 0) + tick)
    return "".join(rng.choice(GLITTER_CHARS) for _ in range(width))


def sparkle_field(rows: int = 5, width: int = 36, tick: int = 0) -> str:
    lines = []
    for r in range(rows):
        line = []
        for c in range(width):
            # deterministic-ish twinkle
            on = (tick + r * 3 + c * 7) % 11 == 0
            line.append(SPARKLE_CHARS[(tick + r + c) % len(SPARKLE_CHARS)] if on else " ")
        lines.append("".join(line))
    return "\n".join(lines)


def banner_crawl(msg: str, width: int = 42, tick: int = 0) -> str:
    pad = "   " + msg + "   "
    if not pad:
        return " " * width
    i = tick % len(pad)
    looped = (pad + pad)[i : i + width]
    return looped.ljust(width)[:width]


def gutter_banner(tick: int = 0) -> str:
    frames = [
        "▓░▓░ GUTTER MODE ░▓░▓",
        "░▓░▓ PINK / BLACK ▓░▓░",
        "▓░▓░ C-64 RUINED  ░▓░▓",
        "★✦★  OLIVIA ALPHA  ★✦★",
        "░░▒▓ STROBE HEAT  ▓▒░░",
    ]
    return strobe_frame(frames[tick % len(frames)], tick)


def ascii_box(title: str, body: str, width: int = 44) -> str:
    """Double-line-ish ASCII box (pure text; Textual will draw real borders)."""
    inner = width - 2
    top = "╔" + "═" * inner + "╗"
    bot = "╚" + "═" * inner + "╝"
    t = (" " + title + " ")[:inner].center(inner, "═")
    mid_title = "║" + t + "║"
    lines = [top, mid_title, "║" + "─" * inner + "║"]
    for raw in body.splitlines() or [""]:
        chunk = raw[:inner].ljust(inner)
        lines.append("║" + chunk + "║")
    lines.append(bot)
    return "\n".join(lines)


def effect_demo_frames(seconds: float = 2.0, fps: float = 12.0) -> Iterator[str]:
    """Yield plain (no ANSI) frames for Textual Static widgets."""
    n = max(1, int(seconds * fps))
    for tick in range(n):
        body = "\n".join(
            [
                banner_crawl("*** GUTTER SPARKLE PARADE ***", 40, tick),
                glitter_line(40, tick),
                sparkle_field(4, 40, tick),
                glitter_line(40, tick + 3),
            ]
        )
        yield ascii_box("EFFECTS PR-06", strip_ansi(body), 42)
        time.sleep(1.0 / fps)


def panel_effect_text(panel_id: int, tick: int, mode: str = "sparkle") -> str:
    """Content for one gallery panel."""
    if mode == "strobe":
        return strip_ansi(gutter_banner(tick + panel_id))
    if mode == "crawl":
        return banner_crawl(f"PANEL {panel_id + 1} · NESTED MENUS · CIRCLE NAV", 34, tick)
    if mode == "glitter":
        return glitter_line(34, tick + panel_id * 5)
    # default sparkle
    return sparkle_field(3, 34, tick + panel_id)
