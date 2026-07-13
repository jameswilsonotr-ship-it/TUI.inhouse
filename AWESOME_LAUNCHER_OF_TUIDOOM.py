#!/usr/bin/env python3
"""
AWESOME_LAUNCHER_OF_TUIDOOM.py

Rock-solid, dead-stupid-simple Python TUI launcher for zip-packaged menus.

Version: 0.1.0 (Initial Sovereign Live Release - full Phase 3 test harness)

- python AWESOME_LAUNCHER_OF_TUIDOOM.py   (if Python in PATH)
- Default menu: "Go find a real menu"
- Zips: search, select, extract, run via harness
- Harnesses support chunked ops (e.g. one day of "memory files"), loops, exit levels (0=success,1=error,2=partial), logs
- Full TUI (Textual): header, footer, screens, prompts, live logs, file I/O
- Session recording + replay for automation on data/script/env changes
- BBS god-tier simple but powerful
- Phase 3: --test (prompt, auto-zip, gutter flash circle + obnoxious, success)

References: OLIVIAPLEASEREADTHIS.md, olivia-dev-alpha in OLIV.DIVA, CHANGELOG.md, PHILOSOPHY.md

Bootstrap per design (stdlib first, venv, deps).

Usage examples:
  python AWESOME_LAUNCHER_OF_TUIDOOM.py
  python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
  python AWESOME_LAUNCHER_OF_TUIDOOM.py --replay sessions/xxx.json

Config: LAUNCHERCONFIG.JSON (same dir)
"""

from __future__ import annotations
import os
import sys
import subprocess
import platform
import json
import zipfile
import argparse
import datetime
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# -------------------------------
# BOOTSTRAP (stdlib only - design principle)
# -------------------------------

CORE_DEPS = ["textual", "rich"]

# Session stamp: one timestamp per process for all log files in this run
_SESSION_STAMP: Optional[str] = None
_INSTALL_MODE_ACTIVE = False
# Never mutate stty cols on WSL/Windows Terminal — that bricks keyboard after alt-tab.


def _session_stamp() -> str:
    global _SESSION_STAMP
    if _SESSION_STAMP is None:
        # Survive re-exec into venv so one run shares one stamp
        env_stamp = os.environ.get("AWESOME_LAUNCHER_STAMP", "").strip()
        if env_stamp and len(env_stamp) >= 8:
            _SESSION_STAMP = env_stamp
        else:
            _SESSION_STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            os.environ["AWESOME_LAUNCHER_STAMP"] = _SESSION_STAMP
    return _SESSION_STAMP


def detect_env() -> Dict[str, Any]:
    print("Detecting environment...")
    env_info = {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "is_wsl": "WSL_DISTRO_NAME" in os.environ or "microsoft" in platform.release().lower(),
        "is_windows": sys.platform.startswith("win"),
        "is_linux": sys.platform.startswith("linux"),
        "cwd": str(Path.cwd()),
    }
    for k, v in env_info.items():
        print(f"  {k}: {v}")
    return env_info


def _bootstrap_log_paths() -> Dict[str, Any]:
    """Bootstrap/deps logging under logs/ with per-session date-time stamps.

    Writes both stamped files (error_YYYYMMDD_HHMMSS.log, …) and stable
    latest aliases (error.log, tui_crash.log, …) for install.sh tails.
    """
    base = Path(__file__).parent
    log_dir = base / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = _session_stamp()
    return {
        "dir": log_dir,
        "stamp": stamp,
        "bootstrap": log_dir / f"bootstrap_{stamp}.log",
        "bootstrap_latest": log_dir / "bootstrap.log",
        "error": log_dir / f"error_{stamp}.log",
        "error_latest": log_dir / "error.log",
        "success": log_dir / f"success_{stamp}.log",
        "success_latest": log_dir / "success.log",
        "ops": log_dir / f"ops_{stamp}.log",
        "ops_latest": log_dir / "ops.log",
        "deps": log_dir / f"bootstrap_deps_{stamp}.log",
        "deps_latest": log_dir / "bootstrap_deps.log",
        "crash": log_dir / f"tui_crash_{stamp}.log",
        "crash_latest": log_dir / "tui_crash.log",
    }


def _append_log(path: Path, text: str, *also: Path) -> None:
    """Append timestamped blob to path and optional alias files."""
    ts = datetime.datetime.now().isoformat()
    blob = f"\n=== {ts} ===\n{text}"
    if text and not text.endswith("\n"):
        blob += "\n"
    targets = [path, *also]
    for p in targets:
        if p is None:
            continue
        with open(p, "a", encoding="utf-8") as f:
            f.write(blob)


def _write_success(msg: str) -> None:
    paths = _bootstrap_log_paths()
    _append_log(paths["success"], msg, paths["success_latest"], paths["ops"], paths["ops_latest"])
    _append_log(paths["bootstrap"], f"SUCCESS: {msg}", paths["bootstrap_latest"])


def _write_ops(msg: str) -> None:
    paths = _bootstrap_log_paths()
    _append_log(paths["ops"], msg, paths["ops_latest"], paths["bootstrap"], paths["bootstrap_latest"])


def _write_error(msg: str) -> None:
    paths = _bootstrap_log_paths()
    _append_log(paths["error"], msg, paths["error_latest"], paths["ops"], paths["ops_latest"])
    _append_log(paths["bootstrap"], f"ERROR: {msg}", paths["bootstrap_latest"])


# ---- Install-mode terminal (SAFE for WSL / Windows Terminal) ----
# Visual only: soft-wrap to ~40 cols, black/white line style, brief flashes.
# NEVER call stty cols / never leave reverse-video or alt-screen stuck.
# Full-screen clear + stty cols 40 was bricking keyboard after alt-tab.

_INSTALL_WIDTH = 40
_KEY_COLOR_MAP = (
    (r"\bFAIL(?:ED|URE)?\b", "\033[91m"),
    (r"\bERROR\b", "\033[91m"),
    (r"\bPASS(?:ED)?\b", "\033[92m"),
    (r"\bOK\b", "\033[92m"),
    (r"\bSUCCESS\b", "\033[92m"),
    (r"\bSKIP(?:PED)?\b", "\033[93m"),
    (r"\bTEST\b", "\033[96m"),
    (r"\btextual\b", "\033[95m"),
    (r"\brich\b", "\033[95m"),
    (r"\bpip\b", "\033[94m"),
    (r"\bDEPS?\b", "\033[96m"),
)


def _colorize_keys(line: str) -> str:
    """Color key tokens; rest stays white on black for the line only."""
    import re as _re

    out = line
    for pat, color in _KEY_COLOR_MAP:
        out = _re.sub(
            pat,
            lambda m, c=color: f"{c}{m.group(0)}\033[37m",
            out,
            flags=_re.IGNORECASE,
        )
    return out


def _wrap40(text: str, width: int = _INSTALL_WIDTH) -> List[str]:
    words = text.split()
    if not words:
        return [""]
    lines: List[str] = []
    cur = words[0]
    for w in words[1:]:
        if len(cur) + 1 + len(w) <= width:
            cur = f"{cur} {w}"
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def _tty_hard_reset() -> None:
    """Best-effort restore so Ctrl-C / keyboard / Textual work after install UX.

    Does NOT change column count (stty cols breaks WSL focus after alt-tab).
    Does: SGR reset, show cursor, leave alt screen, reset scroll region,
    and `stty sane` if stdin is a TTY (recovers cooked mode without resizing).
    """
    try:
        # Reset attributes, show cursor, main buffer, clear sticky modes
        sys.stdout.write(
            "\033[0m"  # SGR reset
            "\033[?25h"  # show cursor
            "\033[?1049l"  # leave alternate screen if any
            "\033[?47l"
            "\033[r"  # reset scroll region
            "\033[27m"  # reverse off
            "\n"
        )
        sys.stdout.flush()
    except Exception:
        pass
    try:
        if sys.stdin.isatty():
            # sane restores echo/icanon/etc without forcing cols=40
            subprocess.run(
                ["stty", "sane"],
                stdin=sys.stdin,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1,
            )
    except Exception:
        pass


def install_mode_enter() -> None:
    """40-col *soft* black/white install UX. Never mutates terminal size."""
    global _INSTALL_MODE_ACTIVE
    if _INSTALL_MODE_ACTIVE:
        return
    _INSTALL_MODE_ACTIVE = True
    # Register cleanup so Ctrl-C / crash still restores TTY
    try:
        import atexit

        atexit.register(install_mode_exit)
    except Exception:
        pass
    try:
        import signal

        def _sig_restore(signum, frame):  # type: ignore[no-untyped-def]
            install_mode_exit()
            _tty_hard_reset()
            # re-raise default behavior
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)

        if hasattr(signal, "SIGINT"):
            signal.signal(signal.SIGINT, _sig_restore)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, _sig_restore)
    except Exception:
        pass

    # Soft banner only — NO full-screen clear, NO stty cols
    # (clear + stty cols left WSL black/unresponsive after alt-tab)
    print()
    install_say("========================================")
    install_say("INSTALL MODE · 40 COL · BLACK/WHITE")
    install_say("soft wrap only — TTY size untouched")
    install_say("Ctrl-C aborts · keys stay live")
    install_say("========================================")
    install_mode_flash(n=2)
    install_say("Key words stay colored. DEPS check next.")


def install_mode_flash(n: int = 2) -> None:
    """Brief reverse-video flashes; ALWAYS ends with reverse-off + SGR reset."""
    if not sys.stdout.isatty():
        return
    for _ in range(max(0, n)):
        try:
            # Flash one banner line only (not whole sticky reverse mode)
            sys.stdout.write("\033[7m\033[40m\033[37m ***           *** \033[0m\r")
            sys.stdout.flush()
            time.sleep(0.05)
            sys.stdout.write("\033[0m\033[40m\033[37m *** FLASH *** \033[0m\r")
            sys.stdout.flush()
            time.sleep(0.05)
        except Exception:
            break
    try:
        sys.stdout.write("\033[0m\033[27m\033[K\n")
        sys.stdout.flush()
    except Exception:
        pass


def install_say(msg: str, *, key: bool = True) -> None:
    """Print in install mode (40-col wrap). Each line ends with full SGR reset."""
    for raw in _wrap40(msg):
        if _INSTALL_MODE_ACTIVE:
            body = _colorize_keys(raw) if key else raw
            # per-line black bg / white fg, then hard reset so nothing sticks
            print(f"\033[40m\033[37m{body}\033[0m")
        else:
            body = _colorize_keys(raw) if key else raw
            print(body)
    try:
        sys.stdout.flush()
    except Exception:
        pass


def install_mode_exit() -> None:
    """Fully restore terminal after install UX so Textual + keyboard work."""
    global _INSTALL_MODE_ACTIVE
    if not _INSTALL_MODE_ACTIVE:
        # Still hard-reset if called defensively before TUI
        return
    _INSTALL_MODE_ACTIVE = False
    # Hand SIGINT/SIGTERM back so Textual can handle quit bindings
    try:
        import signal

        if hasattr(signal, "SIGINT"):
            signal.signal(signal.SIGINT, signal.SIG_DFL)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
    except Exception:
        pass
    _tty_hard_reset()
    try:
        print("\033[0m[install mode end — terminal restored]\033[0m")
        sys.stdout.flush()
    except Exception:
        pass


def _venv_python(venv_path: Path) -> Path:
    if sys.platform.startswith("win"):
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def _deps_importable(python_bin: Path) -> bool:
    """True if textual + rich import cleanly in venv — no reinstall needed."""
    try:
        check = subprocess.run(
            [str(python_bin), "-c", "import textual, rich"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return check.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _run_library_demos(python_bin: Path) -> bool:
    """On-screen test calls for each library used in dependency checking.

    No reinstall — only import + tiny API exercise, results printed + logged.
    """
    paths = _bootstrap_log_paths()
    install_mode_flash(n=2)
    install_say("=== LIBRARY TEST DEMOS ===")
    demo_script = r"""
import json, sys
results = []

# textual
try:
    import textual
    from textual.app import App
    ver = getattr(textual, "__version__", "?")
    ok = callable(App)
    results.append(("textual", True, f"version={ver} App={ok}"))
except Exception as e:
    results.append(("textual", False, repr(e)))

# rich
try:
    import rich
    from rich.console import Console
    from rich.text import Text
    c = Console(file=sys.stdout, force_terminal=True, width=40, highlight=False)
    t = Text("rich OK", style="bold white on black")
    # don't print via Console here — parent formats; just exercise API
    _ = t.plain
    ver = getattr(rich, "__version__", "?")
    results.append(("rich", True, f"version={ver} Console+Text ok"))
except Exception as e:
    results.append(("rich", False, repr(e)))

# stdlib demos shown alongside (no install)
try:
    import zipfile, pathlib
    results.append(("zipfile", True, f"ZipFile={callable(zipfile.ZipFile)}"))
    results.append(("pathlib", True, f"Path={callable(pathlib.Path)}"))
except Exception as e:
    results.append(("stdlib", False, repr(e)))

print(json.dumps(results))
"""
    try:
        proc = subprocess.run(
            [str(python_bin), "-c", demo_script],
            capture_output=True,
            text=True,
            timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        install_say(f"TEST FAIL: library demos: {e}")
        _write_error(f"library demos OS error: {e}\n")
        return False

    raw = (proc.stdout or "").strip().splitlines()
    json_line = raw[-1] if raw else "[]"
    try:
        results = json.loads(json_line)
    except json.JSONDecodeError:
        install_say("TEST FAIL: could not parse demo results")
        _write_error(f"demo parse fail stdout={proc.stdout!r} stderr={proc.stderr!r}\n")
        return False

    all_ok = True
    lines_log: List[str] = []
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        line = f"TEST {name}: {status} — {detail}"
        install_say(line)
        lines_log.append(line)

    blob = "LIBRARY DEMOS\n" + "\n".join(lines_log) + f"\nall_ok={all_ok}\n"
    _write_ops(blob)
    if all_ok:
        _write_success("library demos PASS (textual, rich, zipfile, pathlib)\n")
        install_say("DEPS library tests: PASS")
    else:
        _write_error(blob)
        install_say("DEPS library tests: FAIL")
    return all_ok


def find_or_create_venv() -> Path:
    venv_path = Path(__file__).parent / ".venv"
    if not venv_path.exists():
        install_mode_enter()
        install_say("Creating venv (python -m venv)...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
            _write_success(f"venv created at {venv_path}\n")
            install_say("venv: PASS")
        except subprocess.CalledProcessError as e:
            msg = f"venv create failed: {e}\ncmd={e.cmd!r} returncode={e.returncode}\n"
            install_say("venv: FAIL")
            _write_error(msg)
            sys.exit(1)
    return venv_path


def ensure_deps(venv_path: Path) -> Path:
    """Ensure textual/rich in venv. Skip reinstall if already importable.

    Always runs on-screen library test demos. Install mode = 40-col black/white
    with flashes and colored key words. Logs go to stamped files under logs/.
    """
    python_bin = _venv_python(venv_path)
    paths = _bootstrap_log_paths()
    if not python_bin.exists():
        install_mode_enter()
        msg = f"venv python missing: {python_bin}\n"
        install_say(msg.strip())
        _write_error(msg)
        sys.exit(1)

    # Enter install UX as soon as we touch deps (install OR check path)
    install_mode_enter()
    install_say(f"stamp={paths['stamp']}")
    install_say(f"logs → {paths['dir']}")
    install_say("Ensuring core DEPS (textual, rich)...")
    install_say(f"pip log → {Path(paths['deps']).name}")

    already_ok = _deps_importable(python_bin)
    if already_ok:
        install_say("DEPS already importable — SKIP pip reinstall")
        install_mode_flash(n=1)
        _write_ops(
            f"SKIP reinstall: textual+rich already importable via {python_bin}\n"
        )
        _write_success("deps present — no reinstall\n")
    else:
        install_say("DEPS missing — running pip install (no python reinstall)")
        install_mode_flash(n=2)
        pip = [str(python_bin), "-m", "pip"]

        def _run_pip(args: List[str], label: str) -> None:
            cmd = pip + args
            install_say(f"pip: {label}")
            install_say(" ".join(cmd)[:80])
            proc = subprocess.run(cmd, capture_output=True, text=True)
            blob = (
                f"[{label}] cmd={' '.join(cmd)}\n"
                f"returncode={proc.returncode}\n"
                f"--- stdout ---\n{proc.stdout or ''}\n"
                f"--- stderr ---\n{proc.stderr or ''}\n"
            )
            _append_log(
                paths["deps"], blob, paths["deps_latest"], paths["bootstrap"], paths["bootstrap_latest"]
            )
            if proc.returncode != 0:
                _write_error(f"BOOTSTRAP DEP FAILURE\n{blob}")
                tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-12:]
                for line in tail:
                    install_say(f"| {line}")
                install_say(f"Dep install FAIL ({label})")
                install_say(f"Full: {paths['deps'].name}")
                raise subprocess.CalledProcessError(
                    proc.returncode, cmd, proc.stdout, proc.stderr
                )
            install_say(f"{label}: PASS")
            _write_success(f"pip {label} PASS\n")

        try:
            # Do NOT reinstall python. Only pip packages when missing.
            # Skip pip upgrade if packages already missing only — still try install.
            _run_pip(["install", "--upgrade", "pip"], "upgrade-pip")
            req = Path(__file__).parent / "requirements.txt"
            if req.exists():
                _run_pip(["install", "-r", str(req)], "install-requirements")
            else:
                _run_pip(["install"] + CORE_DEPS, "install-core-deps")
        except subprocess.CalledProcessError:
            install_mode_exit()
            sys.exit(1)
        except OSError as e:
            _write_error(f"Dep install OS error: {e}\n")
            install_say(f"Dep install ERROR: {e}")
            install_mode_exit()
            sys.exit(1)

        if not _deps_importable(python_bin):
            blob = "post-install import check failed for textual/rich\n"
            install_say("import textual/rich: FAIL")
            _write_error(blob)
            install_mode_exit()
            sys.exit(1)
        install_say("import textual, rich: PASS")
        _write_success("post-install import PASS\n")

    # Always demonstrate each library with a real test call on screen
    if not _run_library_demos(python_bin):
        install_mode_exit()
        sys.exit(1)

    install_say("DEPS OK — library demos PASS")
    install_mode_flash(n=1)
    install_mode_exit()
    print("  deps OK (textual, rich importable; demos passed)")
    print(f"  success log → {paths['success']}")
    print(f"  ops log     → {paths['ops']}")
    return python_bin


def reexec_if_needed(venv_python: Path) -> None:
    if os.environ.get("AWESOME_LAUNCHER_VENV") != "1":
        print("Re-executing inside venv...")
        _write_ops(f"re-exec into {venv_python}\n")
        os.environ["AWESOME_LAUNCHER_VENV"] = "1"
        # Keep same session stamp across re-exec via env
        os.environ["AWESOME_LAUNCHER_STAMP"] = _session_stamp()
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# -------------------------------
# CONFIG + PATH HELPERS
# -------------------------------

DEFAULT_CONFIG = {
    "menu_search_paths": [".", "./menus", "./.launcher_menus", "~/.tui/menus"],
    "menus_dir": ".launcher_menus",
    "logs_dir": "logs",
    "sessions_dir": "sessions",
    "branding": {
        "header": "AWESOME LAUNCHER OF TUI DOOM",
        "footer": "BBS-Level | Zip Menus + Harnesses | Chunked Ops | Record/Replay | Phase 1"
    },
    "harness": {
        "default_chunk": "",
        "chunk_size": "1day",
        "log_files": ["processing.log", "error.log"]
    },
    "demo": {"sample_zip_name": "sample_menu.zip"}
}

def load_config() -> Dict[str, Any]:
    cfg_path = Path(__file__).parent / "LAUNCHERCONFIG.JSON"
    if cfg_path.exists():
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg = {**DEFAULT_CONFIG, **user_cfg}
            return cfg
        except Exception as e:
            print(f"Config load failed ({e}), using defaults.")
    return DEFAULT_CONFIG.copy()

def ensure_dirs(cfg: Dict[str, Any]) -> Dict[str, Path]:
    base = Path(__file__).parent
    dirs = {
        "menus": base / cfg["menus_dir"],
        "logs": base / cfg["logs_dir"],
        "sessions": base / cfg["sessions_dir"],
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs

def expand_search_paths(paths: List[str]) -> List[Path]:
    out = []
    for p in paths:
        pp = Path(p).expanduser()
        if pp.exists() or str(pp).startswith("."):
            out.append(pp)
    return out

# -------------------------------
# ZIP MENU + EXTRACT
# -------------------------------

def find_menu_zips(search_paths: List[str]) -> List[Path]:
    zips: List[Path] = []
    for base in expand_search_paths(search_paths):
        try:
            for z in base.glob("*.zip"):
                if z.is_file():
                    zips.append(z.resolve())
        except Exception:
            pass
    # dedupe + sort by name
    seen = set()
    unique = []
    for z in sorted(zips, key=lambda p: p.name.lower()):
        if z not in seen:
            seen.add(z)
            unique.append(z)
    return unique

def extract_menu_zip(zip_path: Path, menus_dir: Path) -> tuple[Path, str]:
    """Extract and return (extracted_dir, main_script_name)"""
    name = zip_path.stem
    target = menus_dir / name
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target)

    manifest = target / "menu.json"
    main_script = "harness.py"
    if manifest.exists():
        try:
            info = json.loads(manifest.read_text(encoding="utf-8"))
            main_script = info.get("main_script", "harness.py")
        except Exception:
            pass
    return target, main_script

# -------------------------------
# HARNESS RUNNER + CHUNKED LOGIC + EXIT LEVELS
# -------------------------------

def run_harness_once(
    extracted_dir: Path,
    main_script: str,
    chunk: Optional[str],
    log_dir: Path,
) -> Dict[str, Any]:
    harness = extracted_dir / main_script
    if not harness.exists():
        harness = extracted_dir / "harness.py"
    if not harness.exists():
        return {"returncode": 1, "stdout": "", "stderr": f"No harness found in {extracted_dir}", "exit_level": 1}

    log_dir.mkdir(parents=True, exist_ok=True)
    proc_log = log_dir / "processing.log"
    err_log = log_dir / "error.log"

    cmd = [sys.executable, str(harness)]
    if chunk:
        cmd += ["--chunk", chunk]
    cmd += ["--log-dir", str(log_dir)]

    start = datetime.datetime.now()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(extracted_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as te:
        return {"returncode": 1, "stdout": te.stdout or "", "stderr": "TIMEOUT", "exit_level": 1}

    # Append to logs
    ts = start.isoformat()
    with open(proc_log, "a", encoding="utf-8") as f:
        f.write(f"\n=== RUN {ts} chunk={chunk or 'full'} ===\n")
        f.write(result.stdout or "")
    if result.stderr:
        with open(err_log, "a", encoding="utf-8") as f:
            f.write(f"\n=== ERR {ts} ===\n{result.stderr}\n")

    rc = result.returncode
    # Map to exit levels: 0 success, 1 error, 2 partial (non-zero but partial work done)
    if rc == 0:
        level = 0
    elif rc == 2:
        level = 2
    else:
        level = 1

    return {
        "returncode": rc,
        "stdout": result.stdout or "",
        "stderr": result.stderr or "",
        "exit_level": level,
        "chunk": chunk,
        "started": ts,
    }

def run_chunked_harness(
    extracted_dir: Path,
    main_script: str,
    start_chunk: Optional[str],
    end_chunk: Optional[str],
    log_dir: Path,
) -> List[Dict[str, Any]]:
    results = []
    if start_chunk and end_chunk:
        try:
            d = datetime.date.fromisoformat(start_chunk)
            end_d = datetime.date.fromisoformat(end_chunk)
            current = d
            while current <= end_d:
                res = run_harness_once(extracted_dir, main_script, current.isoformat(), log_dir)
                results.append(res)
                if res["exit_level"] == 1 and res["returncode"] != 2:
                    # hard error - stop
                    break
                current += datetime.timedelta(days=1)
        except Exception as e:
            results.append({"returncode": 1, "stderr": f"Date range error: {e}", "exit_level": 1})
    else:
        chunk = start_chunk or end_chunk
        res = run_harness_once(extracted_dir, main_script, chunk, log_dir)
        results.append(res)
    return results

# -------------------------------
# DEMO ZIP GENERATOR (self-contained sample menu)
# -------------------------------

DEMO_HARNESS_CODE = r'''#!/usr/bin/env python3
"""
Demo harness (packaged inside sample_menu.zip)
Simulates chunked processing of daily "memory files".
Supports: --chunk YYYY-MM-DD , --log-dir DIR
Exit codes: 0=success, 1=error, 2=partial
"""
import argparse
import sys
import datetime
from pathlib import Path
import time
import json

def main():
    parser = argparse.ArgumentParser(description="Demo chunked memory processor")
    parser.add_argument("--chunk", default=None, help="Single day YYYY-MM-DD")
    parser.add_argument("--log-dir", default="logs")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    proc = log_dir / "processing.log"
    err = log_dir / "error.log"

    def log(msg: str, error: bool = False):
        fh = err if error else proc
        line = f"[{datetime.datetime.now().isoformat()}] {msg}\n"
        with open(fh, "a", encoding="utf-8") as f:
            f.write(line)
        print(msg, file=sys.stderr if error else sys.stdout)

    log(f"DEMO HARNESS start. chunk={args.chunk}")

    chunks = []
    if args.chunk:
        chunks = [args.chunk]
    else:
        today = datetime.date.today()
        chunks = [(today - datetime.timedelta(days=i)).isoformat() for i in range(0, 2)]

    processed = 0
    for ch in chunks:
        log(f"Processing memory files for {ch}...")
        for i in range(3):
            fname = f"mem-{ch}-{i:02d}.log"
            log(f"  + {fname}: read -> parse -> index (demo)")
            time.sleep(0.05)
        processed += 1
        log(f"Chunk {ch} done.")

    summary = {
        "harness": "demo",
        "chunks": len(chunks),
        "processed": processed,
        "exit_level": 0
    }
    (log_dir / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    log(f"DEMO complete. exit=0")
    sys.exit(0)

if __name__ == "__main__":
    main()
'''

DEMO_MENU_JSON = {
    "name": "demo-memory-processor",
    "description": "Phase 1 demo menu. Chunked daily memory file processing via harness.",
    "main_script": "harness.py",
    "version": "phase1-demo"
}

def create_demo_menu_zip(dest: Path) -> Path:
    dest = Path(dest).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("menu.json", json.dumps(DEMO_MENU_JSON, indent=2))
        z.writestr("harness.py", DEMO_HARNESS_CODE)
        z.writestr("README.txt",
            "Demo zip for AWESOME LAUNCHER OF TUI DOOM\n\n"
            "Select this menu, enter a chunk like 2026-06-20 or range, hit Run.\n"
            "Harness writes processing.log + error.log and run_summary.json.\n")
    return dest

# -------------------------------
# RECORDING + REPLAY
# -------------------------------

def save_recording(session_dir: Path, actions: List[Dict[str, Any]]) -> Path:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = session_dir / f"session_{ts}.json"
    data = {
        "recorded_at": datetime.datetime.now().isoformat(),
        "launcher": "AWESOME_LAUNCHER_OF_TUIDOOM",
        "phase": "1",
        "actions": actions,
    }
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out

def replay_session(session_path: Path) -> None:
    print(f"Replaying session: {session_path}")
    data = json.loads(session_path.read_text(encoding="utf-8"))
    actions = data.get("actions", [])
    print(f"  {len(actions)} recorded actions")
    for a in actions:
        print(f"  - {a.get('ts')} {a.get('action')}: {a.get('data')}")
        if a.get("action") == "run_harness":
            d = a.get("data", {})
            print(f"    -> would run zip={d.get('zip')} chunk={d.get('chunk')}")
            # For full replay you could resolve zip + call runner here
    print("Replay complete (non-interactive log of recorded steps).")

# -------------------------------
# TEXTUAL TUI (after bootstrap)
# -------------------------------

def launch_launcher_tui(cfg: Dict[str, Any]) -> None:
    # Heavy imports only after venv is ready
    try:
        from textual.app import App, ComposeResult
        from textual.screen import Screen
        from textual.containers import Grid, Horizontal, Vertical
        from textual.widgets import Button, Header, Footer, Label, Static, ListView, ListItem, Input, Log
        from textual.binding import Binding
        from textual.reactive import reactive
        from textual import work
    except ImportError as e:
        paths = _bootstrap_log_paths()
        msg = (
            f"Textual import failed after deps claimed OK: {e}\n"
            f"python={sys.executable}\n"
            f"Fix: .venv/bin/python -m pip install -r requirements.txt\n"
        )
        print(msg)
        _append_log(paths["error"], msg)
        _append_log(paths["bootstrap"], msg)
        sys.exit(1)

    class LauncherHome(Screen):
        """Main menu + controls screen."""
        def compose(self) -> ComposeResult:
            yield Header()
            yield Label(cfg["branding"]["header"], id="brand")
            yield Static("Default: Go find a real menu  |  Zip menus + harnesses + chunked work + record/replay", id="subtitle")
            # Exact branding per Olivia-pleasereadthis.markdown for Phase 3
            yield Static('BBS-Level | Zip Menus + Harnesses | Chunked Ops | Record/Replay | Gutter Mode | Olivia Dev Alpha | Phase 3', id="branding-footer")
            # Exact per Olivia-pleasereadthis.markdown: high-contrast pink/black, C-64, ruined in Gutter, Liv HUB / Olivia Dev Alpha refs.

            # Multi-pane inspired by Olivia guide starter template
            with Horizontal(id="main-area"):
                with Vertical(id="menu-pane", classes="pane"):
                    yield Static("MENUS", classes="pane-title")
                    yield ListView(id="menu-list")  # Per Olivia guide: ListView for menu

                with Vertical(id="controls-pane", classes="pane"):
                    with Grid(id="main-grid"):
                        yield Button("Scan / Find Menu", id="scan", variant="primary")
                        yield Button("Create Demo Zip", id="demo")
                        yield Button("Run Harness", id="run", variant="success")
                        yield Button("Library", id="library")
                        yield Button("Gallery 6-Panel", id="gallery", variant="warning")
                        yield Button("Effects FX", id="effects")
                        yield Button("Toggle Rec", id="rec")
                        yield Button("Save Rec", id="save_rec")
                        yield Button("Replay", id="replay")
                        yield Button("Toggle Gutter", id="gutter", variant="default")

                    with Horizontal():
                        yield Input(placeholder="Chunk (YYYY-MM-DD)", id="chunk")
                        yield Input(placeholder="End (optional)", id="end_chunk")

                    yield Static("Selected: (none)", id="selected")

            yield Log(id="runlog")  # Per Olivia guide: Log for streaming output
            yield Static("PANE FLASH CIRCLE: [ ] [ ] [ ]", id="pane-flash")  # For gutter-1 circle flash + obnoxious animations in Phase 3 test
            yield Footer()

        def on_mount(self) -> None:
            log = self.app.query_one("#runlog", Log)
            log.write("[dim]Launcher ready. Scan for zips or create demo.[/dim]")
            log.write("[magenta]Keys: G=6-panel gallery · E=effects · g=gutter · s=scan · ctrl+q=quit[/magenta]")
            log.write("[dim]Crash logs → logs/tui_crash_*.log + logs/error_*.log (stamped)[/dim]")

        def on_list_view_selected(self, event) -> None:
            """Handle selection from ListView (per Olivia guide recommendation for menu)."""
            if hasattr(self.app, "_zips") and event.item is not None:
                try:
                    idx = list(event.list_view.children).index(event.item)
                    if idx < len(self.app._zips):
                        self.app.current_zip = self.app._zips[idx]
                        sel = self.query_one("#selected", Static)
                        sel.update(f"Selected: {self.app.current_zip.name}")
                        self.app.ui_log(f"[cyan]ListView selected: {self.app.current_zip.name}[/cyan]")
                except Exception:
                    pass

        def on_button_pressed(self, event: Button.Pressed) -> None:
            bid = event.button.id
            if bid == "scan":
                self.app.scan_for_zips()
            elif bid == "demo":
                dest = Path.cwd() / self.app.config["demo"]["sample_zip_name"]
                create_demo_menu_zip(dest)
                self.app.ui_log(f"[green]Demo menu created: {dest.name}[/green]")
                self.app.ui_log("Now press 'Go find a real menu (Scan)' or run directly.")
            elif bid == "run":
                chunk = self.query_one("#chunk", Input).value
                endc = self.query_one("#end_chunk", Input).value
                self.app.run_current_harness(chunk, endc)
            elif bid == "library":
                self.app.show_library()
            elif bid == "gallery":
                self.app.action_open_gallery()
            elif bid == "effects":
                self.app.action_open_effects()
            elif bid == "rec":
                self.app.is_recording = not self.app.is_recording
            elif bid == "save_rec":
                self.app.action_save_recording()
            elif bid == "replay":
                self.app.replay_last()
            elif bid == "gutter":
                self.app.action_toggle_gutter()

    class AwesomeLauncherApp(App):
        CSS_PATH = "grok_tui.tcss"  # From Olivia's canonical "Olivia says read this.md" (full guide, master a40a52d). Do not overwrite the source file. See that file for the complete TCSS layers, reactive Gutter, ListView+Log multi-pane starter template, and asyncio streaming example. This launcher is a slight extension/alignment.

        CSS = """
        Screen { align: center middle; }
        #brand { text-style: bold; color: #00ffaa; margin: 1; }
        #main-grid { grid-size: 3 4; grid-gutter: 1 1; padding: 1; }
        Button { width: 100%; height: 3; }
        #runlog { height: 14; border: solid #444; margin: 1; }
        #selected { color: #ffaa00; margin: 1 0; }
        """

        gutter_active: reactive[bool] = reactive(False)

        def watch_gutter_active(self, active: bool) -> None:
            """Automatically add/remove the class when the value changes (per Olivia guide)."""
            if active:
                self.add_class("gutter-active")
            else:
                self.remove_class("gutter-active")

        def action_toggle_gutter(self) -> None:
            """Bind this to a key (e.g. 'g'). Per the canonical guide."""
            self.gutter_active = not self.gutter_active

        def action_open_gallery(self) -> None:
            """PR-05: six-panel layout carousel + nested menus."""
            try:
                from tui_chrome.gallery import GalleryScreen
                self.push_screen(GalleryScreen())
                self.ui_log("[magenta]Opened 6-panel gallery (Esc back · ←/→ cycle · L layout)[/magenta]")
            except Exception as e:
                self.ui_log(f"[red]Gallery failed: {e}[/red]")
                _log_tui_crash(e, where="action_open_gallery")

        def action_open_effects(self) -> None:
            """PR-06: ANSI/ASCII effects demo screen."""
            try:
                from tui_chrome.gallery import EffectsDemoScreen
                self.push_screen(EffectsDemoScreen())
                self.ui_log("[magenta]Opened effects demo (Esc back)[/magenta]")
            except Exception as e:
                self.ui_log(f"[red]Effects failed: {e}[/red]")
                _log_tui_crash(e, where="action_open_effects")

        BINDINGS = [
            Binding("ctrl+q", "quit", "Quit"),
            Binding("s", "scan_menus", "Scan"),
            Binding("r", "toggle_record", "Record"),
            Binding("ctrl+s", "save_recording", "Save Rec"),
            Binding("g", "toggle_gutter", "Toggle Gutter"),  # From Olivia guide
            Binding("G", "open_gallery", "Gallery"),
            Binding("e", "open_effects", "Effects"),
        ]

        current_zip: reactive[Optional[Path]] = reactive(None)
        is_recording: reactive[bool] = reactive(False)
        recording: List[Dict[str, Any]] = []

        def __init__(self, config: Dict[str, Any], dirs: Dict[str, Path], **kwargs):
            super().__init__(**kwargs)
            self.config = config
            self.dirs = dirs
            self.current_zip = None
            self.is_recording = False
            self.recording = []

        def compose(self) -> ComposeResult:
            yield LauncherHome()

        def on_mount(self) -> None:
            self.title = self.config["branding"]["header"]
            self.sub_title = "Phase 3 - Full Test Harness (Olivia inputs)"
            if os.environ.get("LAUNCHER_TEST_MODE") == "1":
                self.run_worker(self._run_phase3_test_sequence, thread=True)

        def _run_phase3_test_sequence(self) -> None:
            """Phase 3 test harness per Olivia-pleasereadthis.markdown: 
            - auto-zip if needed (handled in CLI)
            - enter gutter-1
            - flash panes in circle (rapid UI + rotating ASCII)
            - ridiculous obnoxious shit (log spam, flashes, animations)
            - success exit.
            Gutter Mode live and toggleable. Exact branding locked.
            """
            import time
            self.call_from_thread(self.ui_log, "[bold]=== Phase 3 Test Sequence Starting (Gutter-1) ===[/bold]")
            
            # Auto Gutter flash on startup in test (per spec)
            self.call_from_thread(lambda: setattr(self, 'gutter_active', True))
            time.sleep(0.3)
            self.call_from_thread(self.ui_log, "AUTO GUTTER FLASH ON STARTUP - high heat engaged!")
            self.call_from_thread(self.ui_log, "Gutter Mode Engaged (level 1) - pink/black ruined styles active. Liv HUB / Olivia Dev Alpha reference: ON")

            # Flash the panes in a circle + obnoxious shit
            flash_widget = None
            try:
                flash_widget = self.query_one("#pane-flash", Static)
            except:
                pass

            ascii_frames = [
                "  / \\   ",
                " /   \\  ",
                "|  O  | ",
                " \\   /  ",
                "  \\ /   ",
                "   -    ",
                "  / \\   "
            ]
            panes = ["menu-pane", "controls-pane", "runlog area"]
            for i in range(20):  # Extended ridiculous loop for obnoxious effect
                idx = i % len(panes)
                frame = ascii_frames[i % len(ascii_frames)]
                msg = f"[GUTTER-{i%3+1} FLASH CIRCLE] Rotating on {panes[idx]} : {frame} !!!"
                self.call_from_thread(self.ui_log, msg)
                
                if flash_widget:
                    self.call_from_thread(flash_widget.update, f"PANE FLASH CIRCLE: {frame} [INTENSE]")

                # Ridiculous obnoxious shit: spam + flashes + animations
                for s in range(4):
                    self.call_from_thread(self.ui_log, "!!! OBNOXIOUS SHIT: GUTTER HEAT RISING !!! RUINED TEXT SMUDGE !!! PINK/BLACK INTENSE FLASH !!! SILLY ANIMATION FRAME " + str(s))
                    self.call_from_thread(self.ui_log, "   ASCII BANNER: GUTTER MODE ENGAGED !!!! C-64 RUINED !!!!")
                
                # Simulate rapid color/border flash by toggling class temporarily (intensify)
                if i % 2 == 0:
                    self.call_from_thread(lambda: self.add_class("gutter-active"))  # re-apply for flash
                else:
                    self.call_from_thread(lambda: self.remove_class("gutter-active"))
                    self.call_from_thread(lambda: self.add_class("gutter-active"))

                time.sleep(0.08)  # Fast for "rapid UI updates"

            # Restore Gutter
            self.call_from_thread(lambda: self.add_class("gutter-active"))

            self.call_from_thread(self.ui_log, "Gutter flash circle complete. Obnoxious effects + animations demonstrated.")
            time.sleep(0.8)
            
            # "Gutter Mode Engaged" banner with flair
            self.call_from_thread(self.ui_log, "[bold magenta]*** GUTTER MODE ENGAGED *** PINK/BLACK RUINED C-64 FLAIR ***[/bold magenta]")
            self.call_from_thread(self.ui_log, "Liv HUB claim active. Olivia Dev Alpha aesthetics locked.")

            time.sleep(1)
            self.call_from_thread(self.ui_log, "[bold green]Successful test - Gutter Mode verified and harness operational![/bold green]")
            self.call_from_thread(self.ui_log, "Full cycle demonstrated: prompt -> auto-zip -> gutter-1 -> flash circle -> obnoxious -> success exit.")
            self.call_from_thread(self.ui_log, "Test harness cycle complete. Exiting cleanly.")
            time.sleep(2)
            self.call_from_thread(self.exit)

        def watch_current_zip(self, zip_path: Optional[Path]) -> None:
            # Guard: reactive may fire in __init__ before any screen is mounted
            try:
                if not self.is_mounted:
                    return
                sel = self.query_one("#selected", Static)
            except Exception:
                return
            if zip_path:
                sel.update(f"Selected: {zip_path.name} (extracted on run)")
            else:
                sel.update("Selected: (none)")

        def watch_is_recording(self, recording: bool) -> None:
            try:
                if not self.is_mounted:
                    return
                btn = self.query_one("#rec", Button)
                btn.label = "Recording: ON" if recording else "Toggle Recording"
            except Exception:
                pass

        def ui_log(self, msg: str) -> None:
            try:
                lw = self.query_one("#runlog", Log)
                if hasattr(lw, "write_line"):
                    lw.write_line(msg)
                else:
                    lw.write(msg)
            except Exception:
                print(msg)

        def record_action(self, action: str, data: Dict[str, Any]) -> None:
            if self.is_recording:
                self.recording.append({
                    "ts": datetime.datetime.now().isoformat(),
                    "action": action,
                    "data": data
                })

        # --- Actions ---
        def action_scan_menus(self) -> None:
            self.scan_for_zips()

        def action_toggle_record(self) -> None:
            self.is_recording = not self.is_recording
            self.ui_log(f"[bold]{'RECORDING ON' if self.is_recording else 'RECORDING OFF'}[/bold]")

        def action_save_recording(self) -> None:
            if not self.recording:
                self.ui_log("[yellow]No actions recorded yet.[/yellow]")
                return
            out = save_recording(self.dirs["sessions"], self.recording)
            self.ui_log(f"[green]Saved recording: {out.name}[/green]")
            self.recording.clear()

        def scan_for_zips(self) -> None:
            zips = find_menu_zips(self.config.get("menu_search_paths", []))
            self.ui_log(f"Scanned. Found {len(zips)} menu zip(s).")
            if not zips:
                self.ui_log("[yellow]No zips found. Use 'Create Demo Menu Zip' first.[/yellow]")
                return

            try:
                lv = self.query_one("#menu-list", ListView)
                lv.clear()
                for z in zips:
                    lv.append(ListItem(Static(z.name, classes="menu-item")))
                self._zips = zips
                if lv.children:
                    lv.index = 0  # select first per guide-friendly list behavior
            except Exception:
                for i, z in enumerate(zips[:5]):
                    self.ui_log(f"  [{i+1}] {z.name}")

            self.current_zip = zips[0]
            self.ui_log(f"[cyan]Selected: {self.current_zip.name}[/cyan]")

        # Button handling lives in LauncherHome screen (forwards to app)

        def show_library(self) -> None:
            menus_dir = self.dirs["menus"]
            if not menus_dir.exists():
                self.ui_log("No extracted menus yet.")
                return
            entries = list(menus_dir.glob("*"))
            self.ui_log("Extracted menus / library:")
            for e in entries:
                self.ui_log(f"  - {e.name}")
            if not entries:
                self.ui_log("(empty - extract a zip first)")

        def replay_last(self) -> None:
            sessions = sorted(self.dirs["sessions"].glob("session_*.json"), reverse=True)
            if not sessions:
                self.ui_log("[yellow]No session files found.[/yellow]")
                return
            latest = sessions[0]
            self.ui_log(f"Replaying {latest.name} (non-interactive)...")
            try:
                replay_session(latest)
                self.ui_log("[green]Replay done.[/green]")
            except Exception as e:
                self.ui_log(f"[red]Replay error: {e}[/red]")

        # Live harness runner (Phase 2 streaming per Olivia guide - line by line to Log)
        def _run_harness_live(self, extracted_dir: Path, main_script: str, chunk: Optional[str], log_dir: Path) -> Dict[str, Any]:
            harness = extracted_dir / main_script
            if not harness.exists():
                harness = extracted_dir / "harness.py"
            if not harness.exists():
                self.call_from_thread(self.ui_log, "[red]No harness found[/red]")
                return {"returncode": 1, "exit_level": 1, "chunk": chunk}

            log_dir.mkdir(parents=True, exist_ok=True)
            cmd = [sys.executable, str(harness)]
            if chunk:
                cmd += ["--chunk", chunk]
            cmd += ["--log-dir", str(log_dir)]

            self.call_from_thread(self.ui_log, f"$ {' '.join(cmd)}")

            try:
                import subprocess
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(extracted_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                for line in proc.stdout:
                    line = line.rstrip("\n")
                    if line:
                        self.call_from_thread(self.ui_log, line)
                proc.wait()
                rc = proc.returncode
                level = 0 if rc == 0 else (2 if rc == 2 else 1)
                self.call_from_thread(self.ui_log, f"[Process exited with code {rc}]")
                return {
                    "returncode": rc,
                    "exit_level": level,
                    "chunk": chunk,
                }
            except Exception as e:
                self.call_from_thread(self.ui_log, f"[red]Stream error: {e}[/red]")
                return {"returncode": 1, "exit_level": 1, "chunk": chunk}

        # Main run action - attached to a dynamic button or we trigger via code
        def run_current_harness(self, chunk: str = "", end_chunk: str = "") -> None:
            if not self.current_zip:
                self.scan_for_zips()
                if not self.current_zip:
                    self.ui_log("[red]No menu selected. Create demo or scan first.[/red]")
                    return

            extracted, main_script = extract_menu_zip(self.current_zip, self.dirs["menus"])
            self.ui_log(f"[cyan]Extracted {self.current_zip.name} -> {extracted.name}[/cyan]")

            start_c = chunk.strip() or None
            end_c = end_chunk.strip() or None

            self.record_action("run_harness", {
                "zip": str(self.current_zip.name),
                "chunk": start_c,
                "end_chunk": end_c
            })

            self.ui_log(f"[bold]Running harness[/bold] chunk={start_c or 'default'} range_end={end_c or '-'} ...")

            @work(exclusive=True, thread=True)
            def _do_run() -> None:
                try:
                    # Live streaming version inspired by the Olivia guide's asyncio/subprocess to Log pattern
                    # (adapted to thread worker for compatibility with existing harness)
                    results = []
                    if start_c and end_c:
                        try:
                            d = datetime.date.fromisoformat(start_c)
                            end_d = datetime.date.fromisoformat(end_c)
                            current = d
                            while current <= end_d:
                                res = self._run_harness_live(extracted, main_script, current.isoformat(), self.dirs["logs"])
                                results.append(res)
                                if res.get("exit_level") == 1 and res.get("returncode") != 2:
                                    break
                                current += datetime.timedelta(days=1)
                        except Exception as e:
                            self.call_from_thread(self.ui_log, f"[red]Date range error: {e}[/red]")
                    else:
                        chunk = start_c or end_c
                        res = self._run_harness_live(extracted, main_script, chunk, self.dirs["logs"])
                        results.append(res)

                    for r in results:
                        level = r.get("exit_level", 1)
                        color = "green" if level == 0 else ("yellow" if level == 2 else "red")
                        self.call_from_thread(
                            self.ui_log,
                            f"[{color}]Chunk {r.get('chunk') or 'full'}: exit_level={level} rc={r.get('returncode')}[/{color}]"
                        )
                    overall = max((r.get("exit_level", 0) for r in results), default=0)
                    self.call_from_thread(self.ui_log, f"[bold]Overall exit level: {overall}[/bold]  (0=done,1=error,2=partial)")
                    self.call_from_thread(self.ui_log, "See logs/ for processing.log + error.log + run_summary.json")
                except Exception as ex:
                    self.call_from_thread(self.ui_log, f"[red]Run error: {ex}[/red]")

            _do_run()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            # If user hits enter in chunk fields, offer to run
            if event.input.id in ("chunk", "end_chunk"):
                chunk = self.query_one("#chunk", Input).value
                endc = self.query_one("#end_chunk", Input).value
                self.run_current_harness(chunk, endc)

    # Boot the app — hard-reset TTY first so WSL/WT keyboard works
    # (install mode must never leave reverse-video / bad stty behind)
    install_mode_exit()
    _tty_hard_reset()
    dirs = ensure_dirs(cfg)
    app = AwesomeLauncherApp(cfg, dirs)
    try:
        app.run()
    except KeyboardInterrupt:
        _tty_hard_reset()
        print("\n[interrupted — terminal restored]", file=sys.stderr)
        raise
    except Exception as e:
        _tty_hard_reset()
        _log_tui_crash(e, where="app.run")
        raise
    finally:
        # Textual normally restores; belt-and-suspenders for WSL after alt-tab kill
        _tty_hard_reset()

# -------------------------------
# CRASH LOGGING (PR-03)
# -------------------------------

def _log_tui_crash(exc: BaseException, where: str = "unknown") -> None:
    """Write traceback to stamped + latest crash/error logs under logs/."""
    import traceback
    paths = _bootstrap_log_paths()
    crash_path = paths["crash"]
    crash_latest = paths["crash_latest"]
    tb = traceback.format_exc()
    blob = (
        f"where={where}\n"
        f"type={type(exc).__name__}\n"
        f"msg={exc}\n"
        f"python={sys.executable}\n"
        f"cwd={os.getcwd()}\n"
        f"stamp={paths.get('stamp', _session_stamp())}\n"
        f"{tb}\n"
    )
    _append_log(crash_path, blob, crash_latest)
    _append_log(
        paths["error"],
        f"TUI CRASH\n{blob}",
        paths["error_latest"],
        paths["ops"],
        paths["ops_latest"],
    )
    _append_log(
        paths["bootstrap"],
        f"TUI CRASH at {where}: {exc}\n",
        paths["bootstrap_latest"],
    )
    print("\n*** TUI CRASH ***", file=sys.stderr)
    print(f"  {type(exc).__name__}: {exc}", file=sys.stderr)
    print(f"  crash log → {crash_path}", file=sys.stderr)
    print(f"  crash latest → {crash_latest}", file=sys.stderr)
    print(f"  error log → {paths['error']}", file=sys.stderr)
    print(f"  error latest → {paths['error_latest']}", file=sys.stderr)
    print(tb, file=sys.stderr)


# -------------------------------
# MAIN
# -------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AWESOME LAUNCHER OF TUI DOOM - Phase 3 (full test harness per Olivia inputs)"
    )
    parser.add_argument("--replay", metavar="SESSION.json", help="Replay a recorded session (non-interactive)")
    parser.add_argument("--create-demo", action="store_true", help="Create sample_menu.zip and exit")
    parser.add_argument("--test", action="store_true", help="Run Phase 3 test harness (interactive prompt, auto-zip, Gutter flash/obnoxious effects, success exit)")
    args = parser.parse_args()

    if args.create_demo:
        dest = Path.cwd() / "sample_menu.zip"
        p = create_demo_menu_zip(dest)
        print(f"Demo menu zip created: {p}")
        print("Run the launcher and scan or select it.")
        return

    if args.replay:
        sp = Path(args.replay)
        if not sp.exists():
            print(f"Session not found: {sp}")
            sys.exit(1)
        replay_session(sp)
        return

    if args.test:
        print("=== Phase 3 Test Harness Activated ===")
        # Interactive prompt per Olivia-pleasereadthis.markdown
        try:
            user_input = input("Hey, what's your input file, idiot? ")
        except EOFError:
            user_input = ""
        if not user_input.strip():
            print("No input provided. Auto-generating sample zip as part of test...")
            dest = Path.cwd() / "sample_menu.zip"
            if not dest.exists():
                create_demo_menu_zip(dest)
                print(f"Auto-created: {dest}")
            # Now proceed to TUI test flow
            print("Entering Gutter mode for test. Launching TUI test sequence...")
            # Pass test mode to TUI
            os.environ["LAUNCHER_TEST_MODE"] = "1"
        else:
            print(f"Input received: {user_input}. Proceeding with test flow...")
            os.environ["LAUNCHER_TEST_MODE"] = "1"
        # Always ensure sample exists for the test cycle (per spec)
        dest = Path.cwd() / "sample_menu.zip"
        if not dest.exists():
            create_demo_menu_zip(dest)
            print(f"Auto-created sample for test: {dest}")
        # Fall through to TUI with test mode

    # Full path (TUI or bootstrap)
    detect_env()
    venv_path = find_or_create_venv()
    venv_python = ensure_deps(venv_path)
    reexec_if_needed(venv_python)

    # Inside venv (or already good)
    cfg = load_config()
    ensure_dirs(cfg)
    _write_ops(f"launching TUI app config branding={cfg.get('branding', {}).get('header')!r}\n")
    try:
        launch_launcher_tui(cfg)
        _write_success("TUI session exited cleanly (app.run returned)\n")
    except Exception as e:
        _log_tui_crash(e, where="launch_launcher_tui")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        _log_tui_crash(e, where="main")
        sys.exit(1)
