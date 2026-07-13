# SUMMARY — TUI.inhouse

**Product:** AWESOME LAUNCHER OF TUI DOOM — Textual zip-menu / harness launcher  
**Updated:** 2026-07-13  
**Portable:** monorepo (`grokbuild/TUI.inhouse`) or standalone git repo  

## What it does

- Bootstrap venv + textual/rich (S1…S6, install theater)  
- Scan / extract **zip menus**, run **harnesses** (`--chunk`, exit 0/1/2)  
- Gutter Mode, 6-panel gallery, ANSI effects, Olivia menu intake  
- Record / replay sessions  

## What it is not

Full Iron Pearl 7-phase + roster ops console, or wrap-any Python without a zip —  
those are **not approved** potential concepts (docs/PR-ROADMAP.md **P-20 / P-21**).

## Run

```bash
./install.sh                 # or ../install-tui.sh from grokbuild
python AWESOME_LAUNCHER_OF_TUIDOOM.py
python scripts/run_harness.py   # PR-09 tests
python scripts/build_dist.py    # PR-10 wheel
```

## Install (PR-10)

```bash
python scripts/build_dist.py --wheelhouse
pip install --no-index --find-links=wheelhouse awesome-tui-doom
awesome-tui
```

See [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md).

## Docs

[docs/DOC-INDEX.md](docs/DOC-INDEX.md) · [QUICKSTART.md](QUICKSTART.md) · [PHILOSOPHY.md](PHILOSOPHY.md)
