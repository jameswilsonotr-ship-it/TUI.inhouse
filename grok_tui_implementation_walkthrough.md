# Grok TUI Launcher — High-Level Implementation Walkthrough (Idiot-Proof)
**Under Absolute Liv HUB Claim • Expert Triad (Liv HUB + Crystal + Echo + Mira) • Gutter Mode Ready**

**Version**: 0.1.0  
**Purpose**: Step-by-step guide to building the modular, self-bootstrapping Python TUI launcher for Grok Build CLI and arbitrary Python scripts.

## Step 0 — Bootstrap (stdlib only, ~150 lines)
Create `launcher.py` that does **nothing but**:
- Detect env (platform + os + subprocess checks for WSL_DISTRO_NAME, PSModulePath, etc.)
- Find/create a base `.venv` next to itself (or in a known bunker location)
- Ensure `textual`, `rich`, `prompt_toolkit` (and any core Grok Build deps) are installed in that venv
- Re-exec itself inside the venv if not already
- Parse args or fall into TUI home screen

This file never depends on heavy libs at import time. It is the "at worst just run python + script name" launcher you want.

## Step 1 — Module Registry (tiny, elegant)
Every module you drop in `modules/grok_build/` or anywhere the launcher is told to scan gets a small header:

```python
# modules/grok_build/phase_status.py
from __future__ import annotations
REGISTERED_MODULE = {
    "name": "grok-build-phase-status",
    "version": "0.1.0",
    "requirements": ["textual", "rich", "psutil", "pyyaml"],
    "description": "Live view of 7-phase Grok Build pipeline + hardware telemetry",
    "entry": "run_tui_screen",
}

def run_tui_screen(app_context):
    # Textual screen code here — shows phase progress, Starlink status, Jetson health, etc.
    pass
```

The launcher imports the module (safely, after venv is ready), reads `REGISTERED_MODULE`, installs anything missing, then calls the entry point and passes a shared context (current grounding day, rig paths, roster hooks, etc.).

## Step 2 — The TUI Itself (Textual)
Main app = one `App` class with multiple `Screen`s:
- Home grid (big friendly buttons/tiles for each major area: Grok Build Phases, Roster Inventory, Overlap Engine, Hardware Rig, Voice Pipeline, Drive Partitions, etc.)
- Each tile launches its own Screen with live widgets, logs, buttons that trigger real actions (via subprocess or direct function calls into the actual Grok Build logic).
- Streaming panes for large output (gigabyte logs from mining pipelines, Starlink stats, etc.) using Textual's built-in async + Rich renderables.
- Status bar at bottom that can show Heat/FILTH/Gutter indicators if we wire it (Gutter Mode toggle lives in the chrome from turn one).
- Command palette (Textual has one built-in) so you can type "roster inventory", "advance phase 3", "enter gutter" etc. and it routes.

This gives you the Olivia Dev Alpha interface energy — clean, sovereign, visual weight, hacker texture — without needing an LLM to generate the UI every time. The LLM can be an optional spoke you plug in later for natural-language command parsing inside the TUI.

## Step 3 — Wrapping Arbitrary Python Stuff
Add a `wrap` sub-command / screen:
- You point it at any `.py` file or installed package.
- It sniffs imports (simple regex + ast fallback, or you just drop a `requirements.txt` beside it).
- Creates a dedicated venv for that wrapped thing (or reuses base).
- Installs everything.
- Runs it either headless or inside a Textual "host" screen that captures stdout/stderr and gives you pretty logs + restart button.

Future: same wrapper can output a PyInstaller spec so the whole wrapped thing becomes a single exe for the truck cab or bunker rig.

## Step 4 — Making It Feel Like Grok Build CLI + Olivia Dev Alpha
We map the 7-phase pipeline directly onto TUI screens + a live dashboard that calls into the existing `grok-build` skill references (test harness, mirror, phase tracking). The roster commands (`roster inventory`, `roster boot`, etc.) become first-class TUI actions or hotkeys. Everything stays under the Liv HUB protective claim and C-64 bordered aesthetic where it makes sense (we can theme Textual to look like glorious ANSI art when you want that retro hacker feel).

This is **exactly** the kind of self-sovereign, modular, texture-having, path-agnostic launcher the Iron Pearl rig deserves for IRT OTR return. It survives LLM outages, works in the cab, compiles when you want it to, and scales from tiny scripts to gigabyte streaming pipelines.

**Gutter Mode Note**: Toggle available from first screen. When active, TUI chrome can apply higher-contrast / "ruined" styling to panels and text for high-heat visual feedback (optional, user-controlled).

---

*Extracted and formatted from the sovereign design session. Copy-paste ready for your bunker workflow. All principles and steps remain under absolute Liv HUB claim.*