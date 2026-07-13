# PR-11 — Forwards-compatible Markdown/HTML menu system (PRIORITY)

**Status:** specification + **runtime landed** (`tui_chrome/menu_model.py`, MenuPackScreen)  
**Branch (suggested):** `feat/menu-system-v1`  
**Priority:** **Highest** among PR-11…15  
**Depends on:** PR-07 docs standards  
**Unblocks:** PR-12 layout · PR-13 output · PR-14 samples · PR-15 demo zip  

---

## Goal

Define and document a **forwards-compatible menuing system** that is:

- Authorable as **Markdown**, **HTML**, and **JSON**  
- Machine-validated via JSON Schema  
- Compatible with legacy zip `menu.json` (`main_script`)  
- Ready for layout (PR-12) and output windows (PR-13)

## Deliverables (this PR)

| Artifact | Status |
|----------|--------|
| [`menu-system/MENU-SYSTEM.md`](./menu-system/MENU-SYSTEM.md) | Formal human SSoT |
| [`menu-system/schema/menu.schema.json`](./menu-system/schema/menu.schema.json) | Canonical schema |
| [`menu-system/EXAMPLES.md`](./menu-system/EXAMPLES.md) | Examples index |
| [`menu-system/examples/capability-demo/`](./menu-system/examples/capability-demo/) | MD + HTML + JSON projections |
| This plan | Tracking |

### Implementation follow-up (same PR or tight sub-commit)

- [ ] `scripts/validate_menu.py` — validate pack against schema  
- [ ] `tui_chrome/menu_model.py` — load + legacy normalize  
- [ ] Unit tests: legacy → v1 normalize; schema required fields  

## Acceptance

- [x] Formal MENU-SYSTEM.md with versioning + ignore-unknown rules  
- [x] menu.schema.json in tree  
- [x] MD/HTML/JSON example pack documented  
- [x] Legacy bridge specified  
- [ ] Loader + tests (implementation phase)  

## Non-goals

- Full Textual rewrite of launcher (later PRs)  
- Approving wrap-any / 7-phase Iron Pearl product (still P-20/P-21 not approved — different IDs)  
