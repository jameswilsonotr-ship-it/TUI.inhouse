# Documentation Standards (Olivia Dev)

**Applies to**: All #CODE projects (OLIV.DIVA as SSoT, TUI, the.maid, NYXELLE, skills, etc.).
**Status**: Placeholders + requirements. Heavy emphasis on **separate Markdown files** + **docstrings in code**.

## Philosophy
- Documentation is first-class (specs-led).
- Separate MD files for humans (easy to read/edit outside code).
- Docstrings in code for IDEs, introspection, and enforcement.
- Cross-reference between MDs and code (e.g. "See docs/DOCUMENTATION-STANDARDS.md").
- Build "this" (e.g. JSON TUI schema/engine) into OLIV.DIVA with full docs.

## Required Separate Markdown Files (per project root or appropriate subdir)
Every project **must** have (or link to central in OLIV.DIVA):

- `README.md` — Purpose, quick start, run/test commands, claims.
- `docs/DOCUMENTATION-STANDARDS.md` (or link) — This file.
- `docs/LINTING-STANDARDS.md` (or link).
- `TODO.md` or `docs/TODO.md` — Current tasks (timestamped).
- `SUMMARY.md` or `docs/SUMMARY.md` — High-level overview.
- `CHANGELOG.md` — History of changes.
- `docs/ARCHITECTURE.md` or `specs/architecture.md` — Component breakdown (see JSON TUI example).
- `specs/` — Specific specs (timestamped .md files).
- For UI-related: `design/tui/` or `docs/ui/` with examples.

**For OLIV.DIVA (canonical SSoT)**:
- Central copies/templates in `docs/` and `.research/templates/`.
- Heavily document new work like the JSON TUI schema here.

**JSON TUI Example (build "this" in)**:
See `design/tui/JSON-TUI-TEMPLATE.md` (or equivalent) for:
- Separate schema (`tui_component_schema.json`).
- Template (`poc_test_menu.json`) defining panels, borders, lists, buttons.
- Engine (`tui_engine.py`).
- POC: simple 1/2/3/4 list + QUIT/NEXT/ALL from JSON only (no hardcode).
- How to extend slowly.

## Code Docstrings (in-source)
- **Mandatory** for all public modules, classes, functions/methods.
- Style: Google or NumPy (consistent within project). Start with short description.
- Include: Purpose, Args, Returns, Raises, Examples (where helpful), cross-refs to MDs.
- Enforced via lint placeholders (ruff + pydocstyle rules).
- Examples from recent work:
  - Module: `"""tui_engine.py - Lightweight JSON TUI engine... See docs/..."""`
  - Class: `class PocTestScreen(Screen): """POC test screen driven 100% from JSON..."""`

Update existing code (TUI/ui/, launcher, skills/*.py) with docstrings as part of integration.

## Process
1. Before code: write/update relevant separate MD(s).
2. In code: add docstrings.
3. After edits: run enforcer (will include lint + doc checks in future).
4. Record in `.aux/plans/`.

## Enforcement (see LINTING-STANDARDS.md)
Placeholders for ruff rules that catch missing docstrings.

## See Also
- FOLDER-STANDARDS.md (requires docs/ + .research/).
- LINTING-STANDARDS.md.
- OLIV.DIVA philosophy + .research/dev-process-codified.md.
- Recent TUI JSON work in #CODE/TUI/ui/ as living example (panels composed of children, char-based, spec-driven).

**Build this into Olivia Dev**: The JSON TUI template is now part of the codified process for modular, documented, spec-first UI components.