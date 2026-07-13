# CHANGELOG

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