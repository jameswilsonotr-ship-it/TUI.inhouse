# PR-13 — Output windows + code call/display protocol

**Status:** specification + **runtime landed** (`tui_chrome/action_runner.py` → Log output window)  
**Branch (suggested):** `feat/output-windows-v1`  
**Depends on:** **PR-11**, **PR-12**  
**Unblocks:** PR-14 (samples need a contract to write against)

---

## Goal

1. **Output windows** that receive stdout/stderr/events from any menu-run code.  
2. Windows adhere to the **panel + MD/HTML** structure (layout schema).  
3. **Exact** definition of how code is **called** and **displayed**.

## Deliverables

| Artifact | Status |
|----------|--------|
| [`menu-system/OUTPUT-WINDOWS.md`](./menu-system/OUTPUT-WINDOWS.md) | Window model |
| [`menu-system/CODE-CALL-DISPLAY.md`](./menu-system/CODE-CALL-DISPLAY.md) | Invoke + display protocol |
| [`menu-system/schema/window.schema.json`](./menu-system/schema/window.schema.json) | Schema |

### Implementation follow-up

- [ ] Subprocess runner binding ActionSpec → window  
- [ ] Control lines (`TUI_RENDER:`, `TUI_EVENT:`, …)  
- [ ] Env vars `TUI_MENU_*` / `TUI_PACK_ROOT` / `TUI_LOG_DIR`  
- [ ] Tests: mock script exit codes + render switch  

## Acceptance

- [x] Stream/render modes defined  
- [x] argv/env/cwd/exit rules defined  
- [x] Control-line protocol defined  
- [ ] Runtime runner + tests  

## Security

- `run_shell` off by default  
- Paths confined to pack root  
