# PR-14 — Sample scripts (wave · file picker · web search)

**Status:** planned (stubs under examples; full scripts in demo pack at PR-15)  
**Branch (suggested):** `feat/sample-scripts`  
**Depends on:** **PR-13** (call/display contract)  
**Priority:** After 11–13  

---

## Goal

Ship sample Python scripts that demonstrate menu actions:

| Sample | Behavior | Output |
|--------|----------|--------|
| **Wave motion** | Animated wavy / sine pattern | `render_as: ansi` or log frames |
| **File picker** | Obtain a filesystem path | markdown result (`TUI_RENDER: markdown`) |
| **Web search** | Attempt a search over the network | markdown list of results / clear error if offline |

All scripts MUST obey [CODE-CALL-DISPLAY.md](./menu-system/CODE-CALL-DISPLAY.md).

## Deliverables

- [ ] `scripts/wave.py` (pack-relative in capability-demo)  
- [ ] `scripts/file_picker.py`  
- [ ] `scripts/web_search.py`  
- [ ] Docstrings + `--help`  
- [ ] Unit tests with mocked network for web search  

### File picker approach (1.0)

Subprocess cannot open Textual modals easily. v1 options (pick one, document):

1. **CLI prompt** on stderr + read path from stdin (host may attach), or  
2. **Arg** `--path` for non-interactive tests, or  
3. **Extension event** `TUI_EVENT: {"type":"request_file"}` if host implements (optional).

Default for samples: `--path` optional; else list cwd and pick via simple numbered prompt if TTY.

### Web search approach (1.0)

- Use **stdlib only** (`urllib`) against a documented endpoint or DuckDuckGo HTML (best-effort).  
- MUST fail gracefully with markdown error when no network.  
- MUST NOT require API keys for the sample.  
- Document that this is a **demo**, not a production search product.

## Acceptance

- [ ] Each script exits 0 on success demo path  
- [ ] Each honors `TUI_*` env when present  
- [ ] Web search does not crash offline  
- [ ] Linked from capability-demo `menu.json`  

## Non-goals

- Full browser automation  
- Guaranteed search ranking quality  
