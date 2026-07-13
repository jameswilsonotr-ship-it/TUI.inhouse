# Output Windows Specification

**Status:** Formal specification · **PR-13**  
**Schema version:** `1.0.0`  
**Machine schema:** [`schema/window.schema.json`](./schema/window.schema.json)  
**Depends on:** [MENU-SYSTEM.md](./MENU-SYSTEM.md), [SCREEN-LAYOUT.md](./SCREEN-LAYOUT.md)  
**Invoke protocol:** [CODE-CALL-DISPLAY.md](./CODE-CALL-DISPLAY.md)

---

## 1. Purpose

Define **output windows** that receive the results of **any code** launched from menus, while adhering to the same **panel / Markdown / HTML** structure as the menu + layout schemas.

---

## 2. Window model

An **output window** is a layout **panel** with `role: output` plus stream/render configuration.

Canonical pack file (optional): `windows.json`.

```json
{
  "schema_version": "1.0.0",
  "windows": [
    {
      "id": "main_output",
      "panel": "main_output",
      "title": "Output",
      "streams": ["stdout", "stderr"],
      "render_as": "log",
      "buffer_lines": 5000,
      "markdown_safe": true,
      "html_safe": true
    }
  ]
}
```

### 2.1 Window fields

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `id` | string | yes | Referenced by `ActionSpec.output.window` |
| `panel` | string | yes | Layout panel id (usually same as `id`) |
| `title` | string | no | Chrome title |
| `streams` | enum[] | no | Default `["stdout","stderr"]` |
| `render_as` | enum | no | `log` \| `markdown` \| `html` \| `ansi` \| `json` |
| `buffer_lines` | number | no | Ring buffer size |
| `markdown_safe` | bool | no | Sanitize MD (default true) |
| `html_safe` | bool | no | Strip unsafe HTML (default true) |
| `show_exit_banner` | bool | no | Append exit code footer (default true) |
| `extensions` | object | no | Ignore-unknown |

---

## 3. Stream kinds

| Stream | Source |
|--------|--------|
| `stdout` | Process standard output (text, UTF-8) |
| `stderr` | Process standard error |
| `both` | Interleaved with tags (see CODE-CALL-DISPLAY) |
| `events` | Structured JSON lines on stdout when `TUI_EVENTS=1` |

---

## 4. Render modes (panel content_types)

| `render_as` | Display rules |
|-------------|----------------|
| `log` | Monospace append; no MD interpretation |
| `ansi` | Log + ANSI color SGR (Textual/Rich) |
| `markdown` | Buffer as MD; re-render on flush / idle; safe subset |
| `html` | Safe HTML subset (same as MENU-SYSTEM §8.2) |
| `json` | Pretty-print if valid JSON; else fall back to log |

If the process sets header line `TUI_RENDER: markdown` (see CODE-CALL-DISPLAY), host MAY override `render_as` for that run.

---

## 5. Lifecycle

1. User activates menu item with action.  
2. Host resolves `output.window` → panel.  
3. If `clear: true`, window buffer cleared.  
4. Process started per CODE-CALL-DISPLAY.  
5. Chunks appended per `stream` / `append` rules.  
6. On exit: optional banner `── exit N (level L) ──`.  
7. Window remains focusable for scroll/copy.

---

## 6. Multiple windows

Actions MAY target `aux_output` or pack-defined windows.  
Hosts without that panel MUST fall back to `main_output` with a warning.

---

## 7. Alignment with Markdown/HTML menu schema

| Menu / layout concept | Output window |
|-----------------------|---------------|
| `content_format` | Informational for help panels |
| `render_as` on action | Forces window mode for that run |
| Panel `content_types` | Intersection must include chosen mode |
| Safe HTML/MD subsets | Same allowlists as MENU-SYSTEM |

---

## 8. Related

- [CODE-CALL-DISPLAY.md](./CODE-CALL-DISPLAY.md) — **exact** call + display protocol  
- [SCREEN-LAYOUT.md](./SCREEN-LAYOUT.md)  
- [MENU-SYSTEM.md](./MENU-SYSTEM.md)  
