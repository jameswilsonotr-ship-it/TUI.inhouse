# PR-15 — Integrate capabilities into default demo zip

**Status:** **runtime landed** — `create_demo_menu_zip()` builds capability pack; auto-open on launch  
**Branch (suggested):** `feat/demo-zip-capabilities`  
**Depends on:** **PR-11…14** (schema + layout + output + samples)  
**Priority:** Final in this series  

---

## Goal

When the user launches the product **with no menu specified**, the built-in demo (`sample_menu.zip` / config `demo.sample_zip_name`) MUST expose:

1. Wave motion  
2. File picker  
3. Web search sample  
4. (Optional) legacy harness chunk demo for bridge  

…using the **v1 menu system**, **standard_menu layout**, and **output windows**.

## Deliverables

- [ ] Rebuild `create_demo_menu_zip()` to pack:
  - `menu.json` (v1 capability-demo)  
  - `menu.md` / optional `menu.html`  
  - `layout.json` → standard_menu  
  - `windows.json`  
  - `scripts/wave.py`, `file_picker.py`, `web_search.py`  
  - optional `harness.py` legacy bridge  
- [ ] Default launch path: no zip found → create/use demo → open capability menu  
- [ ] QUICKSTART + PHILOSOPHY note updated  
- [ ] `scripts/run_harness.py` / tests cover demo pack validate + dry-run scripts  

## Acceptance

```bash
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
# unzip -l sample_menu.zip  → shows menu.json + scripts/*
python scripts/validate_menu.py sample_menu.zip   # when available
```

Interactive: launch with empty search → demo menu items run into `main_output`.

## Migration

- Old phase1-only demo remains representable via `legacy_harness` item.  
- Existing user zips unchanged (legacy bridge).  

## Non-goals

- Network required for demo to *open* (only web search item needs network)  
