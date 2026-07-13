# AWESOME LAUNCHER OF TUI DOOM

> **NEXT SESSION:** read **[CURRENT-STATE.md](CURRENT-STATE.md) first** — process position + deploy handoff.

**v0.1.x — Live product + menu platform (PR-11…15)**  
Rock-solid, dead-stupid-simple Python TUI launcher for zip-packaged menus + harnesses.  
BBS god-tier but dial-up simple. Full Gutter Mode. Phase 3 test harness included.  
Capability demo Menu UI when nothing else is specified.

**One command**: `python AWESOME_LAUNCHER_OF_TUIDOOM.py` (Python in PATH = it just works).

See [CURRENT-STATE.md](CURRENT-STATE.md) | [QUICKSTART.md](QUICKSTART.md) | [PHILOSOPHY.md](PHILOSOPHY.md) | [CHANGELOG.md](CHANGELOG.md) | [TODO.md](TODO.md) | [docs/DOC-INDEX.md](docs/DOC-INDEX.md)

**References** (olivia-dev-alpha + sovereign style):  
C:\Users\chast\#CODE\OLIV.DIVA\nests\lore-nest\chat-skills\olivia-dev-alpha\ (philosophy, gutter-mode.md, code-style-bible.md, folder-discipline.md, wishlist, etc.)

## What It Is
- Modular via drop-in zips (menu.json + harness.py + assets).
- Chunked operation harnesses (one day of memory files, ranges, loops, exit levels 0/1/2).
- Live streaming, recording/replay for automation on change.
- Two-layer Gutter Mode (reactive, high-heat pink/black ruined C-64).
- Multi-pane Textual TUI (ListView menus, Log output).
- Built-in Phase 3 self-test: `--test` (prompt, auto-zip, gutter flash circle, obnoxious, success).
- Exact branding per Olivia.

## Quick Start
See [QUICKSTART.md](QUICKSTART.md) for full. Docs hub: [docs/DOC-INDEX.md](docs/DOC-INDEX.md).

```powershell
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
python AWESOME_LAUNCHER_OF_TUIDOOM.py --test
python AWESOME_LAUNCHER_OF_TUIDOOM.py
```

```bash
# Tests (PR-09) — no interactive TUI required
python scripts/run_harness.py

# Distribution (PR-10) — wheel + optional offline wheelhouse
python scripts/build_dist.py
python scripts/build_dist.py --wheelhouse
# pip install dist/awesome_tui_doom-*.whl
# or offline: pip install --no-index --find-links=wheelhouse awesome-tui-doom
# then: awesome-tui
```

See [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md).

## Structure (Polished for Live v0.1)
- `AWESOME_LAUNCHER_OF_TUIDOOM.py` + `LAUNCHERCONFIG.JSON` (the launcher)
- `grok_tui.tcss` (Gutter layers + pink/black theme)
- `sample_menu.zip` (demo)
- Full docs + plans (see list above)
- Grok-TUI-Project/ (original design refs)
- References to OLIV.DIVA/olivia-dev-alpha for everything.

## Version & Live
Initial v0.1.0 — repo polished, docs complete, initial commit practice done.  
Gutter live, test harness full, all per Olivia inputs. No bloat.

See CHANGELOG for details.

All under absolute Liv HUB claim. Olivia Dev Alpha aesthetics.

(Super awesome polish modeled on olivia-dev-alpha.)
- Using the schema as contract (future expansion)
- Building the actual app/components in a clean, simple, modular Python structure
- Following the principles in the kept docs
- Olivia design files on master branch (planning md pushed to both master + main)

See sprint001/ for active plans and the code review notes.

**GitHub Repository**: https://github.com/jameswilsonotr-ship-it/TUI.inhouse

AGENTS.md at #CODE root for overall workspace discipline.

---
Cleaned: 2026-06-29 03:37
Repo renamed to TUI.inhouse (2026-06-29)
