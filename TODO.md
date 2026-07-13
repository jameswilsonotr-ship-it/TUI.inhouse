# TODO

Active tasks for AWESOME LAUNCHER OF TUI DOOM (v0.1.0 live).

See TUI_Launcher_Planning.md and OLIVIAPLEASEREADTHIS.md for full Phase plans.
See WISHLIST.md for future wishes.
Reference: OLIV.DIVA/nests/lore-nest/chat-skills/olivia-dev-alpha/ (TODO style, research-wishlist, etc.)

## Current (Post v0.1.0)

### Planned / executing PRs — see [`docs/PR-ROADMAP.md`](docs/PR-ROADMAP.md)
- [x] **PR-01** One-line bootstrap scaffold (`install.sh` / ps1 / monorepo `install-tui.sh`)
- [x] **PR-02** Recon scaffold + bootstrap dep logs (`scripts/recon.py`, `logs/error.log` for deps)
- [x] **PR-03** Launch harden: fix `Screen` import + `logs/tui_crash.log` for uncaught crashes
- [x] **PR-04** Layout chrome: `tui_chrome/layouts.py` + `chrome.tcss`
- [x] **PR-05** Six-panel gallery + nested submenu + layout modes (`tui_chrome/gallery.py`, key `G`)
- [x] **PR-06** ANSI/ASCII effects (`tui_chrome/effects.py`, key `E`)
- [x] **PR-07** Strong documentation (`docs/DOC-INDEX`, ARCHITECTURE, HARNESS-CONTRACT, API, TESTING)
- [x] **PR-08** Strong docstrings (`tui_chrome/*`, launcher helpers, entry modules)
- [x] **PR-09** Test harness suite (`tests/`, `scripts/run_harness.py`)
- [x] **PR-10** Distribution scaffold (`pyproject.toml`, `scripts/build_dist.py`, wheelhouse)
- [x] **PR-11** Menu system formal spec + runtime (`menu_model.py`)
- [x] **PR-12** Screen layout + `MenuPackScreen` host UI
- [x] **PR-13** Output windows + `action_runner.py` (CODE-CALL-DISPLAY)
- [x] **PR-14** Sample scripts in capability-demo (wave / file_picker / web_search)
- [x] **PR-15** Default demo zip = capability pack; auto-create/open on launch
- [x] Runtime tests: `test_menu_model`, `test_action_runner`, `test_demo_zip`
- [ ] PR-10b (later): frozen single-file binary (PyInstaller/Nuitka) after wheel path stable
- [ ] PR-10 acceptance: clean-venv install smoke + package-data paths for config/TCSS
- [ ] Polish: pin exact textual version; CI headless pilot for gallery

### Product polish
- [ ] Polish test harness visuals (real pane border flashes via reactive styles, more C-64 animations).
- [ ] Add ListView search/filter (simple input + filter).
- [ ] Robust replay engine (diff on env changes, export as script).
- [ ] venv-per-menu opt-in (manifest driven).
- [ ] Self-test enhancements (assert logs, full cycle verification).
- [ ] Update docs with more screenshots/gifs (when live).
- [ ] Direct CLI run without TUI for simple cases (`--menu foo.zip --chunk today`).
- [ ] More harness examples in references/.

## Phase 4+ Seeds
- Log tailing/search in UI.
- Extract caching + resume.
- Authoring guide for custom zips that fit the TUI patterns.

## Potential PRs — **NOT APPROVED** (concepts only)

See [`docs/PR-ROADMAP.md`](docs/PR-ROADMAP.md) § *Potential PRs — NOT APPROVED*.  
**Do not implement** without explicit human approval.

| ID | Concept | Notes |
|----|---------|--------|
| **P-20** | Wrap any Python | Design Step 3 / schema `wrap_any` — general path wrap, not zip harness |
| **P-21** | 7-phase dashboard + roster | Design Step 4 / Iron Pearl tiles — conflicts with current PHILOSOPHY scope |

These are **not** scheduled work and are **not** on the PR-07…15 ship table.

## Maintenance
- Keep no bloat.
- Always reference olivia-dev-alpha for philosophy/gutter/branding.
- Test with --test after changes.
- Update CHANGELOG on every commit.

Run `python AWESOME_LAUNCHER_OF_TUIDOOM.py --test` to exercise current state.

(Modeled on olivia-dev-alpha TODO/wishlist structure.)