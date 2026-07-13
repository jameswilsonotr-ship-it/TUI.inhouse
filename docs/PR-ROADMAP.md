# TUI.inhouse — PR roadmap (deploy & execute)

**Updated:** 2026-07-13  
**Product root:** `/mnt/c/out/grokbuild/TUI.inhouse`  
**Monorepo pointer:** `../install-tui.sh`  
**Doc hub:** [DOC-INDEX.md](./DOC-INDEX.md)

## Open / in-flight / quality PRs

| PR | Name | Status | Plan |
|----|------|--------|------|
| **01** | One-line bootstrap (`install.sh` / ps1) | Scaffold live | [PR-01-one-line-bootstrap.md](./PR-01-one-line-bootstrap.md) |
| **02** | Error handling + recon | Partial + `scripts/recon.py` | [PR-02-error-recon.md](./PR-02-error-recon.md) |
| **03** | Launch harden + **error logs always** | Executing / landed | [PR-03-launch-error-logs.md](./PR-03-launch-error-logs.md) |
| **04** | Layout chrome (panels, borders, GUI shells) | Executing / landed | [PR-04-layout-chrome.md](./PR-04-layout-chrome.md) |
| **05** | Six-panel carousel + nested menus | Executing / landed | [PR-05-six-panel-gallery.md](./PR-05-six-panel-gallery.md) |
| **06** | ANSI/ASCII effects (strobe, glitter, sparkle) | Executing / landed | [PR-06-ansi-effects.md](./PR-06-ansi-effects.md) |
| **07** | **Strong documentation** | **Executing (in tree)** | [PR-07-strong-documentation.md](./PR-07-strong-documentation.md) |
| **08** | **Strong docstrings** | **Executing (in tree)** | [PR-08-docstrings.md](./PR-08-docstrings.md) |
| **09** | **Test harness suite** | **Executing (in tree)** | [PR-09-test-harness.md](./PR-09-test-harness.md) |
| **10** | **Distribution (wheel / wheelhouse)** | **Scaffold in tree** | [PR-10-distribution-wheel.md](./PR-10-distribution-wheel.md) |
| **11** | **Menu system MD/HTML/JSON (PRIORITY)** | **Spec + runtime** | [PR-11-menu-system-md-html.md](./PR-11-menu-system-md-html.md) |
| **12** | **Screen GUI layout structure** | **Spec + MenuPackScreen** | [PR-12-screen-gui-layout.md](./PR-12-screen-gui-layout.md) |
| **13** | **Output windows + code call/display** | **Spec + action_runner** | [PR-13-output-windows.md](./PR-13-output-windows.md) |
| **14** | **Sample scripts** (wave · picker · search) | **In demo pack** | [PR-14-sample-scripts.md](./PR-14-sample-scripts.md) |
| **15** | **Demo zip integration** (default launch) | **Landed** | [PR-15-demo-zip-integration.md](./PR-15-demo-zip-integration.md) |

### Menu platform series (priority order)

| Order | PR | One-liner | Spec hub |
|------:|----|-----------|----------|
| 1 | **11** | Forwards-compatible MD/HTML/JSON menus | [menu-system/](./menu-system/README.md) |
| 2 | **12** | Formal screen layout any menu mounts into | [SCREEN-LAYOUT.md](./menu-system/SCREEN-LAYOUT.md) |
| 3 | **13** | Output windows + exact invoke/display protocol | [CODE-CALL-DISPLAY.md](./menu-system/CODE-CALL-DISPLAY.md) |
| 4 | **14** | Sample scripts: wave, file picker, web search | [PR-14](./PR-14-sample-scripts.md) |
| 5 | **15** | Wire all into default `sample_menu.zip` | [PR-15](./PR-15-demo-zip-integration.md) |

```bash
cd /mnt/c/out/grokbuild/TUI.inhouse
python3 scripts/run_harness.py    # PR-09 — expect HARNESS OK
python3 scripts/build_dist.py     # PR-10 — wheel → dist/
python3 scripts/validate_menu.py docs/menu-system/examples/capability-demo   # PR-11
```

---

## Potential PRs — **NOT APPROVED** (design-only Iron Pearl)

> **Do not implement.** Concepts only, from `grok-tui` design docs.  
> Product PHILOSOPHY = zip-menu harness launcher, not full ops console.  
> **Requires explicit human approval** before branch, plan scaffold, or code.

| ID | Name | Status | Origin |
|----|------|--------|--------|
| **P-20** | Wrap any Python | **Potential only — not approved** | Design walkthrough Step 3 + schema `wrap_any` |
| **P-21** | 7-phase dashboard + roster | **Potential only — not approved** | Design walkthrough Step 4 + schema modules/screens |

IDs **P-20 / P-21** so they never collide with ship PRs 11–15.  
No plan files until approved.

### P-20 concept — Wrap any Python (NOT APPROVED)

**One-liner:** Point the launcher at any `.py` and run under managed deps + Textual host log.

| Piece | Intent |
|-------|--------|
| CLI / entry | `python launcher.py wrap /path/to/any_script.py` (or Wrap screen) |
| Import sniff | Regex + AST, or sibling `requirements.txt` |
| Deps | Dedicated venv or shared base |
| Host screen | Capture stdout/stderr; restart button |
| Optional later | PyInstaller/Nuitka single-file |

Overlap today: zip harnesses already run scripts with `--chunk` / exit 0/1/2.  
Wrap-any would be a **general path**, not zip-bound. **Not approved.**

### P-21 concept — 7-phase + roster (NOT APPROVED)

**One-liner:** Iron Pearl tiles for Grok Build 7-phase pipeline + Chaos Bratz roster.

| Piece | Intent |
|-------|--------|
| Home tiles | Phases, Roster, Hardware, Wrap |
| `grok_build_core` | Live 7-phase dashboard |
| `chaos_bratz_roster` | Inventory / boot actions |
| Screens | `PhaseDashboardScreen`, `RosterScreen` |

**PHILOSOPHY conflict:** shipped product is *not* a full 7-phase dashboard.  
Approval must reconcile scope first.

**Note:** Frozen single-file binary (PyInstaller/Nuitka) is **PR-10b** under distribution — not these design concepts.

---

## Where errors go (always)

| Log | Purpose |
|-----|---------|
| `logs/error.log` | Failures: bootstrap, Textual import, **uncaught launch crash** |
| `logs/bootstrap.log` | Step narrative from `install.sh` + python bootstrap |
| `logs/bootstrap_deps.log` | Raw pip |
| `logs/recon-report.md` | `python scripts/recon.py` |
| `logs/tui_crash.log` | Full traceback from last TUI crash (PR-03) |

```bash
tail -100 logs/error.log
tail -100 logs/tui_crash.log
./install-tui.sh --recon-only
python3 scripts/run_harness.py
```

## One-command after PRs

```bash
cd /mnt/c/out/grokbuild
./install-tui.sh                 # or TUI.inhouse/./install.sh
# In TUI: press G for gallery, E for effects demo, g for gutter
```
