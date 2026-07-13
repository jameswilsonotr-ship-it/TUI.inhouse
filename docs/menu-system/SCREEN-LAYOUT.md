# Screen GUI Layout Structure

**Status:** Formal specification · **PR-12**  
**Schema version:** `1.0.0`  
**Machine schema:** [`schema/layout.schema.json`](./schema/layout.schema.json)  
**Depends on:** [MENU-SYSTEM.md](./MENU-SYSTEM.md) (PR-11)

---

## 1. Purpose

Define a **formal screen / GUI layout structure** that **any menu pack** can mount into—without hard-coding Textual widgets in each menu.

Goals:

- Stable **regions** and **panels** with roles.  
- Compatible with Markdown/HTML **content slots** from the menu system.  
- Same structure describes terminal (Textual) *and* future HTML shells.  
- Forwards compatible (`schema_version`, ignore-unknown).

---

## 2. Core concepts

| Term | Meaning |
|------|---------|
| **Screen** | One full UI state (e.g. “menu home”, “running action”). |
| **Layout** | Named arrangement of regions/panels (`layout_id`). |
| **Region** | Named area of the screen (`header`, `nav`, `main`, `output`, `footer`, …). |
| **Panel** | A windowed unit inside a region (title, chrome, content type). |
| **Slot** | Named content bind point (`menu_tree`, `item_help`, `main_output`, …). |

Any menu pack MAY ship `layout.json`. If absent, host uses **`standard_menu`** built-in layout.

---

## 3. Canonical `layout.json`

```json
{
  "schema_version": "1.0.0",
  "id": "standard_menu",
  "title": "Standard menu + output",
  "orientation": "vertical",
  "regions": [ … ],
  "panels": [ … ],
  "bindings": [ … ],
  "extensions": {}
}
```

### 3.1 Top-level

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `schema_version` | string | yes | Layout schema semver |
| `id` | string | yes | `layout_id` referenced from menu `defaults.layout_id` |
| `title` | string | no | Human name |
| `orientation` | enum | no | `vertical` \| `horizontal` (root flex) |
| `regions` | Region[] | yes | Ordered regions |
| `panels` | Panel[] | yes | Panel definitions |
| `bindings` | SlotBinding[] | no | Slot → panel wiring |
| `css_hints` | object | no | Non-normative theme hints |
| `extensions` | object | no | Ignore-unknown |

### 3.2 Region

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `id` | string | yes | e.g. `header`, `body`, `footer` |
| `role` | enum | yes | See §4 |
| `size` | string | no | `auto` \| `fr:N` \| `rows:N` \| `cols:N` \| `percent:N` |
| `panels` | string[] | yes | Ordered panel ids in this region |
| `visible` | bool | no | Default true |

### 3.3 Panel

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `id` | string | yes | Stable id |
| `title` | string | no | Chrome title (MD/plain) |
| `role` | enum | yes | `chrome` \| `menu` \| `content` \| `output` \| `status` \| `dialog` |
| `content_types` | string[] | no | Allowed: `markdown`, `html`, `plain`, `log`, `ansi`, `widget` |
| `default_content_type` | string | no | Default render mode |
| `scroll` | bool | no | Default true for output |
| `focusable` | bool | no | Default true for menu/output |
| `min_size` | number | no | Rows/cols hint |
| `border` | enum | no | `none` \| `single` \| `heavy` \| `double` |
| `gutter_reactive` | bool | no | Participate in Gutter Mode chrome |
| `extensions` | object | no | Ignore-unknown |

### 3.4 SlotBinding

| Field | Type | Description |
|-------|------|-------------|
| `slot` | string | Logical slot name (see §5) |
| `panel` | string | Panel id |
| `priority` | number | Optional conflict resolution |

---

## 4. Region roles (normative set)

| Role | Purpose |
|------|---------|
| `header` | App/menu title, branding |
| `navigation` | Menu tree / list / buttons |
| `main` | Primary content / help / forms |
| `output` | Streams from actions (PR-13) |
| `status` | Status line / heat / messages |
| `footer` | Keybindings help |
| `modal` | Overlays (confirm, file picker host) |
| `extension` | Unknown host regions — ignore if unimplemented |

Hosts MUST implement at least: `header`, `navigation`, `output`, `footer`.

---

## 5. Standard slots (normative names)

| Slot | Typical panel role | Filled by |
|------|--------------------|-----------|
| `app_title` | chrome | Host + menu `title` |
| `menu_tree` | menu | MenuNode tree |
| `item_help` | content | Selected item `help` / description |
| `main_output` | output | Action streams (default) |
| `aux_output` | output | Secondary stream |
| `status_line` | status | Host messages |
| `key_help` | chrome | Bindings |

Menus bind actions via `output.window` → panel id **or** slot name (host resolves slot → panel).

---

## 6. Built-in layout: `standard_menu`

```text
┌──────────────────────────────────────────────┐
│ header: app_title                            │
├─────────────────┬────────────────────────────┤
│ navigation:     │ main: item_help            │
│  menu_tree      │                            │
│                 ├────────────────────────────┤
│                 │ output: main_output        │
│                 │ (scroll, log/md/html)      │
├─────────────────┴────────────────────────────┤
│ footer: key_help                             │
└──────────────────────────────────────────────┘
```

JSON for this layout ships as `docs/menu-system/examples/layout.standard_menu.json` and as host default.

---

## 7. Relationship to Textual (implementation note)

PR-12 **does not require** every menu to import Textual. Host maps:

| Spec | Textual mapping (informative) |
|------|-------------------------------|
| Region vertical stack | `Vertical` |
| Region horizontal | `Horizontal` |
| Panel | bordered container + `Static` / `Log` / `RichLog` / custom |
| `menu_tree` | `ListView` / `Tree` / `OptionList` |
| `main_output` | `RichLog` or `Log` (PR-13) |

Other hosts (HTML) map panels to `<section data-panel-id=…>`.

---

## 8. Forwards compatibility

Same rules as MENU-SYSTEM: ignore-unknown fields; major version for breaks; minor for additive regions/roles.

Hosts MUST tolerate unknown `role` values by hiding that region or treating as `extension`.

---

## 9. Related

- [MENU-SYSTEM.md](./MENU-SYSTEM.md)  
- [OUTPUT-WINDOWS.md](./OUTPUT-WINDOWS.md)  
- [CODE-CALL-DISPLAY.md](./CODE-CALL-DISPLAY.md)  
