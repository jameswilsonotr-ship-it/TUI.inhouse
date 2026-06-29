#!/usr/bin/env python3
"""
launcher.py - Grok TUI Launcher bootstrap (per design principles and walkthrough)
Stdlib only for bootstrap. Detects env, sets up venv, installs deps, re-execs, launches TUI.
This is the "at worst just run python + script name" entry point.
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
    """Per-module / core dep installation that doesn't suck."""
    python_bin = venv_path / ("Scripts/python.exe" if sys.platform.startswith("win") else "bin/python")
    pip = [str(python_bin), "-m", "pip"]
    print("Ensuring core deps (textual, rich)...")
    try:
        subprocess.check_call(pip + ["install", "--upgrade", "pip"])
        subprocess.check_call(pip + ["install"] + CORE_DEPS)
    except subprocess.CalledProcessError as e:
        print(f"Dep install failed: {e}")
        sys.exit(1)
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
    # Import after venv
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
