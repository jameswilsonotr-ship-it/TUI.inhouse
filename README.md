# Grok TUI (TUI work)

**Location**: C:\Users\chast\#CODE\TUI
**Purpose**: Core work on the robust, modular Python TUI framework (Textual-based).

This folder is dedicated to the actual TUI implementation and deployment.

## Kept (supposed to be here)
- textual_main_app_schema.py — Core schema/contract for the modular app (screens, modules, gutter mode, etc.)
- grok_tui.tcss — Textual CSS styling
- grok_tui_design_principles.md — Design principles for the TUI
- grok_tui_implementation_walkthrough.md — Implementation guidance
- FOLDER-STANDARDS.md — Reference copy of folder discipline (originals in proper sovereign locations)
- sprint001/ — Current sprint tracking and plans (timestamped)
- .git/ — Version history for this TUI project

## Recent Cleanup (Refactoring)
Mismatched / olivia-dev / mining / old-project / stale files were moved to:
C:\Users\chast\grok_sunsets.bak\TUI

See the MANIFEST.md and README.md there for full details (labeled as MISMATCHES for safety and disentanglement).

## Current Push
Implement and deploy a **modular and simple framework** as discussed in the design files still here.

**Phase 1 delivered (auto-approved)**:
- `AWESOME_LAUNCHER_OF_TUIDOOM.py` — the primary entry point. `python AWESOME_LAUNCHER_OF_TUIDOOM.py` (Python in PATH)
- `LAUNCHERCONFIG.JSON`
- Full zip menu support (scan, select, extract), operation harnesses (chunked e.g. daily memory files, exit levels 0/1/2, logs)
- Textual TUI with header/footer, prompts, live run log, library, recording + replay
- Demo: `python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo` then scan + run
- BBS-simple but powerful. See TUI_Launcher_Planning.md for full recorded plan.

Focus on:
- Using the schema as contract (future expansion)
- Building the actual app/components in a clean, simple, modular Python structure
- Following the principles in the kept docs
- Olivia design files on master branch (planning md pushed to both master + main)

See sprint001/ for active plans and the code review notes.

**GitHub Repository**: https://github.com/jameswilsonotr-ship-it/TUI.inhouse

AGENTS.md at #CODE root for overall workspace discipline.

---
Cleaned: 2026-06-29 03:37
Repo renamed to TUI.inhouse (2026-06-29)
