# Code Review + Bug Report: Grok TUI Project
**Timestamp**: 2026-06-22_0837  
**Sprint**: sprint001  
**Files Reviewed**: 
- textual_main_app_schema.py (main code)
- grok_tui_design_principles.md
- grok_tui_design_principles (1).md (duplicate)
- grok_tui_implementation_walkthrough.md
- grok_build_7_phases.json (context)

**Reviewer**: Grok (auto-approved per user)  
**Methodology**: Olivia Dev Alpha — specs first, test harness based, phases/steps/bridges. High-level architecture captured before aggressive fixes. First baby step focus: structure + review + fixes on the schema (lint + commit) before any full TUI work.

**Under Absolute Liv HUB Claim • Chaos Bratz Roster • Gutter Mode Available**

---

## Executive Summary

The `Grok-TUI-Project` contains **strong design intent** aligned with modular Python TUI, Textual framework, sovereign/Olivia Dev aesthetics (C-64, Gutter Mode, Liv HUB claim), and integration with Grok Build 7-phase pipeline.

However, the **only Python code** (`textual_main_app_schema.py`) is a **partial schema/contract + stub implementation**, not a working baby step.

- **Syntax**: Clean (passes AST + py_compile).
- **Completeness**: ~30-40%. Lots of TODOs, no real screens, no launcher, no module discovery, no venv bootstrap.
- **Bugs/Issues**: Several design/code quality problems + missing functionality that would prevent it from matching the design docs or being useful.
- **Risk**: High for "first baby step" — current state would fail to launch a useful TUI or follow the walkthrough.

**Recommendation (baby step)**: 
- Treat `textual_main_app_schema.py` as the deliverable for this first step.
- Aggressively clean it: fix structural bugs, make the schema usable, add minimal runnable App + Home screen stub, add basic CSS, make it lint-clean.
- Do **not** build full TUI, launcher, or phase integration yet.
- Lint (ruff/black/pyright or equivalent), git commit the baby step.

This matches user's directive: "dont worry about the tui until the first baby step is completed and ideally linted and re committed"

---

## Alignment with Design Docs

**Good alignment**:
- Modular registration concept (ModuleRegistration).
- Screen + module separation.
- Gutter Mode reactivity (classes, toggle).
- Textual + Rich chosen.
- C-64 / sovereign flavor.
- Ties to 7-phase pipeline (from json).

**Gaps vs. docs**:
- Walkthrough emphasizes `launcher.py` (stdlib-only venv bootstrap, re-exec, module registry via REGISTERED_MODULE).
- Current schema uses different (more complex) dataclass approach. No launcher.py exists.
- No "wrap any python" yet.
- No dynamic discovery or per-module venv logic implemented.
- No actual `run_tui_screen` entry points wired.
- Design principles stress "zero path bullshit", env sniffing, texture — none present in code.

The schema is more of a "contract for later implementation" than executable baby step.

---

## Detailed Bugs, Issues & Improvements

### Critical / Will Break or Prevent Baby Step

1. **CSS_PATH points to non-existent file**
   - `CSS_PATH = "grok_tui.tcss"` at module level.
   - Textual will fail to load if the file is missing (or warn loudly).
   - **Fix**: Either remove or create a minimal .tcss with basic styles + gutter rules. For baby step, provide inline CSS or a stub file.

2. **Binding objects misused in data model**
   - `ScreenDefinition.bindings: List[Binding]`
   - Bindings are usually class-level on App/Screen: `BINDINGS = [...]`
   - Instantiating `Binding(...)` at schema definition time and storing in dicts is not how Textual works for dynamic screens.
   - The example binding "roster_inventory" has no corresponding `action_roster_inventory` defined anywhere.
   - **Fix**: Change to lightweight dicts/tuples for schema (key, action, description). Actual bindings applied in concrete Screen classes.

3. **screen_class stored as string with zero resolution**
   - `"HomeGridScreen"`, `"PhaseDashboardScreen"` etc. — never imported or instantiated.
   - No `SCREEN_REGISTRY` or `importlib` mechanism.
   - The App never pushes any screens.
   - **Fix**: Add a simple class registry or switch to actual class references in the schema for baby step (or implement minimal resolution).

4. **GrokBuildTUI is almost non-functional**
   - `on_mount` only sets title + class.
   - No `compose()`, no `push_screen()`, no home grid.
   - `action_toggle_gutter` exists but does nothing visible (no CSS).
   - No command palette implementation (binding "?" does nothing useful).
   - `__name__` block launches a blank app.
   - **Fix**: Add minimal compose + a basic Home screen class using Textual widgets. Make it actually runnable and demonstrate 1-2 "tiles".

5. **No CSS / styling for Gutter Mode or C-64 texture**
   - Relies on `.gutter-active` and `.high-heat-ruined` but no rules defined.
   - Design principles emphasize "texture".
   - **Fix**: Add a small CSS string or .tcss with borders, colors, gutter variants.

### Medium / Code Quality & Maintainability

6. **Mutation of DEFAULT_SCHEMA after construction**
   ```python
   DEFAULT_SCHEMA = TUIAppSchema()
   DEFAULT_SCHEMA.screens = { ... }
   DEFAULT_SCHEMA.modules = { ... }
   ```
   - Bad practice. Makes the "default" non-default.
   - **Fix**: Build a complete `build_default_schema()` function or pass at construction.

7. **Incomplete / missing actions and command handling**
   - `action_command_palette` referenced in BINDINGS but not implemented.
   - No routing from command palette to screens/modules.
   - **Fix**: Wire basic `self.push_screen(...)` and a simple command handler for baby step.

8. **App __init__ and schema handling**
   - `def __init__(self, schema: TUIAppSchema = DEFAULT_SCHEMA):`
   - Calling `super().__init__()` is usually fine, but Textual recommends not overriding lightly if you want watch features.
   - Schema stored but under-used.
   - **Fix**: Make schema drive more (e.g. title, status components).

9. **Module registration vs. walkthrough mismatch**
   - Walkthrough uses `REGISTERED_MODULE = {...}` + `run_tui_screen(app_context)`
   - Schema uses dataclasses with `entry_point`.
   - Inconsistent. Will cause confusion later.
   - **Fix**: For this baby step, pick one (keep schema since it's the .py file) and note the alignment needed in review.

10. **No tests, no harnesses**
    - Per Olivia Dev: "specification and test harness based coding".
    - Nothing here.
    - **Fix (minimal for baby step)**: Add a simple test file or `if __name__` smoke that at least instantiates without crash. Document in review.

### Style / Minor / Future

11. Duplicate design principles file (`(1).md`).
12. Hardcoded status bar components with emojis — cute but should be driven from schema or config.
13. No type hints on some methods, missing docstrings on key classes.
14. No error boundary, no logging pane (core for "robust").
15. `from __future__ import annotations` good.
16. The file claims to be "schema definition" but mixes in executable stub code.

---

## Other Observations (Non-Bug)

- **Strengths**: Clean dataclasses, good separation of concerns in the model, strong branding/claim in docstrings, alignment with 7-phases json.
- **Missing baby step artifacts** (per user process + olivia):
  - No `specs/` for this TUI work.
  - No state/ or kanban/.
  - No timestamped plans until this review.
  - No git history in the subfolder yet.
- The project is mostly design artifacts + one schema file. This is the right time for "first baby step".

---

## Bugs/Issues Summary Table

| # | Severity | Location | Issue | Impact |
|---|----------|----------|-------|--------|
| 1 | High | schema.py:143 | CSS_PATH non-existent | App fails/warns on start |
| 2 | High | ScreenDefinition + usage | Binding in data model | Won't work for dynamic screens |
| 3 | High | screens dict | string screen_class no loader | App can't show any defined screens |
| 4 | High | GrokBuildTUI | Mostly empty implementation | Not a usable baby step |
| 5 | Med | Gutter | No CSS rules | Toggle does nothing visible |
| 6 | Med | DEFAULT_SCHEMA | Post-init mutation | Brittle |
| 7 | Med | Actions | Missing implementations | Dead bindings |
| ... | ... | ... | ... | ... |

Full list above.

---

## Recommended Fixes for First Baby Step (Aggressive)

Focus only on making `textual_main_app_schema.py` + minimal supporting file a **linted, committed, runnable baby step**:

1. Fix CSS_PATH → provide inline CSS or create `grok_tui.tcss`.
2. Replace Binding list in schema with simple `list[tuple[str, str, str]]`.
3. Add a minimal `SCREEN_CLASSES` registry + actual tiny `HomeGridScreen` and one other stub Screen.
4. Implement basic `compose()` + push home screen.
5. Add gutter CSS classes + visual effect (simple).
6. Implement basic command palette routing or use Textual's built-in.
7. Clean DEFAULT_SCHEMA construction.
8. Add a smoke test in `__main__` or separate.
9. Run linter (see below).
10. Document that full launcher, module system, 7-phase integration is future steps.

**Do not** implement full TUI, phases, voice, hardware, etc. yet.

---

## Next Steps (per user)

- [x] 1. Sprint001 structure under tui/
- [x] 2. This timestamped review doc
- Then: Aggressively fix bugs (focus on schema.py)
- Lint + commit the first baby step
- Then (later) worry about the rest of the TUI

All under Liv HUB claim. Gutter Mode toggle ready in design.

---

**Signed**: Grok under Olivia Dev process, 2026-06-22

*This document is the first timestamped plan artifact for sprint001.*

---

## Completion of First Baby Step (post-review)

After writing this review:

- Sprint001/ created under tui/
- Git initialized in Grok-TUI-Project/
- Aggressively fixed all identified high/medium bugs in textual_main_app_schema.py:
  - Fixed Binding misuse → simple tuples
  - Fixed DEFAULT_SCHEMA mutation → build_default_schema()
  - Fixed missing runnable UI → added HomeGridScreen + compose + buttons
  - Fixed CSS_PATH bug → embedded CSS + separate .tcss stub
  - Fixed gutter not visible → CSS rules + notifications
  - Fixed incomplete actions
  - Added go_home, better notifications
- Added .gitignore
- ruff --fix + check: **All checks passed!**
- py_compile: PASS
- Smoke test (with textual installed): **Import + Instantiation PASSED**
- Committed in project git: `aea49aa` "sprint001 baby step..."

**Baby step complete, linted, and re-committed.**

Do not expand into full TUI / phases / launcher until next steps / more specs provided.

Ready for next markdown or directive.

---

**RELOCATED (2026-06-22)**: This review and the fixed baby step work gathered from old tui/Grok-TUI-Project + sprint001 to #CODE/TUI/ (CONCEPTSS as user-introduced canonical design).
See new structure, the.maid, OLIV.DIVA/SSoT_INDEX.md .
Old archived (not deleted).
New confined Grok sessions from #CODE/TUI/ .
