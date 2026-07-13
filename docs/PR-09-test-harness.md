# PR-09 — Test harness suite

**Status:** executing (in tree)  
**Branch (suggested):** `feat/test-harness`  
**Depends on:** PR-07 (TESTING.md), PR-08 (stable public APIs)  
**Philosophy:** harness-first · stdlib unittest · no CI drama · exit codes 0/1  

---

## Goal

Automated checks for pure logic and harness contract **without** requiring a full interactive Textual session.

## Deliverables

| Path | Role |
|------|------|
| `tests/` | Unit tests (unittest) |
| `tests/test_effects.py` | ANSI / sparkle pure helpers |
| `tests/test_layouts.py` | layout mode cycle + circle_index |
| `tests/test_menus.py` | zip find / extract / demo zip / harness run |
| `tests/test_config.py` | load_config + ensure_dirs |
| `scripts/run_harness.py` | One-command runner (unit + optional product flags) |
| `docs/TESTING.md` | Operator instructions |

## Layers

1. **Unit** — no Textual App, fast, offline.  
2. **Contract** — extract demo zip, run harness with `--chunk`, expect exit 0.  
3. **Product smoke (optional)** — `python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo` only (no interactive TUI).

## Non-goals

- Full Textual pilot / screenshot CI (wishlist).  
- Approving wrap-any or 7-phase product PRs.

## Acceptance

- [x] `python scripts/run_harness.py` exits 0 on clean tree  
- [x] `python -m unittest discover -s tests -v` works with `.venv` or system Python  
- [x] Harness contract test creates temp dirs (no pollution of `.launcher_menus`)  
- [x] Documented in TESTING.md + DOC-INDEX  

## Run

```bash
cd /mnt/c/out/grokbuild/TUI.inhouse
./.venv/bin/python scripts/run_harness.py
# or
python3 scripts/run_harness.py
```
