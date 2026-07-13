# PR-06 — ANSI / ASCII effects (strobe, glitter, sparkle)

## Intent

Classic BBS-era energy as a **reusable module** (`tui_chrome/effects.py`):

- Strobe frames (ANSI color swaps)
- Sparkle / glitter particle lines (ASCII)
- Banner crawl
- Used by gallery + optional install.sh theater + Phase 3 test

## Deliverables

- Frame generators (no third-party deps)
- `EffectsDemoScreen` (key `E` from launcher)
- Integration: gallery panel can run sparkle timer

## Acceptance

- [ ] Effects module importable without Textual  
- [ ] Textual screen shows animated frames  
- [ ] Can disable with `--quiet` style flags later  
