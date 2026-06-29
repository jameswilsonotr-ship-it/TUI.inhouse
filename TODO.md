# TODO

Active tasks for AWESOME LAUNCHER OF TUI DOOM (v0.1.0 live).

See TUI_Launcher_Planning.md and OLIVIAPLEASEREADTHIS.md for full Phase plans.
See WISHLIST.md for future wishes.
Reference: OLIV.DIVA/nests/lore-nest/chat-skills/olivia-dev-alpha/ (TODO style, research-wishlist, etc.)

## Current (Post v0.1.0)
- [ ] Polish test harness visuals (real pane border flashes via reactive styles, more C-64 animations).
- [ ] Add ListView search/filter (simple input + filter).
- [ ] Robust replay engine (diff on env changes, export as script).
- [ ] venv-per-menu opt-in (manifest driven).
- [ ] Self-test enhancements (assert logs, full cycle verification).
- [ ] Update docs with more screenshots/gifs (when live).
- [ ] Direct CLI run without TUI for simple cases (`--menu foo.zip --chunk today`).
- [ ] Packaging story (single .py + config is the dist).
- [ ] More harness examples in references/.

## Phase 4+ Seeds
- Optional bridge to textual_main_app_schema for 7-phase screens.
- Log tailing/search in UI.
- Extract caching + resume.
- Authoring guide for custom zips that fit the TUI patterns.

## Maintenance
- Keep no bloat.
- Always reference olivia-dev-alpha for philosophy/gutter/branding.
- Test with --test after changes.
- Update CHANGELOG on every commit.

Run `python AWESOME_LAUNCHER_OF_TUIDOOM.py --test` to exercise current state.

(Modeled on olivia-dev-alpha TODO/wishlist structure.)