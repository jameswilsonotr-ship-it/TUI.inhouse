# PR-07 — Strong documentation

**Status:** executing (in tree)  
**Branch (suggested):** `feat/strong-documentation`  
**Depends on:** product core (PR-01…06 behavior stable enough to describe)  
**Philosophy:** specs-first · separate MDs for humans · no bloat · cross-link to code

---

## Goal

Make the launcher **documentable without reading 1.6k lines of Python**.  
Operators, agents, and future PRs should open `docs/` first.

## Deliverables

| Artifact | Purpose |
|----------|---------|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Components, data flow, entrypoints |
| [`HARNESS-CONTRACT.md`](./HARNESS-CONTRACT.md) | Zip / `menu.json` / harness CLI contract |
| [`TESTING.md`](./TESTING.md) | How to run unit + product harnesses |
| [`API.md`](./API.md) | Public modules map (`tui_chrome`, launcher helpers) |
| [`DOC-INDEX.md`](./DOC-INDEX.md) | Single table of all human docs |
| Root `README.md` / `SUMMARY.md` / `docs/README.md` | Point at index + test commands |

## Non-goals

- No new product features.
- Does **not** approve design-only P-20 wrap-any or P-21 7-phase+roster.

## Acceptance

- [x] DOC-INDEX lists architecture, harness, testing, API, PR roadmap  
- [x] ARCHITECTURE describes real entrypoints (AWESOME, install, tui_chrome)  
- [x] HARNESS-CONTRACT matches `run_harness_once` / demo zip behavior  
- [x] TESTING documents `scripts/run_harness.py` and `python -m unittest`  
- [x] QUICKSTART / README mention docs + tests  

## See also

- [DOCUMENTATION-STANDARDS.md](./DOCUMENTATION-STANDARDS.md)  
- [PR-08-docstrings.md](./PR-08-docstrings.md)  
- [PR-09-test-harness.md](./PR-09-test-harness.md)  
