# TUI Launcher Planning

## Planning Record (Consolidated)

**Recorded**: 2026-06-29 (per user request to capture planning done so far in markdown file)

**Focus**: Stayed focused. No weird meta recording. Used /btw prompt (provided by user) for answers to avoid infinite loop of clarifying questions / turns. User interjected/stopped prior turn when it looked like looping.

**User Request Summary** (exact scope):
- Rock-solid, dead-stupid-simple Python TUI launcher (e.g. AWESOME_LAUNCHER_OF_TUIDOOM.py + LAUNCHERCONFIG.JSON).
- Runs if Python is in PATH: `python AWESOME_LAUNCHER_OF_TUIDOOM.py`.
- Default menu prompts "go find a real menu".
- System of packaged zips for menus (files/scripts/assets/etc): decompressed from inside the launcher (selectable, searched); executed or interpreted.
- Header, footer, screen elements with prompts + logic + decision making + file input/output.
- Library of scripts that have exit levels (0=done/success, 1=error, 2=partial) and "operation harnesses".
- Harnesses support chunked processing (e.g. processing one day of memory files at a time or a week only).
- Little TUI thing can loop through a big task until it is done.
- Error logs, processing logs, etc.
- Offer to record a "playback or recording of session script" which can automate the process for later if the data or script or environment or whatever changes.
- BBS level god tier but still dial up BBS level functionality (simple menu).
- Phase 1 = minimal working TUI bits (launcher etc.). Go through brainstorming on web artifacts, formal planning, record to md, then implement.

**Artifacts Processed** (web version files from "OLIVIA IS CHECKING IN" + kept design files):
- grok_tui_design_principles.md: Locked principles (zero path bullshit, env sniffing first, dep install via venv, modular REGISTERED_MODULE, Textual TUI + texture/C-64/Olivia Dev Alpha/Gutter Mode, easy launcher contract, 7-phase alignment, Liv HUB).
- grok_tui_implementation_walkthrough.md: Step-by-step (bootstrap stdlib launcher.py, registry, Textual App/Screens/home grid, wrap, map to 7-phase).
- grok_build_7_phases.json + schema + tcss + manifest.
- grok build cli_review_and_minimal_tui_plan.md + tui_menu_research_copyable_examples.md + brainstorming-2026-06-29-TUI-design-brainstorm.md (produced during process).
- sprint review notes.

**Brainstorm / Review Outcomes** (full in sections below):
- What makes sense: bootstrap (stdlib-only first), modular registry, Textual for robust TUI, branding/texture, launcher contract, 7-phase tie-in.
- Needs clarif (resolved via /btw + user vision): adapt modules->zip menus, default "find real menu" + search/extract, harness/chunk/record details, exact zip structure + execution.
- Critiques: artifacts high-level + Grok-Build-specific; current code was baby-step; need super-simple (python-in-path, no bloat).
- Suggestions / chosen approach: Hybrid (bootstrap from design + Textual framework + zip menu support + harness contract inside zips). Launcher owns TUI chrome + config + search/extract/run/logs/record; zips provide the "real" menu content/harness/scripts.
- 2-3 approaches considered then narrowed (pure text/BBS subprocess; full original modules; hybrid with zips). Hybrid selected for simplicity + power.

**Formal Planning** (Phase 1 focus - full details in "Formal Planning" and "Implementation Steps" sections below):
- Launcher script + config as specified.
- Zip menu packaging + extract + entry (menu.json + harness.py).
- Operation harnesses: exit codes, chunk params, logs.
- TUI screens: menu, chunk config, logs, record.
- Recording/replay of session choices for automation.
- BBS-simple yet harness-powered for real chunked looping work (e.g. memory file days).
- Impl steps, verification, files listed below.

**Planning Docs Produced**:
- This file (TUI_Launcher_Planning.md) as primary record of artifacts + formal plan.
- grok build cli_review_and_minimal_tui_plan.md (file review + Q/C/S + initial phasing + "file back").
- tui_menu_research_copyable_examples.md (Textual menu patterns).
- brainstorming-*.md (session notes).

**Work Completed During Planning**:
- Git diagnostics (master/main split, filename variants with/without spaces, duplicate push visibility, ls-tree/log/show confirmed files on master).
- launcher.py (bootstrap per walkthrough).
- minimal_tui.py (runnable home grid + Gutter Mode per design, as early working bits).
- Schema and design files kept/inspected.

**User Feedback on Plan**: "your plan seemed fine as s... we will do more with phase 2 and stuff... next turn"

**Git at Record Time**: On master. Recent commits cover review/plan + py launchers. Working tree clean at session start.

**Next (per user)**: Plan is solid for Phase 1. More Phase 2 next turn. (No auto-implement until turned loose; record complete.)

See detailed sections below for the full brainstorming on artifacts, critiques, formal planning, Phase 1 spec, zip/harness examples, and implementation steps.

---

## Brainstorming on Web Artifacts

The web artifacts (from Grok-TUI-Project) describe a Grok TUI Launcher with the following key elements:

### Design Principles
- Zero path bullshit: Launcher discovers its own siblings or uses a simple registry. Modules can be dropped in modules/ tree or explicit paths.
- Env sniffing first: Detect WSL, PowerShell, CMD, Linux, macOS, containers. Check Python, pip, venv.
- Dep installation that doesn't suck: Per-module requirements. Isolated venv per module or shared base. Use subprocess + venv + pip with progress in TUI.
- Modular by nature: Plain .py or small packages. Register with decorator or call. TUI discovers dynamically.
- TUI framework: Textual (not Click for main). Real screens, reactive widgets, CSS for texture. Click inside module if needed.
- Texture: Olivia Dev Alpha hacker-girl feel - dark terminal, glowing accents, gem-red, bordered panels, heat-reactive Gutter Mode, monospace beauty.
- Easy launcher contract:
  - python launcher.py -> TUI home with module grid
  - python launcher.py grok-build -> boot Grok Build TUI screen
  - python launcher.py wrap /path/to/script.py -> sniff, venv, install, run in managed TUI wrapper
- Future-proof: Compiled versions or async streaming.

Alignment: Grok Build 7-phase pipeline, Iron Pearl rig, Liv HUB claim. Gutter Mode toggleable. Pure Python core. C-64 ANSI. Anti-injection, RACK, symmetry.

### Implementation Walkthrough
- Step 0: Bootstrap launcher.py (stdlib, ~150 lines): detect env, .venv, install textual/rich/prompt_toolkit, re-exec in venv, parse or TUI home. No heavy libs at import.
- Step 1: Module Registry: Each module has REGISTERED_MODULE dict with name, version, requirements, description, entry. Launcher imports, installs, calls entry with context.
- Step 2: The TUI (Textual): App with Screens. Home grid with buttons for areas (phases, roster, overlap, hardware, voice, drive). Live widgets, logs, buttons. Streaming panes. Status bar (Heat/FILTH/Gutter). Command palette.
- Step 3: Wrapping: wrap command/sniff, venv, host screen with logs/restart. Future PyInstaller.
- Step 4: Make it feel like Grok Build + Olivia Dev: Map 7-phase to screens + dashboard calling grok-build logic. Roster as TUI actions. C-64 aesthetic.

Gutter Mode: Toggle from first screen, higher contrast for high-heat.

### 7 Phases
The pipeline for sovereign development: env, tooling, data, hardware, automation, voice, IRT OTR. TUI as control surface.

### Review and Menu Research
The review confirms the design for modular launcher/TUI aligned with 7-phases, sovereign aesthetics. Notes the baby step is partial. Menu examples for Textual: home grid, sidebar, command palette, Gutter CSS. Suggestions for minimal start with launcher + one screen.

**What makes sense**: The bootstrap for simplicity, modular registry, Textual for TUI with branding, launcher contract, tie to 7-phase.

**Needs clarification**:
- How to adapt the "modules" to "menus" as zips.
- The default menu "go find a real menu" - how to implement search for zips.
- The harness for chunked processing and recording.
- Exact structure of the zip for menus (e.g. what files inside, how to execute).

**Critiques**:
- The design is high level, the current code is baby step with stubs.
- The artifacts are specific to Grok Build, but user wants general for any "menu" like processing tasks.
- Need to keep super simple as per user: no complex install, just python in path.

**Suggestions**:
- Use the bootstrap idea for the launcher to handle deps simply.
- Make the launcher support loading zips as "real menus".
- The launcher provides the TUI framework (header, footer, basic screens), the zip provides the content (scripts, harness).
- For simplicity, the launcher can be the main py, it handles config, default menu, zip search/extract/run.
- Use Textual for the TUI to match the design.
- For harness: the zip can contain a harness.py that the launcher runs with params for chunk, logs.
- Recording: the launcher can log the TUI interactions or choices to a file for replay.

**Approaches**:
1. Minimal text based launcher with subprocess for menus (BBS style, simple).
2. Textual based launcher as per design, with zip support for menus.
3. Hybrid: launcher with bootstrap, uses Textual for UI, supports zips.

Recommendation: Approach 2, adapt the design to support zips as menus, keep the bootstrap for simplicity.

## Formal Planning

### Phase 1: Minimal Working TUI Bits (Launcher)

**Goal**: A simple launcher that can run with python in path, shows a default menu, can find and load a "real menu" from zip, runs it with basic harness, supports logging and basic recording. BBS like simple menu system.

**Launcher Script**: AWESOME_LAUNCHER_OF_TUIDOOM.py

- If python in path, `python AWESOME_LAUNCHER_OF_TUIDOOM.py` runs.
- Loads LAUNCHERCONFIG.JSON for paths, defaults, branding.
- Uses Textual for TUI (to match design).
- Header: "AWESOME LAUNCHER OF TUI DOOM" with Gutter status, C-64 style.
- Footer: key bindings, current status.
- Main screen: menu with options.
  - Default: "1. Go find a real menu" - prompts or searches for zip files in configured paths.
  - Other basic: view logs, record, quit.
- When select a menu zip: decompress to .launcher_menus/<name>/ (using zipfile).
- Look for main entry (e.g. menu.py or harness.py as per config in zip or default).
- Run it using harness: the launcher provides or the zip has a harness that handles execution, chunking, logging.
- For chunked: e.g. for memory files, the harness takes --start-date, --end-date, processes files in range, logs per chunk.
- The TUI can show prompt for chunk params, then run the harness, show logs in a log pane.
- Loop for big task: the harness can be called in loop from the TUI or the harness handles.
- Logging: error.log, processing.log written by harness, shown in TUI.
- Recording: button to start recording, logs the choices and inputs to a .session file. Option to replay from session file.
- Library: the launcher keeps track of loaded menus and their scripts (from zip manifest or scan).
- Scripts have exit levels (e.g. 0 success, 1 error, 2 partial) and harness metadata.

**LAUNCHERCONFIG.JSON** example:
{
  "menu_search_paths": [".", "~/.tui/menus"],
  "default_menu": "find_real",
  "branding": {
    "header": "AWESOME LAUNCHER OF TUI DOOM",
    "footer": "Gutter Mode | C-64 | Olivia Dev"
  },
  "harness": {
    "chunk_size": "1day",
    "log_dir": "logs"
  }
}

**Packaged Menu Zip** example structure:
menu.zip
- menu.json (name, description, main_script: "harness.py", entry: "run")
- harness.py (the script with harness logic, takes args like --chunk, --log)
- assets/ (optional)
- scripts/ (additional scripts)

The launcher searches for zips, when selected, extracts to temp or cache, runs python -m harness --chunk ... with the harness handling the logic.

**Header, Footer, Screens**:
- Use Textual.
- Header with branding, current menu, Gutter status.
- Footer with keys.
- Screens: main menu screen, config screen for chunk, log screen, record screen.
- Prompts: Textual Input, Select for menus.
- Logic: buttons and actions for run, record, search.
- File I/O: select files for processing, read/write logs.
- Library: a screen or pane listing available scripts/menus with status.

**Operation Harnesses**:
- The harness.py in the zip is a python script that can be run standalone or by launcher.
- It supports exit levels (sys.exit(0) success, 1 error).
- For chunked: if --chunk provided, process that chunk, else loop over range.
- Logs to specified files.
- The launcher can call it multiple times for big tasks or the harness supports range.

**Recording**:
- During run, option to record the session (the TUI choices, inputs, selected menu, params).
- Save to .session.json with the sequence.
- Replay: python AWESOME...py --replay session.json which simulates the choices, runs the same.

**BBS Level Functionality**:
- Simple menu system like old BBS: numbered options, select by number or keys.
- Robust for tasks: error handling, logs, resume from partial.
- No bloat: keep the launcher small, menus are the extension.
- God tier: the harness makes it powerful for real tasks like processing large data in chunks with full logging and automation recording.
- Dial up simple: run with python, text based menus, no complex setup.

**Implementation Steps for Phase 1 (minimal)**:
1. Create the launcher.py with bootstrap (from design), load config, use Textual for basic app with header/footer.
2. Implement default menu screen with "Go find a real menu" that searches for .zip, lists, selects.
3. On select, extract zip to cache using zipfile.
4. Basic run: use subprocess to run the harness.py from extracted with params, capture output to log pane and file.
5. Basic harness example in a sample zip: a python script that prints, supports --chunk, writes logs.
6. Add simple recording: log choices to json, replay by re-running with params.
7. Add library: scan and list available.
8. Make sure if python in path, python launcher.py works (handle deps with bootstrap or assume installed).
9. Test with chunked example (e.g. process "files" in range).

**Verification**: Run the launcher, it shows menu, can "find" a sample zip, run with chunk, see logs, record a session, replay.

**Files to create**:
- AWESOME_LAUNCHER_OF_TUIDOOM.py (or launcher.py)
- LAUNCHERCONFIG.JSON
- sample_menu.zip (with harness.py example)
- Perhaps a harness base in the launcher.

This keeps it simple, matches the design from artifacts (bootstrap, modular, Textual, branding), and user requirements (zip menus, harness, chunk, record, BBS simple).

Next: implement Phase 1.