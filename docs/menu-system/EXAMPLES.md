# Menu system examples

**PR-11+** · See [MENU-SYSTEM.md](./MENU-SYSTEM.md)

---

## 1. Minimal v1 pack (`menu.json`)

```json
{
  "schema_version": "1.0.0",
  "id": "hello-pack",
  "title": "Hello Menu",
  "content_format": "markdown",
  "menus": [
    {
      "id": "hello",
      "label": "Say hello",
      "action": {
        "type": "run_python",
        "target": "scripts/hello.py",
        "output": { "window": "main_output", "render_as": "log", "clear": true }
      }
    }
  ]
}
```

## 2. Capability demo (target of PR-14/15)

See `docs/menu-system/examples/capability-demo/` for full tree:

| Item | Script | Notes |
|------|--------|-------|
| Wave motion | `scripts/wave.py` | ANSI/log wavy animation |
| File picker | `scripts/file_picker.py` | Path selection protocol |
| Web search | `scripts/web_search.py` | Networked sample (documented) |

## 3. Markdown frontmatter form

```markdown
---
schema_version: "1.0.0"
id: hello-pack
title: Hello Menu
menus:
  - id: hello
    label: Say hello
    action:
      type: run_python
      target: scripts/hello.py
---

# Hello Menu

Pack docs for humans.
```

## 4. Legacy zip (still valid)

```json
{
  "name": "demo-memory-processor",
  "main_script": "harness.py",
  "version": "phase1-demo"
}
```

Normalizes via MENU-SYSTEM §9.1.
