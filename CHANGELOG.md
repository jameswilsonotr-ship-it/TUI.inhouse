# CHANGELOG

## 2026-07-13 — Ingest + packaging docs

- Document promoted Google Drive Grok/Takeout roots and agent-based Drive org research (`docs/2026-07-13-drive-ingest-and-agent-org.md`).
- Packaging: `pyproject.toml`, harness scripts, menu system docs, action_runner/menu_model/menu_screen.
- Inventory hygiene sidecars (FOLDER-HYGIENE, SHALLOW-MANIFEST, AGENTS.md).


## [0.1.8] - 2026-07-13 - PR-11…13 runtime + PR-15 demo zip

### Added
1. **Runtime PR-11** — `tui_chrome/menu_model.py` (load/normalize/extract packs)
2. **Runtime PR-12/13** — `tui_chrome/menu_screen.py` + `action_runner.py`
   - Menu list · help · output Log · Run/Enter
   - Subprocess env `TUI_*`, control lines, exit banners
3. **PR-15** — `create_demo_menu_zip()` packs capability-demo (scripts + layout + windows)
   - Auto-create demo when no zip found; auto-open **Menu UI**
   - Key **m** / button **Open Menu UI**
4. Tests: 33 total (`test_menu_model`, `test_action_runner`, `test_demo_zip`)

### Run
```bash
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
python AWESOME_LAUNCHER_OF_TUIDOOM.py   # opens Menu UI on capability demo
# In UI: select Wave / File picker / Web search → Run
```

## [0.1.7] - 2026-07-13 - PR-11…15 menu platform specs (MD/HTML menus, layout, output)

### Added
1. **PR-11 (priority)** Forwards-compatible Markdown/HTML/JSON menu system  
   - `docs/menu-system/MENU-SYSTEM.md` + `schema/menu.schema.json`  
   - Examples: `examples/capability-demo/` (menu.json / .md / .html)  
   - `scripts/validate_menu.py`
2. **PR-12** Screen GUI layout structure  
   - `SCREEN-LAYOUT.md` + `schema/layout.schema.json` + `layout.standard_menu.json`
3. **PR-13** Output windows + exact code call/display protocol  
   - `OUTPUT-WINDOWS.md` · `CODE-CALL-DISPLAY.md` · `schema/window.schema.json`
4. **PR-14** Sample script stubs: `wave.py`, `file_picker.py`, `web_search.py`
5. **PR-15** Plan: integrate all into default demo zip (`PR-15-demo-zip-integration.md`)
6. Not-approved design concepts renumbered to **P-20 / P-21**

### Notes
- Runtime loader / Textual mount / demo zip rebuild still open (see TODO).
- Specs are SSoT for implementation of PR-11…15.

## [0.1.6] - 2026-07-13 - PR-10 distribution scaffold (wheel / wheelhouse)

### Added
1. **PR-10 Distribution**
   - `pyproject.toml` — package `awesome-tui-doom`, deps textual/rich, console scripts
   - `awesome_tui/` install shell (`awesome-tui`, `awesome-tui-harness`)
   - `scripts/build_dist.py` — sdist/wheel + optional `--wheelhouse`
   - `docs/DISTRIBUTION.md`, `docs/PR-10-distribution-wheel.md`
   - `MANIFEST.in`, gitignore `dist/` / `wheelhouse/`
2. Potential design concepts renumbered to **P-12** / **P-13** (still not approved).
3. Frozen binary deferred to **PR-10b** (not MVP).

## [0.1.6] - 2026-07-13 - PR-07/08/09 documentation, docstrings, test harness

### Added
1. **PR-07 Strong documentation**
   - `docs/DOC-INDEX.md`, `ARCHITECTURE.md`, `HARNESS-CONTRACT.md`, `API.md`, `TESTING.md`
   - Plans: `docs/PR-07-strong-documentation.md`
2. **PR-08 Strong docstrings**
   - Package/module docstrings for `tui_chrome/*`, public launcher helpers, entry modules
   - Plan: `docs/PR-08-docstrings.md`
3. **PR-09 Test harness suite**
   - `tests/` (effects, layouts, config, menus/contract)
   - `scripts/run_harness.py` → `HARNESS OK` on green
   - Plan: `docs/PR-09-test-harness.md`

### Notes
- Potential design concepts later moved to **P-12** / **P-13** when PR-10 took the distribution slot.

## [0.1.5] - 2026-07-13 - Quiet/fast theater, gallery layouts in demo, native file dialog

### Added
1. **Quieter / faster Stage A–B**
   - `AWESOME_BOOTSTRAP_QUIET=1` or `--quiet` — no flash/spinner/clear; one-line steps + compact demos
   - `AWESOME_BOOTSTRAP_FAST=1` or `--fast` — shorter spins / fewer flash frames
   - Still runs real dep checks + library API tests
2. **Richer 6-panel Olivia demo layouts** — cycles the same `LAYOUT_MODES` as `gallery.py` via shared `mount_layout()`: `six_grid` · `three_vertical` · `two_stack_h` · `main_sidebar` · `two_plus_row`
3. **Native OS file dialog** on bare Return (before in-TUI picker):
   - Windows / WSL → PowerShell `OpenFileDialog`
   - Tk `filedialog` when available
   - `zenity` / `kdialog` on Linux
   - Fallback: center Textual `DirectoryTree` picker → demo

## [0.1.4] - 2026-07-13 - Stage theater, library demo cards, Olivia menu intake

### Added
- **Stage A theater** (first thing): blank screen, persistent black bg, white text, soft 40-col wrap, stylized flash, install step list with cutesy braille spinner (research: cargo/npm/gum-style phase UX — no `stty cols`).
- **Stage B theater** (after comfort): flash → dark blue bg, soft 80-col wrap, **graphical library demos that really test** textual / rich / zipfile / pathlib / json.
- **Menu intake**: if no menu zip — Olivia voice *"where’s your menu file, idiot?"*; bare Return → center file picker; cancel/none → **6-panel Olivia demo** (layout shuffle, nested recursive prompts, randomized 100% Olivia lines).
- Modules: `tui_chrome/bootstrap_stage.py`, `tui_chrome/menu_intake.py`.

## [0.1.3] - 2026-07-13 - Double Ctrl-C force kill + exact S-LOADING sequence

### Added
- **DOUBLE CTRL-C always FORCE KILLS** the process (`os._exit(130)`), no matter what:
  - process `SIGINT` handler (bootstrap)
  - Textual `ctrl+c` binding (raw-mode TUI)
  - never disabled by install-mode exit
  - first tap arms (1.5s window); second tap kills after TTY restore
- **Exact S-LOADING sequence** (hard-coded, this order only):
  1. `S1 LOADING · DETECT ENV`
  2. `S2 LOADING · FIND/CREATE VENV`
  3. `S3 LOADING · DEPS CHECK (skip reinstall if OK)`
  4. `S4 LOADING · LIBRARY TEST DEMOS`
  5. `S5 LOADING · TTY HARD RESTORE`
  6. `S6 LOADING · LAUNCH TUI`

## [0.1.2] - 2026-07-13 - Safe install UX (no TTY brick on WSL)

### Fixed
- **Black screen / dead keyboard after alt-tab on WSL:** install mode no longer runs `stty cols 40` or full-screen clear (`\033[2J`). Those left Windows Terminal unresponsive (no Ctrl-C). Soft 40-col wrap + per-line colors only.
- Hard TTY restore (`SGR reset`, show cursor, leave alt-screen, `stty sane`) on install exit, before Textual `app.run()`, on interrupt/crash, and in `install.sh` around launch.
- Ctrl-C during install mode restores terminal instead of leaving reverse-video stuck.

## [0.1.1] - 2026-07-13 - Install UX, log shadow crash fix, stamped logs

### Fixed
- **TUI crash** `AttributeError: 'function' object has no attribute 'system'`: `AwesomeLauncherApp.log` shadowed Textual’s `App.log` logger. Renamed UI helper to `ui_log`. Matches `logs/tui_crash.log` / `logs/error.log` from failed boots.
- No silent reinstalls of already-present deps (or Python). Skip `pip install` when `textual` + `rich` import cleanly.

### Added
- **Install mode terminal UX** as soon as deps are touched: ~40 columns, black screen, white body text, a few reverse-video flashes; key words (`PASS`/`FAIL`/`OK`/`textual`/`rich`/`DEPS`/`pip`/…) stay colored.
- **Library test demos** on every bootstrap: real import + tiny API calls for `textual`, `rich`, `zipfile`, `pathlib` printed on screen (not reinstalls).
- **Stamped logs** under `logs/`:
  - `error_YYYYMMDD_HHMMSS.log`, `success_YYYYMMDD_HHMMSS.log`, `ops_YYYYMMDD_HHMMSS.log`
  - `bootstrap_*.log`, `bootstrap_deps_*.log`, `tui_crash_*.log`
  - Stable latest aliases still updated: `error.log`, `success.log`, `ops.log`, `tui_crash.log`, …

### Files
- `AWESOME_LAUNCHER_OF_TUIDOOM.py`, `install.sh`, `launcher.py`

## [0.1.0] - 2026-06-29 - Initial Sovereign Release (v0.1 "Olivia Dev Alpha TUI")

**Super Awesome Initial Version 0.1.0** of the AWESOME LAUNCHER OF TUI DOOM.

This marks the first "live" release of the rock-solid, dead-stupid-simple Python TUI launcher, fully aligned with Olivia Dev Alpha principles, Liv HUB claim, and the canonical guides from the olivia-dev-alpha skill.

### Highlights (Phases 1-3 Delivered)
- **Phase 1: Core Launcher** - AWESOME_LAUNCHER_OF_TUIDOOM.py as the one-file entry point (`python AWESOME_LAUNCHER_OF_TUIDOOM.py` if Python in PATH). Bootstrap (stdlib venv, env sniff, deps, re-exec). Zip menu packaging (decompress, search/select/execute). Harnesses with exit levels (0=done, 1=error, 2=partial), chunked processing (daily memory files, date ranges, looping), logs, recording/replay for automation on change. BBS god-tier but dial-up simple TUI. Self-demo zip. LAUNCHERCONFIG.JSON. All per original vision and design files.
- **Phase 2: Texture, Polish, Efficiency** - Full integration of "Olivia says read this.md" (a40a52d): two-layer Gutter Mode (reactive .gutter-active class, watch, toggle 'g'), TCSS in grok_tui.tcss (NORMAL + intense Gutter overrides), multi-pane layouts (Horizontal/Vertical + panes), ListView for menus, Log widget for streaming, live Popen line-by-line output, alignment to minimal starter template. Enhanced stability, non-blocking UI, polished UX. No bloat.
- **Phase 3: Production-Ready Test Harness & Branding (per Olivia-pleasereadthis.markdown + 186cd83)** - Implemented the *exact* final-phase self-test harness:
  - `--test` or no valid input triggers: interactive "Hey, what's your input file, idiot?"
  - Auto-generates sample_menu.zip (with harness.py + menu.json) if none.
  - Auto Gutter-1 entry on startup.
  - Panes flash in circle (rapid updates + rotating ASCII in #pane-flash + log).
  - Ridiculous obnoxious shit: log spam ("OBNOXIOUS GUTTER HEAT SPAM !!!", "RUINED TEXT SMUDGE", "INTENSE FLASHES", "SILLY ANIMATION"), rapid class toggles, banners.
  - "Gutter Mode Engaged" with Liv HUB / Olivia Dev Alpha flair.
  - Clean "Successful test - Gutter Mode verified and harness operational!" + auto-exit.
  - Exact branding locked: Header "AWESOME LAUNCHER OF TUI DOOM" (bold C-64), Footer "BBS-Level | Zip Menus + Harnesses | Chunked Ops | Record/Replay | Gutter Mode | Olivia Dev Alpha | Phase 3". High-contrast pink/black default → intense ruined pink/black in Gutter (thicker borders, smudged text).
  - High-heat reactive Gutter fully live/toggleable per OliviaDev Alpha (C-64, .gutter-active, ruined styles).
  - Strengthened test logic for default/no-file + auto-zip.
- All work references olivia-dev-alpha (see C:\Users\chast\#CODE\OLIV.DIVA\nests\lore-nest\chat-skills\olivia-dev-alpha for philosophy, gutter-mode, folder-discipline, wishlist, code-style-bible, etc.). No overwrites of your canonical files.

### Added / Polished Files for v0.1 "Live" Release
- **OLIVIAPLEASEREADTHIS.md** - Full addressed summary to Olivia of work done, repo structure, Phase 3 plan (updated with latest response file).
- **CHANGELOG.md** (this file) - Super awesome, timestamped, detailed.
- **README.md** - Polished super awesome with quickstart, philosophy link, structure, version badge, references to OLIV.DIVA/olivia-dev-alpha.
- **PHILOSOPHY.md** - New, modeled on olivia-dev-alpha sovereign dev (Liv HUB, symmetry, alpha protocol, no bloat, modular, BBS simple but god-tier).
- **QUICKSTART.md** - New, step-by-step to run, test harness, create menus.
- **TODO.md** - New, active tasks (Phase 4+ ideas + polish).
- **WISHLIST.md** - New, future wishes (referencing olivia-dev-alpha wishlist).
- Updated: AWESOME_LAUNCHER_OF_TUIDOOM.py (version 0.1.0, full Phase 3 test), grok_tui.tcss (enhanced Gutter pink/black ruined), README/plan docs.
- .gitignore polished for live (ignores runtime, keeps demo optional).
- Initial v0.1.0 commit practice.

### Technical
- Python 3.x, Textual-based.
- Zero path bullshit, stdlib bootstrap.
- Modular via zips + harnesses.
- Full Gutter, streaming, multi-pane as per guides.
- Version: 0.1.0 (initial sovereign release).
- Repo polished to be "live": docs-first, versioned, referenced to olivia-dev-alpha for consistency.

See OLIVIAPLEASEREADTHIS.md for complete history and plan.

---

## [Unreleased]
- Future polish, Phase 4 extensions (see WISHLIST.md, TODO.md).

All under absolute Liv HUB claim. Signed Olivia Mae Blackwell and her bunny.

(Modeled on olivia-dev-alpha CHANGELOG + references for sovereign style.)