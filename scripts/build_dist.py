#!/usr/bin/env python3
"""PR-10 — build sdist/wheel and optional offline wheelhouse.

Usage
-----
    python scripts/build_dist.py
    python scripts/build_dist.py --wheelhouse
    python scripts/build_dist.py --wheelhouse --clean

See docs/DISTRIBUTION.md.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
WHEELHOUSE = ROOT / "wheelhouse"


def _run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd or ROOT))


def ensure_build_tools() -> None:
    """Install build/wheel into the *current* interpreter if missing."""
    try:
        import build  # noqa: F401
    except ImportError:
        _run([sys.executable, "-m", "pip", "install", "-U", "build", "wheel"])


def clean_outputs() -> None:
    """Remove dist/ and wheelhouse/."""
    for d in (DIST, WHEELHOUSE):
        if d.exists():
            print(f"clean: {d}")
            shutil.rmtree(d)


def build_sdist_wheel() -> None:
    """Produce sdist + wheel under dist/ via pep517 build."""
    DIST.mkdir(parents=True, exist_ok=True)
    _run([sys.executable, "-m", "build", "--outdir", str(DIST)])


def build_wheelhouse() -> None:
    """Download/build wheels for this project + all dependencies into wheelhouse/.

    Offline install::

        pip install --no-index --find-links=wheelhouse awesome-tui-doom
    """
    WHEELHOUSE.mkdir(parents=True, exist_ok=True)
    # Prefer installing our just-built wheel into the house, plus deps.
    wheels = sorted(DIST.glob("*.whl"))
    if not wheels:
        raise SystemExit("build_wheelhouse: no wheel in dist/; build first")

    req = ROOT / "requirements.txt"
    # pip download project wheel + requirements (binary preferred)
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--dest",
        str(WHEELHOUSE),
        str(wheels[-1]),
    ]
    if req.is_file():
        cmd.extend(["-r", str(req)])
    _run(cmd)
    print(f"wheelhouse ready: {WHEELHOUSE} ({len(list(WHEELHOUSE.glob('*.whl')))} wheels)")


def main(argv: list[str] | None = None) -> int:
    """CLI for distribution builds."""
    parser = argparse.ArgumentParser(description="Build TUI.inhouse wheels (PR-10)")
    parser.add_argument(
        "--wheelhouse",
        action="store_true",
        help="Also build offline wheelhouse of product + deps",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove dist/ and wheelhouse/ before building",
    )
    args = parser.parse_args(argv)

    print(f"build_dist root={ROOT}")
    if args.clean:
        clean_outputs()

    ensure_build_tools()
    build_sdist_wheel()

    if args.wheelhouse:
        build_wheelhouse()

    print("BUILD OK")
    for p in sorted(DIST.glob("*")):
        print(f"  dist: {p.name}")
    if args.wheelhouse and WHEELHOUSE.exists():
        print(f"  wheelhouse: {len(list(WHEELHOUSE.glob('*.whl')))} wheels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
