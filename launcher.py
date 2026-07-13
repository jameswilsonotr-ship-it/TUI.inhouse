#!/usr/bin/env python3
"""
launcher.py - Grok TUI Launcher bootstrap (per design principles and walkthrough)
Stdlib only for bootstrap. Detects env, sets up venv, installs deps, re-execs, launches TUI.
This is the "at worst just run python + script name" entry point.

PR-04+: skip reinstall when importable; stamped logs under logs/; no App.log shadow.
Prefer AWESOME_LAUNCHER_OF_TUIDOOM.py for the full install UX (40-col black/white).
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Minimal deps for the TUI (per design)
CORE_DEPS = ["textual", "rich"]


def detect_env():
    """Env sniffing first, always (per design)."""
    print("Detecting environment...")
    env_info = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "is_wsl": "WSL_DISTRO_NAME" in os.environ or "microsoft" in platform.release().lower(),
        "is_windows": sys.platform.startswith("win"),
        "is_linux": sys.platform.startswith("linux"),
        "cwd": os.getcwd(),
    }
    for k, v in env_info.items():
        print(f"  {k}: {v}")
    return env_info


def find_or_create_venv():
    """Find/create a base .venv next to launcher (or in known bunker location)."""
    venv_path = Path(__file__).parent / ".venv"
    if not venv_path.exists():
        print(f"Creating venv at {venv_path}...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
    return venv_path


def ensure_deps(venv_path):
    """Install only if missing. Full pip log under logs/ with timestamp stamp."""
    import datetime as _dt

    python_bin = venv_path / (
        "Scripts/python.exe" if sys.platform.startswith("win") else "bin/python"
    )
    pip = [str(python_bin), "-m", "pip"]
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = os.environ.get("AWESOME_LAUNCHER_STAMP") or _dt.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    deps_log = log_dir / f"bootstrap_deps_{stamp}.log"
    deps_latest = log_dir / "bootstrap_deps.log"
    err_log = log_dir / f"error_{stamp}.log"
    err_latest = log_dir / "error.log"
    success_log = log_dir / f"success_{stamp}.log"
    print("Ensuring core deps (textual, rich)...")
    print(f"  pip log → {deps_log}")

    # Skip reinstall if already importable
    check = subprocess.run(
        [str(python_bin), "-c", "import textual, rich"],
        capture_output=True,
        text=True,
    )
    if check.returncode == 0:
        print("  deps already importable — SKIP pip reinstall")
        with open(success_log, "a", encoding="utf-8") as f:
            f.write(f"\n=== {_dt.datetime.now().isoformat()} ===\n")
            f.write("deps present — no reinstall\n")
        return python_bin

    def _run(args, label):
        cmd = pip + args
        proc = subprocess.run(cmd, capture_output=True, text=True)
        blob = (
            f"\n=== {_dt.datetime.now().isoformat()} [{label}] ===\n"
            f"cmd={' '.join(cmd)}\nrc={proc.returncode}\n"
            f"--- stdout ---\n{proc.stdout or ''}\n--- stderr ---\n{proc.stderr or ''}\n"
        )
        for p in (deps_log, deps_latest):
            with open(p, "a", encoding="utf-8") as f:
                f.write(blob)
        if proc.returncode != 0:
            for p in (err_log, err_latest):
                with open(p, "a", encoding="utf-8") as f:
                    f.write("BOOTSTRAP DEP FAILURE\n" + blob)
            for line in (proc.stderr or proc.stdout or "").splitlines()[-20:]:
                print(f"  | {line}")
            print(f"Dep install failed ({label}): exit {proc.returncode}")
            print(f"  Full log: {deps_log}")
            print(f"  Error log: {err_log}")
            raise subprocess.CalledProcessError(proc.returncode, cmd)

    try:
        _run(["install", "--upgrade", "pip"], "upgrade-pip")
        req = Path(__file__).parent / "requirements.txt"
        if req.exists():
            _run(["install", "-r", str(req)], "install-requirements")
        else:
            _run(["install"] + CORE_DEPS, "install-core-deps")
    except subprocess.CalledProcessError:
        sys.exit(1)

    # Library demo tests (on-screen)
    demo = subprocess.run(
        [
            str(python_bin),
            "-c",
            "import textual, rich; from textual.app import App; "
            "from rich.text import Text; t=Text('ok'); "
            "print('TEST textual: PASS'); print('TEST rich: PASS')",
        ],
        capture_output=True,
        text=True,
    )
    print(demo.stdout or "")
    if demo.returncode != 0:
        print("library demos FAIL", demo.stderr)
        sys.exit(1)
    with open(success_log, "a", encoding="utf-8") as f:
        f.write(f"\n=== {_dt.datetime.now().isoformat()} ===\n")
        f.write("deps install + library demos PASS\n")
    return python_bin


def reexec_if_needed(venv_python):
    """Re-exec inside the venv if not already."""
    if os.environ.get("GROK_TUI_VENV") != "1":
        print("Re-executing inside venv...")
        os.environ["GROK_TUI_VENV"] = "1"
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)


def launch_tui():
    """Launch the TUI (uses the schema-driven app from design)."""
    print("Launching Grok TUI (home grid with Gutter Mode, per design)...")
    try:
        from textual_main_app_schema import GrokBuildTUI

        app = GrokBuildTUI()
        app.run()
    except Exception as e:
        print(f"TUI launch error: {e}")
        print("Ensure textual is installed and schema is valid.")
        sys.exit(1)


def main():
    print("Grok TUI Launcher (bootstrap per design walkthrough)")
    detect_env()
    venv_path = find_or_create_venv()
    venv_python = ensure_deps(venv_path)
    reexec_if_needed(venv_python)
    launch_tui()


if __name__ == "__main__":
    main()
