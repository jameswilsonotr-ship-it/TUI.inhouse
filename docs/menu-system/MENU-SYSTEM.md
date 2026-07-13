# Menu System Specification (Markdown / HTML compatible)

**Status:** Formal specification · **PR-11** (priority)  
**Schema version:** `1.0.0`  
**Machine schema:** [`schema/menu.schema.json`](./schema/menu.schema.json)  
**Compatibility:** Extends (does not break) legacy zip `menu.json` from [HARNESS-CONTRACT.md](../HARNESS-CONTRACT.md)

---

## 1. Purpose

Define a **forwards-compatible** menuing system that:

1. Is authorable as **Markdown**, **HTML**, and/or **JSON** with a single logical model.  
2. Survives schema evolution (`schema_version` + ignore-unknown rules).  
3. Feeds a stable **screen layout** (PR-12) and **output windows** (PR-13).  
4. Remains usable offline, in Textual, and in future web/static renderers.

This document is the **human SSoT**. Validators should implement `menu.schema.json`.

---

## 2. Design principles

| Principle | Rule |
|-----------|------|
| **One logical model** | JSON is canonical at runtime. MD/HTML are projections / authoring forms. |
| **Forwards compatible** | Unknown fields MUST be ignored (not errors) by older loaders. |
| **Versioned** | Every document carries `schema_version` (semver string). |
| **Content portable** | Labels and help MAY be Markdown or HTML; renderers pick a safe subset. |
| **Actions explicit** | Every interactive item declares *how* it runs (not implied by filename alone). |
| **Legacy bridge** | A zip with only `main_script` remains valid (`schema_version` optional → treated as `0.9-legacy`). |

---

## 3. Document set (per menu pack)

A menu pack (directory or zip) MAY contain:

```text
menu-pack/
├── menu.json          # REQUIRED for machine load (canonical)
├── menu.md            # RECOMMENDED authoring + human view
├── menu.html          # OPTIONAL rich static/preview form
├── layout.json        # OPTIONAL until PR-12 (defaults apply)
├── windows.json       # OPTIONAL until PR-13 (defaults apply)
├── scripts/           # OPTIONAL action targets
│   └── *.py
├── assets/            # OPTIONAL images, css fragments
└── README.md          # OPTIONAL pack docs
```

**Loader order (PR-11 contract):**

1. If `menu.json` present → parse as canonical.  
2. Else if `menu.md` present → parse frontmatter + body into the logical model (emit virtual `menu.json`).  
3. Else if only legacy fields would apply → synthesize from `main_script` / zip root.  
4. `menu.html` is never required for launch; it is a projection for browsers/docs.

---

## 4. Canonical model (`menu.json`)

### 4.1 Top-level object

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `schema_version` | string | **yes** (for v1 packs) | e.g. `"1.0.0"` |
| `id` | string | yes | Stable pack id (slug) |
| `title` | string | yes | Display title (plain or MD inline) |
| `description` | string | no | Longer blurb (MD/HTML per `content_format`) |
| `content_format` | enum | no | `plain` \| `markdown` \| `html` (default `markdown`) |
| `version` | string | no | Pack version (author-defined) |
| `locale` | string | no | BCP-47, default `en` |
| `tags` | string[] | no | Search/filter tags |
| `defaults` | object | no | Default layout/window/action profiles (see §6) |
| `menus` | MenuNode[] | yes | Root menu tree (at least one node) |
| `actions` | object | no | Named action registry (id → ActionSpec) |
| `extensions` | object | no | Vendor/extension bag (ignored if unknown) |

### 4.2 MenuNode

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `id` | string | yes | Unique within pack |
| `label` | string | yes | Item text (`content_format`) |
| `help` | string | no | Longer help / tooltip |
| `kind` | enum | no | `item` \| `group` \| `separator` \| `link` (default `item`) |
| `children` | MenuNode[] | no | Nested menus when `kind=group` |
| `action` | string \| ActionSpec | no | Action id or inline ActionSpec |
| `hotkey` | string | no | e.g. `"1"`, `"g"`, `"ctrl+o"` |
| `enabled` | bool | no | Default true |
| `visible` | bool | no | Default true |
| `icon` | string | no | Emoji or asset key |
| `when` | string | no | Optional expression hook (future; ignore if unknown) |
| `extensions` | object | no | Forwards-compatible bag |

### 4.3 ActionSpec

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `type` | enum | yes | See §5 |
| `target` | string | depends | Script path, menu id, URL, builtin name |
| `args` | array \| object | no | CLI args or structured params |
| `cwd` | string | no | Relative to pack root (default `.`) |
| `timeout_sec` | number | no | Default from launcher (legacy 120) |
| `output` | OutputBinding | no | How results bind to windows (PR-13) |
| `env` | object | no | Extra env vars (string values only) |
| `confirm` | string | no | Confirmation prompt (MD) before run |
| `extensions` | object | no | Ignore-unknown |

### 4.4 OutputBinding (preview; formal in PR-13)

| Field | Type | Description |
|-------|------|-------------|
| `window` | string | Window id in layout (`main_output` default) |
| `stream` | enum | `stdout` \| `stderr` \| `both` \| `events` |
| `render_as` | enum | `log` \| `markdown` \| `html` \| `ansi` \| `json` |
| `clear` | bool | Clear window before run (default true) |
| `append` | bool | Append instead of replace (default false) |

---

## 5. Action types (`ActionSpec.type`)

| Type | `target` meaning | Code call (runtime contract) |
|------|------------------|------------------------------|
| `run_python` | Relative `.py` path in pack | `python target [args…]` with env `TUI_MENU_*` (PR-13) |
| `run_shell` | Shell command string | Explicit allowlist policy required; default **disabled** in product |
| `open_menu` | MenuNode id or pack-relative menu path | Navigate UI tree |
| `open_url` | http(s) URL | Open externally or in output window as link list |
| `builtin` | Builtin id (`gutter_toggle`, `quit`, `gallery`, …) | Host launcher API |
| `noop` | ignored | No-op / placeholder |
| `legacy_harness` | script name | **Bridge:** same as current `main_script` + `--chunk` / `--log-dir` |

Unknown `type` values: loader MUST skip the item with a warning, not crash.

---

## 6. Defaults object

```json
{
  "defaults": {
    "content_format": "markdown",
    "layout_id": "standard_menu",
    "output_window": "main_output",
    "action_timeout_sec": 120,
    "render_as": "log"
  }
}
```

Unknown default keys MUST be ignored.

---

## 7. Markdown authoring form (`menu.md`)

### 7.1 Structure

```markdown
---
schema_version: "1.0.0"
id: demo-capability-pack
title: Capability Demo Menu
version: "0.1.0"
content_format: markdown
---

# Capability Demo Menu

Human-readable intro (Markdown). Ignored for structure if `menus` is fully
defined in frontmatter; otherwise headings may map to groups (optional
authoring convenience — **canonical remains JSON**).

## Actions

Defined in frontmatter `actions` / `menus` for machine reliability.
```

### 7.2 Frontmatter fields

YAML frontmatter MUST support the same fields as `menu.json` (snake_case keys).  
If both `menu.md` and `menu.json` exist, **`menu.json` wins** at runtime; MD is documentation unless JSON is absent.

### 7.3 Markdown item sugar (optional, non-normative)

Authors MAY list items as:

```markdown
- [Wave motion](action:run_python:scripts/wave.py)
- [File picker](action:run_python:scripts/file_picker.py)
- [Web search](action:run_python:scripts/web_search.py)
```

A MD→JSON compiler (tooling) MAY convert these into MenuNodes.  
Runtime loaders are **not** required to parse body links until a later PR; formal requirement is frontmatter/JSON.

---

## 8. HTML authoring form (`menu.html`)

### 8.1 Rules

- Root element SHOULD be `<article data-tui-menu schema-version="1.0.0">`.  
- Menu structure SHOULD use:

```html
<article data-tui-menu data-schema-version="1.0.0" data-menu-id="demo-capability-pack">
  <h1 data-role="title">Capability Demo Menu</h1>
  <nav data-role="menu">
    <ul>
      <li data-item-id="wave" data-action-type="run_python" data-action-target="scripts/wave.py">
        <span data-role="label">Wave motion</span>
      </li>
    </ul>
  </nav>
  <section data-role="description"><p>…</p></section>
</article>
```

- **data-\*** attributes carry machine fields; visible HTML is human presentation.  
- Unknown tags/attributes MUST be ignored by loaders.  
- HTML is a **projection**: if `menu.json` exists, HTML need not be complete.

### 8.2 Safe HTML subset (for labels/help when `content_format=html`)

Allowed: `p`, `br`, `strong`, `em`, `code`, `pre`, `ul`, `ol`, `li`, `a` (href), `span`, `div`, `h1`–`h4`.  
Disallowed at render time: `script`, `iframe`, event handlers, `javascript:` URLs.

---

## 9. Forwards compatibility rules (normative)

1. **Ignore-unknown:** Fields not in the implemented version MUST NOT cause load failure.  
2. **schema_version:**  
   - Major bump = breaking removals/renames.  
   - Minor = additive fields.  
   - Patch = clarifications.  
3. Loaders MUST accept any `1.x.y` when implementing `1.0.0`, if they ignore unknown fields.  
4. Loaders MUST reject only when **required** fields for the declared major version are missing/invalid.  
5. Extension bags: `extensions`, `*.extensions` — namespaced keys recommended (`vendor.key`).  
6. **Deprecation:** Fields marked deprecated remain readable ≥ one minor after removal notice.

### 9.1 Legacy bridge (`0.9-legacy`)

If only the following are present (current product):

```json
{
  "name": "demo-memory-processor",
  "description": "…",
  "main_script": "harness.py",
  "version": "phase1-demo"
}
```

Normalize to v1 as:

```json
{
  "schema_version": "1.0.0",
  "id": "demo-memory-processor",
  "title": "demo-memory-processor",
  "description": "…",
  "version": "phase1-demo",
  "menus": [
    {
      "id": "root",
      "label": "Run harness",
      "action": {
        "type": "legacy_harness",
        "target": "harness.py"
      }
    }
  ]
}
```

---

## 10. Validation

| Check | Severity |
|-------|----------|
| JSON Schema draft-07/2020-12 validate against `menu.schema.json` | error |
| Duplicate MenuNode `id` | error |
| Action type unknown | warning (skip item) |
| `run_python` target outside pack root | error |
| Missing `schema_version` on new packs | warning → treat as legacy if `main_script` present |

Tooling: `scripts/validate_menu.py` (to ship with PR-11 implementation phase).

---

## 11. Security notes (normative product defaults)

- Default: only `run_python` relative to pack, `open_menu`, `builtin`, `legacy_harness`, `open_url` (http/https).  
- `run_shell` off unless config enables it.  
- No automatic network from the menu schema itself; scripts that call the network (PR-14 web search) own that risk and MUST document it.

---

## 12. Related documents

| Doc | PR | Role |
|-----|----|------|
| [SCREEN-LAYOUT.md](./SCREEN-LAYOUT.md) | 12 | Where menus mount in the GUI |
| [OUTPUT-WINDOWS.md](./OUTPUT-WINDOWS.md) | 13 | Streaming + render targets |
| [CODE-CALL-DISPLAY.md](./CODE-CALL-DISPLAY.md) | 13 | Exact invoke + display protocol |
| [EXAMPLES.md](./EXAMPLES.md) | 11 | Concrete menu pack examples |
| [../HARNESS-CONTRACT.md](../HARNESS-CONTRACT.md) | 07 | Legacy harness CLI |

---

## 13. Change log (spec)

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-07-13 | Initial formal specification (PR-11) |
