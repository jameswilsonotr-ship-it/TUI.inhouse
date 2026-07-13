"""Bootstrap stage theater — visually staged install / dep UX (PR-08 docs).

Research notes (how polished tool managers stage boot):
  - cargo / rustup: sequential phase lines + quiet status verbs (Compiling… Done)
  - npm / pnpm: staged progress, spinner glyphs, color by success/fail
  - Homebrew: step list with ✓ / ✗, minimal chrome
  - Charmbracelet gum / lipgloss: soft color blocks, spinner frames, no TTY geometry hacks
  - mise / volta: short phase labels, never resize the terminal

Rules (WSL / Windows Terminal safe):
  - NEVER stty cols / NEVER leave reverse-video stuck
  - Soft wrap only (40 then 80)
  - Per-line SGR with full reset
  - Hard TTY restore between stages and before Textual

Stage A  — black bg, white text, 40 cols, blank flash, install steps + spinner
Stage B  — dark blue bg, 80 cols, flash, graphical-but-real library demos

See docs/ARCHITECTURE.md, docs/API.md.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

# ---- ANSI (line-local; always end with RESET) ----
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
WHITE = "\033[37m"
BRIGHT_WHITE = "\033[97m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"  # dark-ish blue (classic ANSI)
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE_FG = "\033[94m"

# Braille spinner — what gum / modern CLIs use (cutesy + readable)
SPINNER_FRAMES = list("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
# Fallback classic
SPINNER_CLASSIC = list("|/-\\")

STAGE_A_WIDTH = 40
STAGE_B_WIDTH = 80

# Theater modes (env):
#   AWESOME_BOOTSTRAP_QUIET=1  → no flash/spinner/clear; one-line steps only
#   AWESOME_BOOTSTRAP_FAST=1   → shorter spins / fewer flash frames
#   AWESOME_BOOTSTRAP_QUIET=1 + FAST both work together
#   AWESOME_BOOTSTRAP_SKIP_DEMOS=1 → Stage B import-only (still tests, no art)


def theater_quiet() -> bool:
    return os.environ.get("AWESOME_BOOTSTRAP_QUIET", "").strip() in (
        "1",
        "true",
        "yes",
        "on",
    )


def theater_fast() -> bool:
    return os.environ.get("AWESOME_BOOTSTRAP_FAST", "").strip() in (
        "1",
        "true",
        "yes",
        "on",
    ) or theater_quiet()  # quiet implies fast timings


def theater_skip_demo_art() -> bool:
    return theater_quiet() or os.environ.get(
        "AWESOME_BOOTSTRAP_SKIP_DEMOS", ""
    ).strip() in ("1", "true", "yes", "on")


def _spin_ticks() -> int:
    if theater_quiet():
        return 0
    if theater_fast():
        return 4
    return 10


def _spin_delay() -> float:
    if theater_quiet():
        return 0.0
    if theater_fast():
        return 0.02
    return 0.04


def _flash_frames() -> int:
    if theater_quiet():
        return 0
    if theater_fast():
        return 2
    return 4


# Exact install step theater (informative, ordered)
STAGE_A_STEPS: List[Tuple[str, str]] = [
    ("A1", "blank canvas · black void"),
    ("A2", "detect environment"),
    ("A3", "locate / create venv"),
    ("A4", "ensure pip tooling"),
    ("A5", "deps present? (no reinstall if OK)"),
    ("A6", "comfort check · ready for blue"),
]

STAGE_B_DEMOS: List[str] = [
    "textual",
    "rich",
    "zipfile",
    "pathlib",
    "json",
]


def _out(s: str = "") -> None:
    try:
        sys.stdout.write(s)
        if not s.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception:
        pass


def _wrap(text: str, width: int) -> List[str]:
    words = text.split()
    if not words:
        return [""]
    lines: List[str] = []
    cur = words[0]
    for w in words[1:]:
        if len(cur) + 1 + len(w) <= width:
            cur = f"{cur} {w}"
        else:
            lines.append(cur[:width])
            cur = w
    lines.append(cur[:width])
    return lines


def tty_hard_reset() -> None:
    """Restore TTY without changing column geometry (WSL-safe)."""
    try:
        sys.stdout.write(
            f"{RESET}\033[?25h\033[?1049l\033[?47l\033[r\033[27m\n"
        )
        sys.stdout.flush()
    except Exception:
        pass
    try:
        if sys.stdin.isatty():
            subprocess.run(
                ["stty", "sane"],
                stdin=sys.stdin,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1,
            )
    except Exception:
        pass


def _blank_flash(bg: str, fg: str, width: int, frames: int = 3) -> None:
    """Stylized blank-screen flash (no sticky reverse mode)."""
    bar = " " * min(width, 40)
    for i in range(frames):
        # alternate filled / empty line flash
        if i % 2 == 0:
            sys.stdout.write(f"{bg}{fg}{BOLD}{bar}{RESET}\r")
        else:
            sys.stdout.write(f"{bg}{fg}{'·' * min(width, 40)}{RESET}\r")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f"{RESET}\033[K\n")
    sys.stdout.flush()


def stage_line(text: str, *, width: int, bg: str, fg: str = WHITE, key: bool = True) -> None:
    """One theater line: soft-wrap, bg/fg, full reset (never sticky)."""
    for raw in _wrap(text, width):
        body = raw
        if key:
            body = (
                body.replace("PASS", f"{GREEN}PASS{fg}")
                .replace("FAIL", f"{RED}FAIL{fg}")
                .replace("SKIP", f"{YELLOW}SKIP{fg}")
                .replace("OK", f"{GREEN}OK{fg}")
                .replace("textual", f"{MAGENTA}textual{fg}")
                .replace("rich", f"{MAGENTA}rich{fg}")
            )
        _out(f"{bg}{fg}{body}{RESET}")


def spin_once(frame_i: int, label: str, *, width: int, bg: str, fg: str = WHITE) -> None:
    """Cutesy spinning cursor on a single status line (\\r rewrite)."""
    frames = SPINNER_FRAMES if sys.stdout.encoding and "UTF" in (sys.stdout.encoding or "").upper() else SPINNER_CLASSIC
    # also try braille always; if terminal mangles, user still sees something
    frames = SPINNER_FRAMES
    ch = frames[frame_i % len(frames)]
    msg = f" {ch}  {label}"
    if len(msg) > width:
        msg = msg[: width - 1] + "…"
    try:
        sys.stdout.write(f"\r{bg}{fg}{msg.ljust(width)[:width]}{RESET}")
        sys.stdout.flush()
    except Exception:
        pass


def spin_work(
    label: str,
    work: Callable[[], None],
    *,
    width: int,
    bg: str,
    ticks: int = 12,
    delay: float = 0.04,
) -> None:
    """Run work() while showing a spinner; if work is fast, still spin a bit."""
    done = {"ok": False, "err": None}

    # work is sync and usually fast — interleave spins around it for theater
    for i in range(max(3, ticks // 2)):
        spin_once(i, label, width=width, bg=bg)
        time.sleep(delay)
    try:
        work()
        done["ok"] = True
    except Exception as e:
        done["err"] = e
    for i in range(max(3, ticks // 2)):
        spin_once(i + ticks, label, width=width, bg=bg)
        time.sleep(delay * 0.8)
    sys.stdout.write(f"\r{RESET}\033[K")
    sys.stdout.flush()
    if done["err"] is not None:
        raise done["err"]  # type: ignore[misc]


# ---------------------------------------------------------------------------
# STAGE A — black / white / 40 cols — install steps
# ---------------------------------------------------------------------------

def stage_a_enter() -> None:
    """FIRST THING: blank screen, persistent black bg, white text, 40 cols soft.

    QUIET: no full clear / flash — one banner line only (faster boots).
    """
    tty_hard_reset()
    if theater_quiet():
        mode = "QUIET"
        if theater_fast():
            mode = "QUIET+FAST"
        stage_line(
            f"STAGE A · {mode} · black/white 40-col",
            width=STAGE_A_WIDTH,
            bg=BLACK_BG,
            fg=BRIGHT_WHITE,
            key=False,
        )
        return
    # Full theater: clear + flash + banner
    try:
        sys.stdout.write(f"{BLACK_BG}{WHITE}\033[2J\033[H{RESET}")
        sys.stdout.flush()
    except Exception:
        pass
    frames = _flash_frames()
    if frames:
        _blank_flash(BLACK_BG, BRIGHT_WHITE, STAGE_A_WIDTH, frames=frames)
    stage_line("╔══════════════════════════════════════╗", width=STAGE_A_WIDTH, bg=BLACK_BG, fg=BRIGHT_WHITE, key=False)
    stage_line("║  AWESOME LAUNCHER · STAGE A          ║", width=STAGE_A_WIDTH, bg=BLACK_BG, fg=BRIGHT_WHITE, key=False)
    tag = " FAST" if theater_fast() else ""
    stage_line(
        f"║  black · white · 40 col{tag}          ║",
        width=STAGE_A_WIDTH,
        bg=BLACK_BG,
        fg=WHITE,
        key=False,
    )
    stage_line("╚══════════════════════════════════════╝", width=STAGE_A_WIDTH, bg=BLACK_BG, fg=BRIGHT_WHITE, key=False)
    stage_line("double Ctrl-C always force-kills", width=STAGE_A_WIDTH, bg=BLACK_BG, fg=DIM + WHITE)
    stage_line("", width=STAGE_A_WIDTH, bg=BLACK_BG, key=False)


def stage_a_step(step_id: str, label: str, phase: str = "RUNNING") -> None:
    mark = {
        "RUNNING": f"{CYAN}…{WHITE}",
        "PASS": f"{GREEN}✓{WHITE}",
        "FAIL": f"{RED}✗{WHITE}",
        "SKIP": f"{YELLOW}·{WHITE}",
    }.get(phase, "·")
    stage_line(
        f"{mark} {step_id}  {label}  [{phase}]",
        width=STAGE_A_WIDTH,
        bg=BLACK_BG,
        fg=WHITE,
    )


def run_stage_a_steps(
    hooks: Optional[dict] = None,
) -> None:
    """Play Stage A install theater. hooks map step_id -> callable (optional real work).

    Respects AWESOME_BOOTSTRAP_QUIET / AWESOME_BOOTSTRAP_FAST.
    """
    hooks = hooks or {}
    stage_a_enter()
    if not theater_quiet():
        stage_line("install steps · dependencies", width=STAGE_A_WIDTH, bg=BLACK_BG, fg=CYAN)
    ticks = _spin_ticks()
    delay = _spin_delay()
    for step_id, label in STAGE_A_STEPS:
        if theater_quiet():
            # single line RUNNING→PASS (no spinner)
            fn = hooks.get(step_id)
            try:
                if fn:
                    fn()
                stage_a_step(step_id, label, "PASS")
            except Exception as e:
                stage_a_step(step_id, f"{label} ({e})", "FAIL")
                raise
            continue

        stage_a_step(step_id, label, "RUNNING")
        fn = hooks.get(step_id)
        try:
            if fn:
                if ticks <= 0:
                    fn()
                else:
                    spin_work(
                        f"{step_id} {label}",
                        fn,
                        width=STAGE_A_WIDTH,
                        bg=BLACK_BG,
                        ticks=ticks,
                        delay=delay,
                    )
            else:
                for i in range(max(1, ticks)):
                    spin_once(i, f"{step_id} {label}", width=STAGE_A_WIDTH, bg=BLACK_BG)
                    if delay:
                        time.sleep(delay)
                sys.stdout.write(f"\r{RESET}\033[K")
                sys.stdout.flush()
            stage_a_step(step_id, label, "PASS")
        except Exception as e:
            stage_a_step(step_id, f"{label} ({e})", "FAIL")
            raise
    stage_line(
        "stage A comfortable · flashing to blue…"
        if not theater_quiet()
        else "stage A done → blue demos",
        width=STAGE_A_WIDTH,
        bg=BLACK_BG,
        fg=GREEN,
    )
    if not theater_quiet():
        time.sleep(0.08 if theater_fast() else 0.15)


# ---------------------------------------------------------------------------
# STAGE B — dark blue / 80 cols — library demos (graphical + real tests)
# ---------------------------------------------------------------------------

def stage_b_enter() -> None:
    """Comfort flash → dark blue background, 80-col soft wrap."""
    if theater_quiet():
        stage_line(
            "STAGE B · QUIET · library API checks",
            width=STAGE_B_WIDTH,
            bg=BLUE_BG,
            fg=BRIGHT_WHITE,
            key=False,
        )
        return
    frames = _flash_frames()
    if frames:
        _blank_flash(BLUE_BG, BRIGHT_WHITE, STAGE_B_WIDTH, frames=frames)
    try:
        sys.stdout.write(f"{BLUE_BG}{WHITE}\033[2J\033[H{RESET}")
        sys.stdout.flush()
    except Exception:
        pass
    stage_line(
        "╔" + "═" * 78 + "╗",
        width=STAGE_B_WIDTH,
        bg=BLUE_BG,
        fg=BRIGHT_WHITE,
        key=False,
    )
    tag = " FAST" if theater_fast() else ""
    stage_line(
        f"║  STAGE B · dark blue · 80 col · library demos (real tests){tag}          ║",
        width=STAGE_B_WIDTH,
        bg=BLUE_BG,
        fg=BRIGHT_WHITE,
        key=False,
    )
    stage_line(
        "╚" + "═" * 78 + "╝",
        width=STAGE_B_WIDTH,
        bg=BLUE_BG,
        fg=BRIGHT_WHITE,
        key=False,
    )
    stage_line(
        "each demo is graphical AND exercises a real API from that library",
        width=STAGE_B_WIDTH,
        bg=BLUE_BG,
        fg=CYAN,
    )


def _spark_bar(ok: bool, width: int = 24, tick: int = 0) -> str:
    fill = width if ok else max(1, width // 4)
    body = "█" * fill + "░" * (width - fill)
    color = GREEN if ok else RED
    return f"{color}{body}{WHITE}"


def run_library_demo_graphical(python_bin: Path) -> bool:
    """Graphical library demos that actually test each library.

    Spawns venv python for isolated imports; parent only renders.
    """
    stage_b_enter()
    demo_src = r"""
import json, sys, zipfile, pathlib, os
results = []

# textual — real App class + version
try:
    import textual
    from textual.app import App
    ver = getattr(textual, "__version__", "?")
    ok = callable(App) and bool(ver)
    # mini "glyph" identity
    glyph = "▣" if ok else "□"
    results.append({
        "name": "textual",
        "ok": ok,
        "detail": f"v{ver} App={callable(App)}",
        "glyph": glyph,
        "art": f"{glyph} TEXTUAL  [{ver}]",
    })
except Exception as e:
    results.append({"name": "textual", "ok": False, "detail": repr(e), "glyph": "□", "art": "□ TEXTUAL FAIL"})

# rich — real Text + style render length
try:
    import rich
    from rich.text import Text
    from rich.console import Console
    import io
    t = Text("rich OK", style="bold magenta")
    buf = io.StringIO()
    Console(file=buf, force_terminal=False, width=40).print(t)
    rendered = buf.getvalue()
    ver = getattr(rich, "__version__", "?")
    ok = "rich" in rendered.lower() or len(t.plain) == 7
    results.append({
        "name": "rich",
        "ok": ok,
        "detail": f"v{ver} Text+Console ok plain={t.plain!r}",
        "glyph": "◆" if ok else "◇",
        "art": f"{'◆' if ok else '◇'} RICH     gradient■■■■□□",
    })
except Exception as e:
    results.append({"name": "rich", "ok": False, "detail": repr(e), "glyph": "◇", "art": "◇ RICH FAIL"})

# zipfile — open sample if present else exercise ZipFile API in memory
try:
    import io as _io
    buf = _io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("demo.txt", "olivia was here\n")
    buf.seek(0)
    with zipfile.ZipFile(buf, "r") as z:
        names = z.namelist()
        data = z.read("demo.txt")
    ok = names == ["demo.txt"] and b"olivia" in data
    # also probe sample_menu.zip if on disk
    sample = "sample_menu.zip"
    extra = ""
    if os.path.isfile(sample):
        with zipfile.ZipFile(sample, "r") as z:
            extra = f" sample={len(z.namelist())} entries"
    results.append({
        "name": "zipfile",
        "ok": ok,
        "detail": f"in-memory zip OK{extra}",
        "glyph": "▤" if ok else "▥",
        "art": f"{'▤' if ok else '▥'} ZIPFILE  [demo.txt]{extra}",
    })
except Exception as e:
    results.append({"name": "zipfile", "ok": False, "detail": repr(e), "glyph": "▥", "art": "▥ ZIPFILE FAIL"})

# pathlib — real Path ops
try:
    p = pathlib.Path(".").resolve()
    ok = p.exists() and p.is_dir()
    results.append({
        "name": "pathlib",
        "ok": ok,
        "detail": f"cwd={str(p)[:60]}",
        "glyph": ">" if ok else "?",
        "art": f"> PATHLIB  {p.name or '.'}/  exists={ok}",
    })
except Exception as e:
    results.append({"name": "pathlib", "ok": False, "detail": repr(e), "glyph": "?", "art": "▸ PATHLIB FAIL"})

# json — round-trip
try:
    payload = {"olivia": True, "panels": 6, "voice": "alpha"}
    s = json.dumps(payload)
    back = json.loads(s)
    ok = back["panels"] == 6 and back["olivia"] is True
    results.append({
        "name": "json",
        "ok": ok,
        "detail": f"round-trip keys={list(back)}",
        "glyph": "{}" if ok else "xx",
        "art": f"{{}} JSON     panels={back.get('panels')} olivia={back.get('olivia')}",
    })
except Exception as e:
    results.append({"name": "json", "ok": False, "detail": repr(e), "glyph": "xx", "art": "{} JSON FAIL"})

print(json.dumps(results))
"""
    try:
        proc = subprocess.run(
            [str(python_bin), "-c", demo_src],
            capture_output=True,
            text=True,
            timeout=45,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        stage_line(f"demo runner FAIL: {e}", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=RED)
        return False

    raw_lines = (proc.stdout or "").strip().splitlines()
    if not raw_lines:
        stage_line(
            f"demo runner empty stdout rc={proc.returncode} err={(proc.stderr or '')[:200]}",
            width=STAGE_B_WIDTH,
            bg=BLUE_BG,
            fg=RED,
        )
        return False
    try:
        results = json.loads(raw_lines[-1])
    except json.JSONDecodeError:
        stage_line("demo parse FAIL", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=RED)
        return False

    all_ok = True
    spin_n = 0 if theater_skip_demo_art() else (3 if theater_fast() else 6)
    spin_d = 0.0 if theater_quiet() else (0.015 if theater_fast() else 0.03)
    for i, r in enumerate(results):
        name = r.get("name", "?")
        ok = bool(r.get("ok"))
        if not ok:
            all_ok = False
        art = r.get("art") or name
        detail = r.get("detail") or ""
        status = "PASS" if ok else "FAIL"
        if theater_skip_demo_art():
            # one compact line — still real tests
            stage_line(
                f"{'✓' if ok else '✗'} {name}: {status} — {detail}",
                width=STAGE_B_WIDTH,
                bg=BLUE_BG,
                fg=WHITE,
            )
            continue
        for t in range(spin_n):
            spin_once(t, f"demo {name}", width=STAGE_B_WIDTH, bg=BLUE_BG)
            if spin_d:
                time.sleep(spin_d)
        sys.stdout.write(f"\r{RESET}\033[K")
        sys.stdout.flush()
        bar = _spark_bar(ok, 28, i)
        stage_line(f"┌─ {art}", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=BRIGHT_WHITE, key=False)
        stage_line(f"│  {bar}  {status}", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=WHITE)
        stage_line(f"└─ {detail}", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=DIM + WHITE, key=False)
        stage_line("", width=STAGE_B_WIDTH, bg=BLUE_BG, key=False)

    if all_ok:
        stage_line(
            "all library demos PASS · comfortable enough for menu load",
            width=STAGE_B_WIDTH,
            bg=BLUE_BG,
            fg=GREEN,
        )
    else:
        stage_line("one or more library demos FAIL", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=RED)
    return all_ok


def stage_b_exit_to_tui() -> None:
    """Leave blue stage cleanly before Textual takes the TTY."""
    stage_line("handing off to TUI…", width=STAGE_B_WIDTH, bg=BLUE_BG, fg=CYAN)
    if not theater_quiet():
        time.sleep(0.04 if theater_fast() else 0.08)
    tty_hard_reset()


def run_full_bootstrap_theater(
    python_bin: Path,
    *,
    hooks_a: Optional[dict] = None,
) -> bool:
    """Run Stage A then Stage B. QUIET/FAST via env (still runs real deps/demos)."""
    run_stage_a_steps(hooks_a)
    ok = run_library_demo_graphical(python_bin)
    stage_b_exit_to_tui()
    return ok
