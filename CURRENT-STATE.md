# CURRENT STATE — TUI.inhouse

> ## NEXT SESSION: READ THIS FILE FIRST
>
> **Do not skip.** Open this file before coding, deploying, or re-exploring the tree.  
> Path: `/mnt/c/out/grokbuild/TUI.inhouse/CURRENT-STATE.md`  
> (Windows: `C:\out\grokbuild\TUI.inhouse\CURRENT-STATE.md`)  
>
> Operator intent when this was written: **come back and actually deploy this thing.**

**Written:** 2026-07-13  
**Product version (CHANGELOG):** 0.1.8 (menu platform runtime + PR-15 demo)  
**Target:** AWESOME LAUNCHER OF TUI DOOM + v1 menu platform  

---

## Where we are (one paragraph)

The **product runs**. Bootstrap → Textual App → default **capability demo** zip → **Menu UI** (`MenuPackScreen`) can run sample scripts (wave / file picker / web search / legacy harness) into an output window. Formal specs exist for menus (MD/HTML/JSON), layout, and code-call/display. Distribution is **scaffolded** (wheel builds) but **not fully production-deployed** (no clean-venv CI gate, package-data paths still a known gap). Full recipe documentation passes **A–E/5 + 6** exist in **basic** (main tree) and **medium** (clones section), and those docs are archived in a zip on **`C:\`**.

**Next workstream:** **deploy** (ship path: install story + wheel/smoke + whatever “production” means for this bunker) — not more unscoped redesign.

---

## Process position (checklist)

| Stage | Status | Notes |
|-------|--------|--------|
| Core launcher (zip menus, Gutter, gallery, effects) | **Done** | `AWESOME_LAUNCHER_OF_TUIDOOM.py` + `tui_chrome/*` |
| PR-07…09 docs / docstrings / harness | **Done** | 33 tests, `scripts/run_harness.py` |
| PR-10 wheel distribution | **Scaffold** | `pyproject.toml`, `build_dist.py` — wheel builds; clean install path incomplete |
| PR-11 menu system (spec + runtime) | **Done** | `menu_model.py` + `docs/menu-system/` |
| PR-12 screen layout | **Spec + partial UI** | Spec full; MenuPackScreen uses fixed compose (layout.json not fully driving UI) |
| PR-13 output windows + call/display | **Done** | `action_runner.py` + Log panel |
| PR-14 sample scripts | **Done** | In capability-demo examples |
| PR-15 default demo zip | **Done** | Auto-create + auto-open Menu UI |
| Recipes A B C D E(5) + 6 **basic** | **Done** | `.fork-onboarding/` … `.codebase-pass/` |
| Same recipes **medium** (clone) | **Done** | `clones/TUI.inhouse-medium/` |
| Recipe results zip on `C:\` | **Done** | See “Archives” below |
| **Deploy / production cut** | **NOT STARTED** | **← you are here next** |

---

## What “deploy” should mean next (suggested)

Pick explicitly at session start; do not invent a new product:

1. **Local deploy (minimum):** reliable `./install.sh` / `install-tui.sh` on this machine; demo Menu UI works cold.  
2. **Wheel deploy:** `python scripts/build_dist.py` → clean venv `pip install dist/*.whl` → `awesome-tui` works (fix package-data paths if broken).  
3. **GitHub deploy:** clean PR of product paths only (exclude inventory noise); tag/release.  
4. **Hardening from Recipe C/D (optional same track):** zip-slip sanitization, layout.json → UI, path resolve for wheel.

**Do not** by default implement P-20 wrap-any or P-21 Iron Pearl 7-phase (not approved).

---

## How to run (today)

```bash
cd /mnt/c/out/grokbuild/TUI.inhouse   # or C:\out\grokbuild\TUI.inhouse

# Tests
python scripts/run_harness.py          # expect: HARNESS OK · 33 tests

# Demo zip + launch
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
python AWESOME_LAUNCHER_OF_TUIDOOM.py
# UI: m = Menu UI · Wave / File picker / Web search / Legacy harness · Enter = Run

# Monorepo one-liner
# from grokbuild: ./install-tui.sh
```

---

## Critical paths (code)

| Role | Path |
|------|------|
| Entry | `AWESOME_LAUNCHER_OF_TUIDOOM.py` |
| Menu load | `tui_chrome/menu_model.py` |
| Run actions | `tui_chrome/action_runner.py` |
| Menu UI | `tui_chrome/menu_screen.py` |
| Specs | `docs/menu-system/README.md` |
| Validate pack | `scripts/validate_menu.py` |
| Wheel build | `scripts/build_dist.py` · `pyproject.toml` · `awesome_tui/` |
| Roadmap | `docs/PR-ROADMAP.md` |
| TODO | `TODO.md` |
| Philosophy | `PHILOSOPHY.md` |

**Design stubs (not the ship UI):** `textual_main_app_schema.py`, `minimal_tui.py`, sibling `../grok-tui/`.

---

## Recipe / process artifacts

### Basic pass (main tree)

| Path | Content |
|------|---------|
| `.recipes-ABCDE6-basic/README.md` | Umbrella index |
| `.fork-onboarding/` | Recipe A |
| `.messy-tree-pass/` | Recipe B |
| `.before-change/menu-platform-hardening/` | Recipe C (**plan only** — next implement track) |
| `.security-quality-pass/` | Recipe D (findings; zip-slip **S2** noted) |
| `.vision-spec-plan/` | Recipe E = Recipe 5 |
| `.codebase-pass/` | Recipe 6 |

### Medium pass (clones section)

| Path | Content |
|------|---------|
| `/mnt/c/out/grokbuild/clones/TUI.inhouse-medium/` | Synced snapshot + medium recipe trees |
| `…/.recipes-ABCDE6-medium/README.md` | Medium umbrella |
| `/mnt/c/out/grokbuild/clones/README.md` | Clones hub |

### Archives on `C:\` (recipe docs only)

| File | Role |
|------|------|
| `C:\TUI.inhouse-recipes-ABCDE6-basic-and-medium-20260713.zip` | Main archive (QUICKSTART + basic/ + medium/) |
| `C:\TUI.inhouse-recipes-ABCDE6-basic-and-medium-20260713.zip.gz` | Gzip of that zip |
| `C:\TUI.inhouse-recipes-ABCDE6-basic-and-medium-20260713-compressed.zip` | Outer zip (zip + gz + QUICKSTART) |

Also under `/mnt/c/out/grokbuild/`.

---

## Known gaps before “real” deploy

1. **Wheel / site-packages paths** for config + `grok_tui.tcss` after `pip install`.  
2. **`layout.json` not fully driving** MenuPackScreen compose.  
3. **Zip-slip** sanitization on extract (security S2).  
4. **Dirty git tree** — product vs inventory-skeleton noise; ship needs a clean PR shape.  
5. **No CI** harness gate yet.  
6. Recipe **C plan** not implemented (by design until deploy session).

---

## Session start script (for the next agent / you)

```text
1. Read CURRENT-STATE.md (this file)
2. Skim docs/PR-ROADMAP.md + TODO.md
3. Confirm deploy target: local | wheel | GitHub | harden-first
4. Run: python scripts/run_harness.py
5. Only then change code or cut a release
```

---

## Open questions for deploy session

- [ ] Deploy = this machine only, or also GitHub release?  
- [ ] Must wheel work offline (wheelhouse)?  
- [ ] Implement Recipe C P0 items (zip-slip + paths) before announce?  
- [ ] Tag version (e.g. 0.2.0) after deploy smoke?

---

## One-line for the next chat

> “Read `TUI.inhouse/CURRENT-STATE.md` — we’re past recipes and menu runtime; **start deploy** (local/wheel/GitHub). Don’t re-onboard from zero.”

---

*End of handoff. Leave this file at the TUI folder root. Update the date and checklist when deploy advances.*
