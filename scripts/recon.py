#!/usr/bin/env python3
"""PR-02 scaffold: environment reconnaissance for AWESOME LAUNCHER OF TUI DOOM.

Usage:
  python scripts/recon.py
  python scripts/recon.py --out logs
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import sys
import datetime
from pathlib import Path


def _try_import(name: str):
    try:
        mod = __import__(name)
        ver = getattr(mod, "__version__", None) or getattr(mod, "VERSION", None)
        return True, str(ver) if ver is not None else "unknown"
    except Exception as e:
        return False, str(e)


def pypi_reachable(timeout: float = 3.0) -> dict:
    try:
        socket.create_connection(("pypi.org", 443), timeout=timeout).close()
        return {"ok": True, "error": None}
    except OSError as e:
        return {"ok": False, "error": str(e)}


def main() -> int:
    ap = argparse.ArgumentParser(description="TUI.inhouse recon report")
    ap.add_argument("--out", default="logs", help="output directory")
    ap.add_argument("--root", default=None, help="project root (default: parent of scripts/)")
    args = ap.parse_args()

    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.mkdir(parents=True, exist_ok=True)

    is_wsl = bool(os.environ.get("WSL_DISTRO_NAME")) or (
        "microsoft" in platform.release().lower()
    )

    textual_ok, textual_ver = _try_import("textual")
    rich_ok, rich_ver = _try_import("rich")

    expected = [
        "AWESOME_LAUNCHER_OF_TUIDOOM.py",
        "LAUNCHERCONFIG.JSON",
        "grok_tui.tcss",
        "install.sh",
        "requirements.txt",
    ]
    files = {name: (root / name).is_file() for name in expected}

    err_log = root / "logs" / "error.log"
    err_tail = ""
    if err_log.is_file():
        try:
            err_tail = err_log.read_text(encoding="utf-8", errors="replace")[-2000:]
        except OSError as e:
            err_tail = f"<read error: {e}>"

    usage = shutil.disk_usage(root)
    report = {
        "generated": datetime.datetime.now().isoformat(),
        "root": str(root),
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "platform": platform.platform(),
            "wsl": is_wsl,
            "cwd": str(Path.cwd()),
        },
        "python": {
            "executable": sys.executable,
            "version": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "prefix": sys.prefix,
            "base_prefix": getattr(sys, "base_prefix", sys.prefix),
            "in_venv": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
        },
        "deps": {
            "textual": {"importable": textual_ok, "detail": textual_ver},
            "rich": {"importable": rich_ok, "detail": rich_ver},
        },
        "disk": {
            "total_gb": round(usage.total / 1e9, 2),
            "free_gb": round(usage.free / 1e9, 2),
        },
        "network": {"pypi_org_443": pypi_reachable()},
        "files_present": files,
        "runtime_dirs": {
            "logs": (root / "logs").is_dir(),
            "sessions": (root / "sessions").is_dir(),
            ".venv": (root / ".venv").is_dir(),
            ".launcher_menus": (root / ".launcher_menus").is_dir(),
        },
        "error_log_tail": err_tail,
        "tips": [],
    }

    tips = report["tips"]
    if not all(files.values()):
        tips.append("Missing expected product files — re-clone or re-copy the repo root.")
    if not textual_ok or not rich_ok:
        tips.append("Run: ./install.sh --no-launch   (or .venv/bin/pip install -r requirements.txt)")
    if not report["network"]["pypi_org_443"]["ok"]:
        tips.append("PyPI not reachable — fix network/proxy before pip install.")
    if report["disk"]["free_gb"] < 0.5:
        tips.append("Low disk space (<0.5 GB free).")
    if "pip._vendor.rich" in err_tail or "themes" in err_tail:
        tips.append("Broken pip vendor rich — rm -rf .venv && ./install.sh --no-launch")
    if not tips:
        tips.append("Recon looks healthy. Launch: ./install.sh   or   python AWESOME_LAUNCHER_OF_TUIDOOM.py")

    json_path = out / "recon-report.json"
    md_path = out / "recon-report.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        f"# Recon report — TUI.inhouse",
        f"",
        f"**Generated:** {report['generated']}",
        f"**Root:** `{report['root']}`",
        f"",
        f"## Python",
        f"- executable: `{report['python']['executable']}`",
        f"- version: {report['python']['version']} ({report['python']['implementation']})",
        f"- in_venv: {report['python']['in_venv']}",
        f"",
        f"## Deps",
        f"- textual: {textual_ok} ({textual_ver})",
        f"- rich: {rich_ok} ({rich_ver})",
        f"",
        f"## Host",
        f"- {report['host']['platform']}  WSL={is_wsl}",
        f"- disk free: {report['disk']['free_gb']} GB",
        f"- pypi: {report['network']['pypi_org_443']}",
        f"",
        f"## Files",
    ]
    for k, v in files.items():
        md.append(f"- {'OK' if v else 'MISSING'} `{k}`")
    md += ["", "## Tips"]
    for t in tips:
        md.append(f"- {t}")
    if err_tail:
        md += ["", "## error.log tail", "```", err_tail, "```"]
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    for t in tips:
        print(f"  tip: {t}")
    # exit 0 if core deps importable else 1
    return 0 if textual_ok and rich_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
