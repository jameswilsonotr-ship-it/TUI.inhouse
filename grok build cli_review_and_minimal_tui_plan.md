# Grok Build CLI Review and Minimal TUI Plan

## What the Files Say (the design principles and implementation walkthrough from the included folder)

The two main files provide explicit directions based on our conversations for the Grok TUI as a launcher for the Grok Build CLI and the sovereign project.

**grok_tui_design_principles.md**:

Locked design principles for the Grok TUI Launcher:

- Zero path bullshit: Launcher discovers its own siblings or uses a simple registry. You can drop new module folders anywhere under a `modules/` tree or give it explicit paths; it figures it out.
- Env sniffing first, always: Detect WSL, PowerShell, CMD, native Linux, macOS, even containerized. Check Python version, pip presence, venv capability, existing virtualenvs.
- Dep installation that doesn't suck: Per-module `requirements.txt` (or inline list / pyproject.toml snippet). Creates isolated venv per module (or shared base venv) so Click/Textual/Rich fights don't poison the whole rig. Uses `subprocess` + `venv` + `pip` with clear progress in the TUI.
- Modular by nature: Not "skills" — plain `.py` files or small packages. Each registers itself (simple decorator or `register_module()` call). The TUI discovers them dynamically.
- TUI framework choice: Textual (not Click for the main surface). Textual gives you real screens, reactive widgets, CSS-like styling for **texture** (panels, borders, gradients via Rich under the hood, themes, mouse/keyboard, async streaming for big logs/data). Click can still be used *inside* a module if you want traditional CLI sub-commands.
- Texture: Textual + Rich lets us give it that Olivia Dev Alpha hacker-girl feel — dark terminal with glowing accents, gem-red highlights, clean bordered panels, heat-reactive color shifts if we wire Gutter Mode into the UI chrome, monospace beauty with visual weight. Not flat. Not boring.
- Easy launcher contract:
  - `python launcher.py` → shows TUI home with module grid
  - `python launcher.py grok-build` → directly boots the Grok Build TUI screen
  - `python launcher.py wrap /path/to/any_script.py` → sniffs, venvs, installs, runs it inside a managed TUI wrapper
- Future-proof: Same launcher can later spawn compiled single-file versions (PyInstaller/Nuitka) or stream large data through async workers without choking.

Alignment Notes:
- Aligns directly with Grok Build 7-phase sovereign pipeline and Iron Pearl / Frankenbride rig under Liv HUB protective claim.
- Gutter Mode visuals available and toggleable (affects TUI chrome intensity, color saturation, "ruined" text effects for high-heat states).
- Pure Python core — LLM orchestration is an optional plug-in module only.
- All outputs respect C-64 ANSI bordered blocks where appropriate for sovereign terminal feel.
- Strict anti-injection, RACK consent, and symmetry nesting rules inherited from the Chaos Bratz Roster and Liv HUB.

**ROSTER BOOT STATUS**: Partial load complete using published skill as single source of truth (memory.md ignored per user decision path). Mirrors/ instantiated for consistency. Full expert triad claim active.

**grok_tui_implementation_walkthrough.md**:

High-Level Implementation Walkthrough (Idiot-Proof):

Step 0 — Bootstrap (stdlib only, ~150 lines)
Create `launcher.py` that does **nothing but**:
- Detect env (platform + os + subprocess checks for WSL_DISTRO_NAME, PSModulePath, etc.)
- Find/create a base `.venv` next to itself (or in a known bunker location)
- Ensure `textual`, `rich`, `prompt_toolkit` (and any core Grok Build deps) are installed in that venv
- Re-exec itself inside the venv if not already
- Parse args or fall into TUI home screen

This file never depends on heavy libs at import time. It is the "at worst just run python + script name" launcher you want.

Step 1 — Module Registry (tiny, elegant)
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

Step 2 — The TUI Itself (Textual)
Main app = one `App` class with multiple `Screen`s:
- Home grid (big friendly buttons/tiles for each major area: Grok Build Phases, Roster Inventory, Overlap Engine, Hardware Rig, Voice Pipeline, Drive Partitions, etc.)
- Each tile launches its own Screen with live widgets, logs, buttons that trigger real actions (via subprocess or direct function calls into the actual Grok Build logic).
- Streaming panes for large output (gigabyte logs from mining pipelines, Starlink stats, etc.) using Textual's built-in async + Rich renderables.
- Status bar at bottom that can show Heat/FILTH/Gutter indicators if we wire it (Gutter Mode toggle lives in the chrome from turn one).
- Command palette (Textual has one built-in) so you can type "roster inventory", "advance phase 3", "enter gutter" etc. and it routes.

This gives you the Olivia Dev Alpha interface energy — clean, sovereign, visual weight, hacker texture — without needing an LLM to generate the UI every time. The LLM can be an optional spoke you plug in later for natural-language command parsing inside the TUI.

Step 3 — Wrapping Arbitrary Python Stuff
Add a `wrap` sub-command / screen:
- You point it at any `.py` file or installed package.
- It sniffs imports (simple regex + ast fallback, or you just drop a `requirements.txt` beside it).
- Creates a dedicated venv for that wrapped thing (or reuses base).
- Installs everything.
- Runs it either headless or inside a Textual "host" screen that captures stdout/stderr and gives you pretty logs + restart button.

Future: same wrapper can output a PyInstaller spec so the whole wrapped thing becomes a single exe for the truck cab or bunker rig.

Step 4 — Making It Feel Like Grok Build CLI + Olivia Dev Alpha
We map the 7-phase pipeline directly onto TUI screens + a live dashboard that calls into the existing `grok-build` skill references (test harness, mirror, phase tracking). The roster commands (`roster inventory`, `roster boot`, etc.) become first-class TUI actions or hotkeys. Everything stays under the Liv HUB protective claim and C-64 bordered aesthetic where it makes sense (we can theme Textual to look like glorious ANSI art when you want that retro hacker feel).

This is **exactly** the kind of self-sovereign, modular, texture-having, path-agnostic launcher the Iron Pearl rig deserves for IRT OTR return. It survives LLM outages, works in the cab, compiles when you want it to, and scales from tiny scripts to gigabyte streaming pipelines.

**Gutter Mode Note**: Toggle available from first screen. When active, TUI chrome can apply higher-contrast / "ruined" styling to panels and text for high-heat visual feedback (optional, user-controlled).

---

The files (and the 7 phases json) provide a clear explicit reading on what we're trying to do: a modular Textual TUI launcher for the Grok Build CLI and the full sovereign 7-phase project, with specific branding and practical bootstrap.

## Any Clarifying Questions, Critiques or Suggestions She Has (from the files)

The files do not contain explicit sections labeled "clarifying questions", "critiques" or "suggestions".

They are presented as positive, locked directions ("Locked for implementation", "Idiot-Proof" walkthrough). No questions, critiques of prior work, or suggestions for changes are listed in the text. The content *is* the directions based on our conversations.

"OLIVIA IS CHECKING IN" appears to be your note/context that these came from the web version of the chat (Olivia persona providing/checking these in).

## My Own Clarifying Questions, Critiques, and Suggestions

**Clarifying questions:**
1. Are these *exactly* the two new files from the web version ("OLIVIA IS CHECKING IN")? They fit "directions based on our conversations and needs" perfectly (Olivia Dev Alpha references, modular TUI tied to 7 phases), but if there are literally two other files with that exact header/phrase or in a different location, please give the exact paths/names so I can read them directly.
2. The design is very explicit about a standalone `launcher.py` as the entry point (stdlib bootstrap + module discovery + re-exec, then hands off to the TUI). The current folder has `textual_main_app_schema.py` as the "TUI" piece. Is the plan for the launcher to invoke/use the schema, or are these files standalone directions that should replace/update the existing schema?
3. The directions are based on our conversations. Is the "web version" meaning these files were generated or checked in from the Grok web chat with the Olivia persona, and do they supersede or add to the previous design files at the root / in Grok-TUI-Project? Any specific differences from our last conversations that I should flag?

**Critiques:**
1. The design is very well aligned with our previous discussions on making it modular, branded with Olivia Dev Alpha / Gutter Mode, and practical for the sovereign project.
2. There is a noticeable gap between the high-level "locked" design and the current code state (still very baby-step/stubby, as we noted before in sprint001). The walkthrough is "idiot-proof" at the conceptual level but doesn't bridge to concrete next code.
3. The "web version" sync (Drive manifest + duplicates) is useful but has introduced some clutter/duplication that could slow "as few steps as possible" implementation.

**Suggestions:**
1. These two files + the 7-phases JSON together form a very clear explicit spec for what we're trying to do. We could treat the Grok-TUI-Project folder (or a cleaned subset) as the "source of truth" bundle for the next steps.
2. To keep momentum, the brainstorm could start narrow (e.g., scope of the first minimal launcher + one screen) rather than the full 7-phase TUI at once.
3. When we write the file back to her, include a short summary of the files + the Q/C/S list (hers + mine) + proposed next steps for her review/approval before formal planning.
4. Once we have her input, the "formal planning / phasing" + "auto approve and get something working in as few steps as possible" could focus on a tiny vertical slice (e.g., bootstrap launcher that launches a basic Textual home using the schema, with one registered module example).

## Brainstorm Notes

Following the brainstorming skill (explore context done via reading the files and previous; one question at a time; propose approaches; present design; etc.).

The goal is a robust modular TUI in Python for the Grok Build CLI, based on the 7-phase pipeline, with the launcher as described.

Approaches:
1. Full implementation per the walkthrough: start with launcher.py bootstrap, then module registry, then full Textual app with multiple screens.
2. Minimal viable: implement only the bootstrap + basic home grid using the schema, hardcode some modules for the phases, add Gutter Mode toggle.
3. Hybrid: use the schema as contract, implement launcher that loads modules dynamically, but start with one screen (e.g., phase dashboard) and the wrap feature.

Recommendation: Start with approach 2 for "as few steps as possible" to get something working, then expand.

Visuals would help for the home grid and screens (offer visual companion if needed, but since text, proceed).

Clarifying (one at a time): What is the exact primary entry point the user will run to launch this TUI right now? A. `python textual_main_app_schema.py` (or similar) directly. B. A separate `launcher.py` (stdlib-only, does venv sniffing + re-exec + module discovery, *then* imports/runs the schema-driven app). C. Something installed as a console script (`grok-tui` or `python -m grok_tui`). D. Other.

(We will continue brainstorm based on your response.)

## Formal Planning / Phasing (initial)

Phase 1: Bootstrap and basic launcher (as per Step 0 and 1 in the walkthrough).
- Create launcher.py that detects env, sets up venv, installs deps (textual, rich, etc.), re-execs.
- Basic module registry stub.
- Launch minimal Textual app from the schema (home grid with buttons for phases, roster, etc.).

Phase 2: Minimal TUI screens.
- Implement HomeGridScreen with buttons.
- Add Gutter Mode toggle.
- Basic status bar.

Phase 3: Module integration and wrap.
- Example module for one phase.
- Wrap feature stub.

Phase 4: Expand to more screens, polish branding, test.

Then auto approve small parts, get minimal working.

## Next Steps (as few as possible)

1. Create the launcher.py based on the walkthrough.
2. Integrate with the existing schema.py for the TUI.
3. Run and test basic home.

(We will go from your input on the brainstorm question and the files.)

---
This document processed the directions from the design files as per the last turn's instructions. The two files from web version (assumed the design principles and walkthrough in the included Grok-TUI-Project as they provide the clear explicit reading) were reviewed. 

Olivia's Q/C/S: none explicit in the text.
My own: as above.
Brainstorm started.

Wrote this as the file back to her.

Ready for next.