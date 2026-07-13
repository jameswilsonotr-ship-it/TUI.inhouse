# Linting Standards (Olivia Dev) — Placeholders

**Goal**: At least **placeholders** for consistent code quality across projects. Ruff (fast, Python-native) + Black recommended. Docstring enforcement included.

**Status (per user directive)**: Begin with placeholders/config stubs + scripts. Full CI/enforcement later. Integrate into OLIV.DIVA as SSoT.

## Recommended Tools (Placeholders)
- **Ruff**: Linting + some formatting + docstring rules (pydocstyle compatible).
- **Black**: Code formatting (or ruff format).
- Optional later: mypy/pyright for types, pylint if needed.

## Placeholder Configs
See `.research/templates/`:
- `ruff.toml` — Basic rules (select lint + docstring).
- `pyproject-lint-snippet.toml` — Drop-in [tool.ruff] section.

Example ruff.toml (copy and customize per project):

```toml
# Placeholder - copy to project root
target-version = "py312"
line-length = 88

[lint]
select = ["E", "F", "I", "W", "D"]  # E/F errors, I imports, W warnings, D docstrings
ignore = ["D203", "D212"]  # common docstring style tweaks

[lint.pydocstyle]
convention = "google"  # or "numpy"

[format]
quote-style = "double"
```

Run:
```bash
ruff check .
ruff format --check .
# or ruff check --fix
```

## Integration with Enforcer / Process
- Scripts/enforcer (future enhancement) should run lint checks.
- In `.aux/plans/` reports: include "Lint passed" or list issues.
- For new work (e.g. JSON TUI in TUI/ui/): must pass placeholder checks + have docs.

## Docstrings as Lint Target
Ruff D rules + the Documentation Standards require docstrings on public API.
- Update code like `PocTestScreen`, `tui_engine.py`, launcher, skills to have them.
- Cross-ref MDs in docstrings.

## Where to Apply
- OLIV.DIVA (central templates + any scripts).
- TUI (Python + Textual).
- the.maid (cod.py etc.).
- Skills (SKILL.md + .py).
- "Wherever else necessary".

## CI / Future
- Placeholder GitHub Action snippet in templates or docs.
- "Turbo boost" CI once standardized layout solid.

## See Also
- docs/DOCUMENTATION-STANDARDS.md (separate MDs + docstrings).
- FOLDER-STANDARDS.md.
- .research/templates/ for files.
- Recent TUI JSON POC: demonstrates clean, documented, spec-driven code.

**Begin implementation**: These are the initial placeholders. Copy, adapt, run on TUI JSON work + OLIV files.