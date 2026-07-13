#!/usr/bin/env python3
"""PR-14 sample — wavy motion frames to stdout (ANSI/log).

Obeys docs/menu-system/CODE-CALL-DISPLAY.md.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import time


def main(argv: list[str] | None = None) -> int:
    """Print a sine-wave animation; exit 0."""
    p = argparse.ArgumentParser(description="Wave motion demo for TUI menu output")
    p.add_argument("--frames", type=int, default=40)
    p.add_argument("--width", type=int, default=48)
    p.add_argument("--delay", type=float, default=0.03)
    args = p.parse_args(argv)

    # Prefer ANSI when host asked for it
    render = os.environ.get("TUI_RENDER_AS", "log")
    if render == "ansi":
        print("TUI_RENDER: ansi", flush=True)
    print("TUI_TITLE: Wave motion", flush=True)

    width = max(16, min(args.width, 120))
    frames = max(1, args.frames)
    for t in range(frames):
        phase = t / 4.0
        line = []
        for x in range(width):
            y = math.sin(x / 3.5 + phase)
            if y > 0.6:
                ch = "█"
            elif y > 0.2:
                ch = "▓"
            elif y > -0.2:
                ch = "▒"
            elif y > -0.6:
                ch = "░"
            else:
                ch = " "
            line.append(ch)
        # carriage-return style single line when TTY; else one frame per line
        frame = "".join(line)
        if sys.stdout.isatty():
            sys.stdout.write("\r" + frame)
            sys.stdout.flush()
        else:
            print(frame, flush=True)
        time.sleep(max(0.0, args.delay))
    if sys.stdout.isatty():
        print(flush=True)
    print(f"wave done frames={frames} width={width}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
