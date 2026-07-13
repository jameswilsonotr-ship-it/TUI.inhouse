# PR-08 — Strong docstrings

**Status:** executing (in tree)  
**Branch (suggested):** `feat/strong-docstrings`  
**Depends on:** PR-07 (docs exist so docstrings can cross-ref)  
**Style:** Google-ish short summary · Args / Returns / Raises when non-obvious · `See docs/…`

---

## Goal

Every **public** module, class, and non-trivial function in product code carries a docstring that:

1. States purpose in one line.  
2. Mentions side effects (TTY, subprocess, files).  
3. Cross-links `docs/API.md` or `docs/HARNESS-CONTRACT.md` when relevant.

## Scope (in)

| Area | Files |
|------|-------|
| Chrome package | `tui_chrome/*.py` |
| Bootstrap alternate | `launcher.py` |
| Minimal entry | `minimal_tui.py` |
| Main launcher public helpers | `AWESOME_LAUNCHER_OF_TUIDOOM.py` (module + public `def`s; private `_` can stay light) |

## Scope (out)

- Nested demo harness string inside `DEMO_HARNESS_CODE` (already has its own short docstring).  
- Design-only `textual_main_app_schema.py` Iron Pearl stubs (not product runtime).  
- Generated / recipe dirs (`.fork-onboarding`, etc.).

## Acceptance

- [x] `tui_chrome` package module + public APIs documented  
- [x] `load_config`, `find_menu_zips`, `extract_menu_zip`, `run_harness_once`, `run_chunked_harness`, `create_demo_menu_zip` have full docstrings  
- [x] `launcher.py` / `minimal_tui.py` module + key functions  
- [x] Docstrings reference docs paths, not invent new product scope  

## Enforcement (later)

Ruff `D` / pydocstyle optional; not required to land this PR.