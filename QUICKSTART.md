# QUICKSTART

**AWESOME LAUNCHER OF TUI DOOM v0.1.0**  
Rock-solid Python TUI for zip-packaged menus/harnesses. BBS-simple but god-tier.

See PHILOSOPHY.md for why. See OLIVIAPLEASEREADTHIS.md for full plan + Olivia references. See CHANGELOG.md for history.

## Requirements
- Python 3.x in PATH.
- That's it (bootstrap handles venv + textual/rich).

## One-line install (preferred — dirty simple)

```bash
# Linux / WSL / macOS (from repo root)
chmod +x install.sh
./install.sh                  # sprawl + venv + deps + strobe + launch
./install.sh --no-launch      # setup only
./install.sh --recon-only     # environment report → logs/recon-report.*
./install.sh --install-python # opt-in: try to install system Python if missing
```

```powershell
# Windows
.\install.ps1
.\install.ps1 -NoLaunch
# or double-click run.cmd
```

**Roadmap (all PRs):** [docs/PR-ROADMAP.md](docs/PR-ROADMAP.md)  
**Doc hub:** [docs/DOC-INDEX.md](docs/DOC-INDEX.md)  
**Tests (PR-09):** `python scripts/run_harness.py` — see [docs/TESTING.md](docs/TESTING.md)  
**Dist (PR-10):** `python scripts/build_dist.py` — wheel / wheelhouse — [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md)  
**Menus (PR-11…15):** [docs/menu-system/README.md](docs/menu-system/README.md) — runtime Menu UI + capability demo

| In TUI | Key / button |
|--------|----------------|
| **Open Menu UI** (capability pack) | `m` / “Open Menu UI” |
| Run selected menu action | Enter / `r` (inside Menu UI) |
| 6-panel gallery + nested menus | `G` / “Gallery 6-Panel” |
| Effects (strobe/sparkle) | `E` / “Effects FX” |
| Gutter | `g` |
| Quit | `ctrl+q` |

Default launch with no zip → creates `sample_menu.zip` (wave · file picker · web search · legacy harness) and opens Menu UI.

**If it crashes:** `tail -100 logs/tui_crash.log` and `logs/error.log`

## Run It (manual)
```powershell
# From repo root (if you already have venv/deps)
python AWESOME_LAUNCHER_OF_TUIDOOM.py
```

- Default: "Go find a real menu" — scans for *.zip, lists/selects via ListView.
- Extract → run harness → live Log output.
- Chunked: enter date (YYYY-MM-DD) or range for memory-file style processing.
- Gutter: press `g` or button (two-layer intense pink/black ruined C-64 mode).
- Record: toggle, run, save session for replay.
- Quit: ctrl+q.

## Demo Everything
```powershell
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
python AWESOME_LAUNCHER_OF_TUIDOOM.py --test
# Follow prompts for full Phase 3 self-test (prompt, auto-zip, gutter-1 flash circle, obnoxious, success exit)
```

## Create Your Own Menu (zip)
1. Make folder with:
   - menu.json (name, main_script: "harness.py")
   - harness.py (your script, accept --chunk, --log-dir, write logs, sys.exit(0/1/2))
2. Zip it.
3. Drop in . or configured path.
4. Scan + run.

Example harness in sample_menu.zip (auto-created).

## Direct CLI
```powershell
python AWESOME_LAUNCHER_OF_TUIDOOM.py --replay sessions/xxx.json
python AWESOME_LAUNCHER_OF_TUIDOOM.py --test
```

## Polish / Live Notes
- See TUI_Launcher_Planning.md for Phase 1-3 details.
- Gutter, multi-pane, ListView, Log streaming all per Olivia's canonical guides (referenced from OLIV.DIVA/nests/lore-nest/chat-skills/olivia-dev-alpha).
- Initial v0.1.0 — repo polished for live use.

Run, toggle Gutter, test the harness, record a session. It just works.

(Modeled on olivia-dev-alpha quickstart patterns.)