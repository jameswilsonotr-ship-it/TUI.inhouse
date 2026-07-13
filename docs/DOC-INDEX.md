# Documentation index — TUI.inhouse

**Updated:** 2026-07-13  
**Product:** AWESOME LAUNCHER OF TUI DOOM (zip-menu Textual launcher)

Start here if you are new. Code without docs is incomplete (see DOCUMENTATION-STANDARDS).

> **Returning session / deploy:** read **[`../CURRENT-STATE.md`](../CURRENT-STATE.md) first.**

---

## Operator path (run it)

| Doc | Why |
|-----|-----|
| [../CURRENT-STATE.md](../CURRENT-STATE.md) | **Process handoff — read first next session** |
| [../QUICKSTART.md](../QUICKSTART.md) | Install + keys + crash logs |
| [../README.md](../README.md) | What it is + one-command |
| [../PHILOSOPHY.md](../PHILOSOPHY.md) | Why zip menus, not full ops console |
| [TESTING.md](./TESTING.md) | Unit + harness runner |
| [DISTRIBUTION.md](./DISTRIBUTION.md) | Wheel / wheelhouse install (PR-10) |
| [menu-system/README.md](./menu-system/README.md) | **Menu platform** PR-11…15 (MD/HTML menus, layout, output) |

## Engineering path (change it)

| Doc | Why |
|------|-----|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Entrypoints, packages, data flow |
| [API.md](./API.md) | Public modules / helpers |
| [HARNESS-CONTRACT.md](./HARNESS-CONTRACT.md) | Zip / menu.json / harness CLI |
| [DOCUMENTATION-STANDARDS.md](./DOCUMENTATION-STANDARDS.md) | MD + docstring rules |
| [LINTING-STANDARDS.md](./LINTING-STANDARDS.md) | Lint placeholders |
| [PR-ROADMAP.md](./PR-ROADMAP.md) | Real PRs + **not-approved** concepts |

## PR plans (07–15 ship)

### Quality / distribution (07–10)

| PR | Name | Plan |
|----|------|------|
| **07** | Strong documentation | [PR-07-strong-documentation.md](./PR-07-strong-documentation.md) |
| **08** | Docstrings | [PR-08-docstrings.md](./PR-08-docstrings.md) |
| **09** | Test harness | [PR-09-test-harness.md](./PR-09-test-harness.md) |
| **10** | Distribution (wheel / wheelhouse) | [PR-10-distribution-wheel.md](./PR-10-distribution-wheel.md) · [DISTRIBUTION.md](./DISTRIBUTION.md) |

### Menu platform (11–15)

| PR | Name | Plan |
|----|------|------|
| **11** | Menu system MD/HTML (**priority**) | [PR-11-menu-system-md-html.md](./PR-11-menu-system-md-html.md) |
| **12** | Screen GUI layout | [PR-12-screen-gui-layout.md](./PR-12-screen-gui-layout.md) |
| **13** | Output windows + call/display | [PR-13-output-windows.md](./PR-13-output-windows.md) |
| **14** | Sample scripts | [PR-14-sample-scripts.md](./PR-14-sample-scripts.md) |
| **15** | Demo zip integration | [PR-15-demo-zip-integration.md](./PR-15-demo-zip-integration.md) |

## Design archives (not product SSoT)

These live in-repo for history; product PHILOSOPHY may **diverge**:

- `../grok_tui_design_principles.md`
- `../grok_tui_implementation_walkthrough.md`
- `../textual_main_app_schema.py` (Iron Pearl baby-step stubs)
- Sibling design nest: `../grok-tui/` (monorepo)

**Not approved product work:** wrap-any (P-20), 7-phase+roster (P-21) — see PR-ROADMAP.

## Logs (always)

| File | Purpose |
|------|---------|
| `logs/error.log` | Failures |
| `logs/tui_crash.log` | Uncaught TUI crash traceback |
| `logs/bootstrap.log` / `bootstrap_deps.log` | Install narrative / pip |
