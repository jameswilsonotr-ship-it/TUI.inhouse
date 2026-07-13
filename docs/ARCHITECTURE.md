# Architecture — TUI.inhouse

**Updated:** 2026-07-13 · **PR-07**  
**Product:** AWESOME LAUNCHER OF TUI DOOM v0.1.x  
**Scope:** Zip-packaged menu launcher with Textual chrome — **not** a full Grok Build 7-phase console.

---

## Entrypoints

```text
install.sh / install.ps1 / run.cmd
        │
        ▼
AWESOME_LAUNCHER_OF_TUIDOOM.py     ← primary product
        │  bootstrap (stdlib): env → venv → deps → re-exec
        │  S1…S6 loading sequence
        ▼
Textual App (zip menus, gallery, gutter, record/replay)
        │
        ├── tui_chrome/bootstrap_stage.py   Stage A/B theater
        ├── tui_chrome/menu_intake.py       Olivia locate / picker / demo
        ├── tui_chrome/gallery.py           6-panel + nested menus
        ├── tui_chrome/effects.py           ANSI sparkle/strobe (stdlib)
        ├── tui_chrome/layouts.py           LAYOUT_MODES + mount_layout
        └── tui_chrome/native_dialog.py     OS file dialogs

launcher.py          lighter bootstrap (prefer AWESOME for full UX)
minimal_tui.py       minimal Textual alternate
```

Monorepo pointer: `../install-tui.sh` → this tree’s `install.sh`.

---

## Runtime data flow

```text
LAUNCHERCONFIG.JSON
        │
        ▼
load_config() → ensure_dirs() → find_menu_zips()
        │
        ▼
extract_menu_zip() → menus_dir/<name>/
        │                menu.json → main_script
        ▼
run_harness_once() / run_chunked_harness()
        │  subprocess: python harness.py --chunk … --log-dir …
        ▼
logs/  (processing, error, run_summary from harness)
sessions/  (optional record/replay JSON)
```

See [HARNESS-CONTRACT.md](./HARNESS-CONTRACT.md).

---

## Package boundaries

| Package / file | Responsibility | Import weight |
|----------------|----------------|---------------|
| `AWESOME_LAUNCHER_OF_TUIDOOM.py` | Bootstrap + zip runner + main App | Heavy after venv |
| `tui_chrome.effects` | Pure string effects | **stdlib only** |
| `tui_chrome.layouts` | Layout mode ids + mount helpers | Light (Textual types injected) |
| `tui_chrome.gallery` | Gallery / effects screens | Textual |
| `tui_chrome.menu_intake` | Menu locate UX | Textual |
| `tui_chrome.bootstrap_stage` | Pre-TUI install theater | stdlib + subprocess |
| `tui_chrome.native_dialog` | OS dialogs | optional Tk / PS / zenity |
| `textual_main_app_schema.py` | **Design stub only** — not wired as product app | Design |

---

## Config & on-disk sprawl

| Path | Role |
|------|------|
| `LAUNCHERCONFIG.JSON` | Search paths, dirs, demo names |
| `.venv/` | Isolated textual/rich |
| `.launcher_menus/` | Extracted menu trees |
| `logs/` | Bootstrap + errors + crash |
| `sessions/` | Recordings |
| `sample_menu.zip` | Demo pack (`--create-demo`) |

---

## Keys (product chrome)

| Key | Action |
|-----|--------|
| `g` | Toggle Gutter |
| `G` | Gallery 6-panel |
| `E` | Effects demo |
| `ctrl+q` | Quit |
| Double Ctrl-C | Force kill (`os._exit`) |

---

## Design vs product

| Design nest (`grok-tui`) | This product |
|--------------------------|--------------|
| Module registry + Iron Pearl home | Zip menus + harness CLI |
| Wrap-any / 7-phase / roster tiles | **Not approved** (see PR-ROADMAP P-20/P-21) |
| Schema-driven `GrokBuildTUI` | AWESOME App + `tui_chrome` |

---

## Related

- [API.md](./API.md)  
- [TESTING.md](./TESTING.md)  
- [DOC-INDEX.md](./DOC-INDEX.md)  
- [../PHILOSOPHY.md](../PHILOSOPHY.md)  
