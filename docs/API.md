# API map — public modules

**Updated:** 2026-07-13 · **PR-07 / PR-08**  
Docstrings in code are SSoT for signatures; this file is the **map**.

---

## `tui_chrome` package

| Module | Public focus |
|--------|----------------|
| `tui_chrome.effects` | `strip_ansi`, `strobe_frame`, `glitter_line`, `sparkle_field`, `banner_crawl`, `gutter_banner`, `ascii_box`, `effect_demo_frames`, `panel_effect_text` |
| `tui_chrome.layouts` | `LAYOUT_MODES`, `PanelSpec`, `DEFAULT_PANELS`, `next_layout`, `circle_index`, `layout_description`, `mount_layout`, `CHROME_CSS` |
| `tui_chrome.gallery` | `GalleryScreen`, `NestedSubmenuScreen`, `EffectsDemoScreen` |
| `tui_chrome.menu_intake` | `MenuLocateScreen`, `MenuFilePicker`, Olivia voice pools |
| `tui_chrome.bootstrap_stage` | Stage A/B theater, `run_full_bootstrap_theater`, quiet/fast flags |
| `tui_chrome.native_dialog` | `try_tkinter_open`, PowerShell / zenity helpers |

Import chrome after venv has `textual` (except `effects`, which is stdlib-only).

---

## Launcher helpers (`AWESOME_LAUNCHER_OF_TUIDOOM`)

Importable for tests (avoid calling `main()` / `launch_launcher_tui` in unit tests):

| Function | Role |
|----------|------|
| `load_config` | Merge `LAUNCHERCONFIG.JSON` over defaults |
| `ensure_dirs` | Create menus / logs / sessions dirs |
| `expand_search_paths` | Expand user paths for zip search |
| `find_menu_zips` | Glob `*.zip` under search paths |
| `extract_menu_zip` | Extract + read `main_script` |
| `run_harness_once` | One harness subprocess |
| `run_chunked_harness` | Date range of harness runs |
| `create_demo_menu_zip` | Write demo zip bytes |
| `save_recording` / `replay_session` | Session JSON |
| `detect_env` | Platform / WSL sniff |

See [HARNESS-CONTRACT.md](./HARNESS-CONTRACT.md).

---

## Other entry modules

| File | Role |
|------|------|
| `launcher.py` | Stdlib bootstrap → prefer AWESOME for product UX |
| `minimal_tui.py` | Tiny Textual smoke |

---

## Not product API

- `textual_main_app_schema.GrokBuildTUI` — design baby-step only.  
- Potential wrap-any / 7-phase modules — **not approved** (PR-ROADMAP P-20 / P-21).
- Distribution entry shell — `awesome_tui` package (PR-10); see docs/DISTRIBUTION.md.  
