# TUI Menu Research — Copyable / Forkable Examples & Patterns

**Date**: 2026-06-29  
**Goal**: Find real, usable code patterns we can study, adapt, or lightly fork for a sovereign, deterministic terminal menuing system with panes, env management, and script running. Focus on minimal, stable, text-based only.

## Top Recommended Sources (Easy to Study & Adapt)

### 1. Official Textual Examples (Best Overall Starting Point)
- Repo: https://github.com/Textualize/textual/tree/main/examples
- Relevant patterns:
  - `dashboard.py` and layout examples — perfect for "panes of glass" (multiple containers, live updating panels).
  - Command palette examples — excellent stable menu/fuzzy-search system.
  - Log widget + streaming output examples — ideal for showing live output from subprocess or scripts.
  - Simple app structure (App + Screen + compose) is very clean and easy to copy/adapt.
- Why good for us: Mature, well-commented, MIT license. We can study the pane/layout patterns and the menu/command palette, then implement a thin custom version in our own repo so we own sovereignty.
- How to use: Clone the examples, run them locally, pick the dashboard + log + command palette pieces, and rebuild a minimal version tailored to driving GrokBuildCLI commands.

### 2. Rich + questionary / prompt_toolkit Patterns (Lighter Alternative)
- Many small GitHub repos and tutorials show "Rich dashboard + questionary menu".
- Common pattern: Use Rich Layout + Panel for panes, questionary for clean menu selection, then subprocess to run the chosen script and print output into a Rich Live display.
- Search terms that yield good copyable code: "rich python dashboard example", "questionary menu subprocess", "rich live log subprocess".
- Why useful: Extremely lightweight. If we want to avoid full Textual dependency initially, this combo gives beautiful panes + stable menu with very little code.
- Sovereignty note: Both Rich and questionary are small, pure-Python, easy to vendor if we ever want zero external deps.

### 3. Simple CLI Wrapper / Agent-Style Terminal Tools
- Look for repos that do exactly "menu that runs other CLI tools or Python scripts".
- Many internal dev tools and small "dev shell" projects on GitHub follow this pattern.
- Good search: "python terminal menu run subprocess" or "python tui wrapper for cli commands".
- Common reliable pattern seen across examples:
  1. Main loop shows menu.
  2. User picks item.
  3. Clear screen or switch to output pane.
  4. Run target (subprocess or import) and stream output.
  5. On finish, return to menu.
- This is exactly the "cycle through a series of connected scripts" we need. Very easy to copy the control flow.

### 4. Textual "ChatUI" and Dashboard Community Examples
- Several public minimal Textual apps exist that combine a menu/sidebar with a main output area and live logging.
- Pattern to steal: Sidebar menu (ListView) + main content area that swaps between "status view", "log view", and "action running" states.
- These are usually < 300 lines and very readable.

## Recommended Copy/Fork Strategy for Sovereignty
1. Study the official Textual dashboard + command palette + log examples first (highest quality, best documented).
2. Pick the layout/pane and menu routing patterns.
3. Implement our own thin `MenuApp` and `ActionRunner` classes in our repo — do not copy large chunks verbatim.
4. Keep all GrokBuildCLI driving logic in small, well-named functions (e.g. `run_seven_phase_status()`, `run_test_harness()`, `show_roster_inventory()`).
5. Use subprocess for any published CLI commands (keeps the TUI as a pure wrapper).
6. For env management: Write our own small `ensure_venv()` helper (stdlib + subprocess pip) — this is the part we must own completely for reliability.
7. Result: We get the good UX patterns without taking on someone else's full codebase. Full sovereignty maintained.

## Specific Files/Patterns Worth Looking At
- Textual examples: `examples/dashboard.py`, `examples/command_palette.py`, `examples/log.py`
- Any small "dev-tui" or "cli-dashboard" repos that use Rich Layout + Panels for multi-pane terminal apps.
- Simple questionary + Rich combo tutorials (many 100-200 line examples exist that do menu → run script → show output).

## What We Will NOT Do
- Pull in full external TUI frameworks as hard dependencies without vetting.
- Use anything that requires MCP, external bridges, or non-deterministic behavior.
- Over-complicate with agent swarms or visual DNA in the TUI itself (those stay in the image pipeline / sovereign layer).

This research gives us excellent, real-world copyable patterns for a stable menu + panes + script runner while keeping everything deterministic and under our control.

---

*Re-pushed to https://github.com/jameswilsonotr-ship-it/TUI.inhouse root on 2026-06-29. This commit serves as proof of active push.*