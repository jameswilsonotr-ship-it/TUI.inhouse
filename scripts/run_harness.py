#!/usr/bin/env python3
"""PR-09 — one-command test harness runner for TUI.inhouse.

Runs stdlib unittest discovery under ``tests/``. Optional product smoke:

    python scripts/run_harness.py --create-demo

Exit codes:
  0  all tests passed
  1  failures / errors / import problems

See docs/TESTING.md and docs/PR-09-test-harness.md.
"""
from __future__ import annotations

import argparse
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _ensure_path() -> None:
    root_s = str(ROOT)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    os.chdir(ROOT)


def run_unit() -> unittest.TestResult:
    """Discover and run tests/ with verbosity."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


def run_create_demo() -> int:
    """Optional: write sample_menu.zip without launching TUI."""
    import AWESOME_LAUNCHER_OF_TUIDOOM as launcher

    cfg = launcher.load_config()
    name = cfg.get("demo", {}).get("sample_zip_name", "sample_menu.zip")
    dest = ROOT / name
    launcher.create_demo_menu_zip(dest)
    print(f"create-demo: wrote {dest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry — unit tests always; optional demo zip smoke."""
    parser = argparse.ArgumentParser(description="TUI.inhouse test harness (PR-09)")
    parser.add_argument(
        "--create-demo",
        action="store_true",
        help="Also run product --create-demo (write sample zip, no TUI)",
    )
    parser.add_argument(
        "--unit-only",
        action="store_true",
        help="Alias for default unit run (explicit)",
    )
    args = parser.parse_args(argv)

    _ensure_path()
    print(f"HARNESS root={ROOT}")
    print(f"HARNESS python={sys.executable}")

    result = run_unit()
    ok = result.wasSuccessful()
    if args.create_demo:
        try:
            run_create_demo()
        except Exception as exc:  # noqa: BLE001 — report and fail harness
            print(f"create-demo FAILED: {exc}", file=sys.stderr)
            ok = False

    if ok:
        print(
            f"HARNESS OK  tests={result.testsRun}  "
            f"failures={len(result.failures)}  errors={len(result.errors)}"
        )
        return 0

    print(
        f"HARNESS FAIL  tests={result.testsRun}  "
        f"failures={len(result.failures)}  errors={len(result.errors)}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
