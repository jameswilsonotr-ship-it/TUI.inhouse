# PR-04 — Layout chrome (panels / borders / GUI shells)

## Intent

Borrow **patterns** (not wholesale vendored repos) from Textual docs / community TUI layout idioms:

- Multi-pane `Horizontal` / `Vertical` / `Grid`
- Bordered panels (TCSS `border: heavy|round|double|ascii`)
- Header/footer chrome, title bars
- “BBS window” feel with C-64-ish colors

Code lives in `tui_chrome/layouts.py` + `tui_chrome/chrome.tcss`  
**No** full clone of external GitHub apps — attribution notes + pattern ports only.

## Deliverables

- Panel factory helpers
- Named layout presets: `two_stack`, `three_vertical`, `two_plus_h`, `six_grid`
- Shared TCSS fragments for borders

## Acceptance

- Gallery (PR-05) can switch layouts using presets  
- CSS loads without missing-file crash  
