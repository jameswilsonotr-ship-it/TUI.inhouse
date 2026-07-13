# Code Call & Display Protocol

**Status:** Formal specification · **PR-13**  
**Version:** `1.0.0`  
**Depends on:** [MENU-SYSTEM.md](./MENU-SYSTEM.md), [OUTPUT-WINDOWS.md](./OUTPUT-WINDOWS.md)

This document defines **exactly** how menu-driven code is **invoked** and **displayed**.

---

## 1. Scope

Applies to action types:

- `run_python` (primary)  
- `legacy_harness` (bridge to existing zip harnesses)  
- `run_shell` (only if host enables; same stream rules)

Does **not** define GUI chrome beyond binding streams → windows.

---

## 2. Working directory & path rules

| Rule | Value |
|------|--------|
| Pack root | Directory of extracted menu pack / zip |
| Default cwd | Pack root (`ActionSpec.cwd` default `.`) |
| Script path | `target` MUST resolve under pack root after normalization (no `..` escape) |
| Python | Host `sys.executable` (venv interpreter after bootstrap) |

---

## 3. Environment variables (normative)

Host MUST set:

| Variable | Example | Meaning |
|----------|---------|---------|
| `TUI_MENU_SCHEMA` | `1.0.0` | Menu schema version loaded |
| `TUI_MENU_ID` | `demo-capability-pack` | Pack id |
| `TUI_ITEM_ID` | `wave` | MenuNode id |
| `TUI_ACTION_TYPE` | `run_python` | Action type |
| `TUI_OUTPUT_WINDOW` | `main_output` | Target window id |
| `TUI_RENDER_AS` | `log` | Initial render mode |
| `TUI_PACK_ROOT` | absolute path | Pack root |
| `TUI_LOG_DIR` | absolute path | Host log directory for this run |
| `TUI_SESSION_ID` | stamp | Correlates logs |
| `PYTHONUNBUFFERED` | `1` | Recommended always |

Host MAY set:

| Variable | Meaning |
|----------|---------|
| `TUI_EVENTS` | `1` if host requests structured events |
| `TUI_COLOR` | `0`\|`1` |
| `TUI_CHUNK` | ISO date when bridging legacy harness |

Scripts SHOULD prefer these over inventing parallel conventions.

---

## 4. Invocation (run_python)

### 4.1 Command vector

```text
[sys.executable, <absolute-or-pack-relative-script>, *argv]
```

Where `argv` is built from `ActionSpec.args`:

- If `args` is an **array**: each element stringified as its own argv entry.  
- If `args` is an **object**: stable flag form `--key value` for each key (bool true → `--key`, false omitted; null skipped).  
- Host MAY prepend reserved flags only if documented in a minor schema bump.

### 4.2 Example

Action:

```json
{
  "type": "run_python",
  "target": "scripts/wave.py",
  "args": { "frames": 40, "width": 48 },
  "output": {
    "window": "main_output",
    "stream": "both",
    "render_as": "ansi",
    "clear": true
  }
}
```

Becomes:

```bash
python scripts/wave.py --frames 40 --width 48
# cwd = pack root
```

### 4.3 legacy_harness bridge

Same as [HARNESS-CONTRACT.md](../HARNESS-CONTRACT.md):

```bash
python <main_script> [--chunk DATE] --log-dir <TUI_LOG_DIR>
```

Displayed with `render_as: log` unless overridden.

---

## 5. Exit codes (display mapping)

| Process exit | Host `exit_level` | UI treatment |
|-------------:|------------------:|--------------|
| 0 | 0 | Success banner (optional green) |
| 2 | 2 | Partial / warning |
| other | 1 | Error (stderr emphasized) |
| timeout | 1 | Error + `TIMEOUT` line |

Timeout default: `ActionSpec.timeout_sec` or host default (120).

---

## 6. Display protocol (stdout/stderr → window)

### 6.1 Framing

Host reads stdout/stderr as **UTF-8 text** (replace errors).  
Chunks are appended in arrival order. When `stream=both`, lines SHOULD be tagged:

```text
[out] …
[err] …
```

unless `render_as` is `ansi` and colors already distinguish (host choice; document in UI).

### 6.2 Control lines (optional, script → host)

Scripts MAY emit **first-line or any-line** control directives on stdout:

| Line | Meaning |
|------|---------|
| `TUI_RENDER: markdown` | Switch window to markdown for rest of run |
| `TUI_RENDER: html` | Switch to html |
| `TUI_RENDER: log` | Switch to log |
| `TUI_RENDER: ansi` | Switch to ansi |
| `TUI_RENDER: json` | Switch to json |
| `TUI_TITLE: <text>` | Set window title for this run |
| `TUI_CLEAR` | Clear window mid-run |
| `TUI_EVENT: <json-object>` | Structured event (also when `TUI_EVENTS=1`) |

Control lines MUST NOT be shown raw if recognized (strip before display).  
Unknown `TUI_*` lines: show as log text (forwards compatible).

### 6.3 Structured events

When `TUI_EVENTS=1`, scripts SHOULD print JSON lines:

```json
{"type":"progress","pct":40,"msg":"frame 16"}
{"type":"result","path":"/tmp/x"}
{"type":"error","msg":"…"}
```

Host MAY render progress in `status_line` slot and body in output window.

### 6.4 Finalization

After process end, host appends (if `show_exit_banner`):

```text
── exit 0 · level 0 · 1.23s ──
```

---

## 7. How authors should write scripts

### 7.1 Minimal

```python
#!/usr/bin/env python3
"""Demo script — print to stdout for main_output."""
import sys

def main() -> int:
    print("Hello from menu action")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### 7.2 Markdown output

```python
print("TUI_RENDER: markdown")
print("# Result\n\n- item **one**\n- item two")
```

### 7.3 Interactive note

Menus run scripts as **subprocesses**, not in-process widgets.  
True interactive TUI (Textual apps) SHOULD use `builtin` host APIs or a future `type: run_textual` (not in 1.0).  
File pickers in PR-14 either:

- use a **host builtin** action, or  
- print a path result to stdout after a simple prompt protocol, or  
- emit `TUI_EVENT` asking host to open modal (extension; optional).

---

## 8. Failure display

| Failure | Window content |
|---------|----------------|
| Script not found | `[err] script not found: …` exit 1 |
| Path escape | `[err] target outside pack root` exit 1 |
| Non-zero exit | Streams + error banner |
| Decode errors | Replacement chars; continue |

---

## 9. Conformance checklist (host)

- [ ] Sets env vars in §3  
- [ ] Resolves target under pack root  
- [ ] Honors `output.clear` / `append` / `window` / `render_as`  
- [ ] Maps exit codes per §5  
- [ ] Recognizes control lines in §6.2  
- [ ] Falls back safely on unknown render modes  
- [ ] Does not execute `run_shell` unless configured  

---

## 10. Related

- [OUTPUT-WINDOWS.md](./OUTPUT-WINDOWS.md)  
- [HARNESS-CONTRACT.md](../HARNESS-CONTRACT.md)  
- Sample scripts: PR-14 (`scripts/samples/` in demo pack)  
