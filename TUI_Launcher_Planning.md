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

**Phase 1 Status (2026-06-29)**: Implemented and committed (see commit 4f0b60a + merge of a1819d5). Core launcher works, demo passes verification.

---

## New Commit Inspected (a40a52d - "Olivia says read this.md")

Checked out repo first (fetched, inspected commit, extracted the file safely to temp only per instructions, read it via read_file on temp copy). This is the file Olivia explicitly says to read.

Commit message: "Created 'Olivia says read this.md' on master branch with full Textual TCSS + Gutter Mode guide and starter template. This is the canonical planning document. GrokBuildCLI / Rockville CLI: STOP overwriting files I push. Read this file. We are observing."

The file (268 lines) is the **full consolidated guide** (previously only a 1-line stub in a1819d5).

**Key inputs from the file for Phase 2/3**:
- TCSS explanation and usage (CSS_PATH or inline, variables, pseudo, grid, theming).
- Gutter Mode via two CSS layers + simple class toggle (`.gutter-active` on App, watch_reactive or action to add/remove class). Examples for .pane, .menu-item, .log, Header in normal vs gutter.
- Recommended widgets: ListView or SelectionList for Menu, Log widget for Output (best for streaming), DataTable or Static for Status/7-Phase.
- Layout: Horizontal + Vertical + CSS Grid for multi-pane.
- Subprocess streaming: Use asyncio.create_subprocess_exec + Log.write_line in a worker/task (example code provided).
- Complete minimal runnable starter template in Python (with compose using Horizontal for menu-pane + output, ListView, Log, Header/Footer, Gutter toggle binding and reactive).
- Files: grok_tui.tcss (with layers), minimal_tui.py (starter), launcher.py (bootstrap).
- Summary table of recommendations.
- Note: This is canonical; do not overwrite/replace without instruction.

**Current alignment** (extended):
- Launcher already has some streaming and basic Gutter concepts.
- Now adopt the exact patterns: switch to Log widget for harness output, proper multi-pane in the TUI, full two-layer .tcss, the reactive class toggle, asyncio streaming if moving beyond threads.
- Use the provided starter as reference to evolve the current launcher home screen and minimal_tui.py .

Phase 2 and 3 plans below are slight extensions incorporating these specific Olivia inputs.

---

## Overall Phases Before "Usable, Stable, Efficient, Future-Proofed"

**Recommendation: 3 phases total** (Phase 1 done; two more phases).

Rationale (per user request: stable + efficient + future-proofed, **but not all crazy expanded form**):
- The goal is a rock-solid, dead-stupid-simple BBS-like launcher that is *actually usable* for real chunked/looped work + automation via recording.
- Keep scope tight: focus on launcher + zip/harness contract + good TUI + recording.
- Avoid turning it into a full sovereign OS or expanding the original Grok Build 7-phase dashboard unless explicitly asked.
- "Usable": real tasks (memory days, etc.) can be run reliably from TUI or CLI replay.
- "Stable": bootstrap ensures it runs, good error handling/exit levels, no breakage on missing deps or bad zips.
- "Efficient": chunked by design (one day at a time or range), streaming logs, isolated subprocess, no full data load.
- "Future-proof": modular via drop-in zips, manifest-driven, config driven, follows locked design (zero path, venv, Textual texture, Gutter), recording allows replay when anything changes, easy to extend without core changes.
- End state at Phase 3: You can hand the AWESOME_LAUNCHER...py to someone with Python in PATH and they can do useful work immediately. No bloat.

**Phase 1 (DONE)**: Minimal working TUI bits + core contract.
- Bootstrap launcher (python in PATH works).
- Default "go find a real menu", zip search/extract/execute.
- Basic harness contract + demo (chunk, logs, exit 0/1/2).
- TUI basics + recording/replay.
- Self-contained demo.

**Phase 2: Stability + Polish + Texture + Efficiency (next)**
What it looks like (slight extension using full "Olivia says read this.md" inputs):
- Full incorporation of the canonical guide: proper external grok_tui.tcss (or launcher.tcss) with two CSS layers (NORMAL MODE defaults + .gutter-active overrides for Screen, .pane, .menu-item, .log, Header — using $error, darker backgrounds, bold, etc.). Implement via reactive bool + watch_gutter_active that does self.add_class("gutter-active") / remove_class. Bind to key "g" and button. Matches the exact pattern in the guide.
- TUI upgrade to multi-pane per guide: use Horizontal(id="main-area") + Vertical panes (e.g. menu-pane with ListView for zips/library, controls for chunk inputs/buttons, output-pane with Log widget for streaming instead of or in addition to RichLog). Adopt the compose structure from the minimal starter template in the file.
- Adopt the "full minimal runnable starter template" as reference: evolve AWESOME_LAUNCHER and minimal_tui.py to match (ListView for menu, Log for output, Header with clock, Footer, Gutter toggle action, reactive class).
- Subprocess streaming: switch/enhance to the guide's recommended asyncio.create_subprocess_exec pattern + log_widget.write(...) in a worker (for responsive live harness output, with command echo and exit code).
- Stability upgrades: zip-slip protection on extract, manifest validation, graceful missing harness, per-run log dirs, better returncode + level reporting with colors/icons in TUI.
- Efficiency: streaming non-blocking (use run_worker), add simple progress parsing from harness stdout if it emits special lines, cache last extracted for fast re-runs, resume logic for partial (exit 2).
- Harness & menu improvements: richer menu.json (requirements?, description, tags), support "scripts/" subdir in zip, example "library of scripts" with exit metadata, harness can be python or other (if shebang).
- Recording polish: better session format (include config snapshot, env notes for "when data/script/env changes"), in-TUI replay mode that steps through actions visibly.
- Usability: command palette or / commands, persistent recent menus, --help / direct CLI run without full TUI (python AWESOME... --menu foo.zip --chunk 2026-06-20), help screen.
- Future-proof seeds: expose a small HarnessBase or template generator inside launcher, version the launcher contract, full use of LAUNCHERCONFIG for everything. Use the guide's summary table as implementation checklist.
- Clean repo: .gitignore for __pycache__, sessions/, logs/ (demo only), sample zips optional.
- Verification: run full demo + range chunk, toggle Gutter (verify layers), record+replay, check logs, match the recommended widgets/layouts from the guide.

**Deliverables Phase 2**: Updated AWESOME launcher with Gutter/TCSS per guide (do not overwrite the source "Olivia says read this.md"), improved multi-pane + ListView + Log streaming, polished harness, recording v2, .tcss with layers, updated planning + reference the guide file, README examples, starter template aligned.

**Deliverables Phase 2**: Updated AWESOME launcher with Gutter/TCSS, improved panes, polished harness, recording v2, .tcss, updated planning + the guide file filled or referenced, README examples.

**Phase 3: Production Usable + Future-Proof Completion (final for core)**
What it looks like (keep contained):
- "God tier but dial-up simple" complete: robust replay that can run fully non-interactively or simulated in TUI (with diff reporting for changes), export session as standalone automation script.
- Advanced but not crazy: menu search/filter in TUI, favorites, manifest-defined "operations" beyond single harness, safe parallel chunk option (opt-in), log tailing + search in UI.
- Efficiency & scale: extract caching with hash check, large log handling (virtualized Log widget if needed), resume from session mid-way.
- Stability & future-proof: self-test mode (launcher --self-test runs demo and asserts exit levels/logs), harness template with full blade-law style headers if desired, support for venv-per-menu (opt-in in manifest), clear extension points.
- Integration light: optional bridge to existing textual_main_app_schema / GrokBuildTUI for users who want the 7-phase screens alongside (e.g. "launch grok build from launcher").
- Packaging & docs: single "distributable" note (the .py + config + one sample zip is the whole thing), full usage guide, how to author your own menu.zip.
- No bloat: everything still fits the "if python in path it just works" + BBS simple menu energy.
- End verification: End-to-end for real use case (e.g. multi-day chunk loop with recording, replay after "env change" simulation, Gutter on, clean exit on errors).

**After Phase 3**: The launcher is usable for serious repeated work, stable across runs/machines, efficient by construction (chunking + streaming + isolation), future-proof via modularity and design principles. Further expansion (voice, full sovereign 7-phase control surface, hardware telemetry panes, etc.) would be new projects or explicit Phase 4+.

**Latest Input Added to Phase 3 Plan (commit 186cd83, file: Olivia-pleasereadthis.markdown)**:
- Incorporated full details: Gutter Mode high-heat reactive (OliviaDev Alpha .gutter-active, C-64 pink/black ruined styles, intense borders/text).
- Exact branding: Header "AWESOME LAUNCHER OF TUI DOOM" bold C-64, Footer "BBS-Level | Zip Menus + Harnesses | Chunked Ops | Record/Replay | Gutter Mode | Olivia Dev Alpha | Phase X".
- Code review: Current impl strong but strengthen test harness for default/no-file + auto zip gen in final phase.
- Detailed test harness for launchers (final phase self-test): Interactive "Hey, what’s your input file, idiot?", default -> auto sample zip, enter gutter-1, flash panes in circle (rapid updates/rotating ASCII), obnoxious shit (log spam, flashes, animations), clean exit "Successful test - Gutter Mode verified and harness operational!".
- Auto-trigger sample_menu.zip if none when entering test/gutter flow.
- Use as built-in --test or default flow. Gutter live/toggleable. Build on previous guides without overwriting.
- This is now part of the canonical Phase 3 requirements for the "final phase".

---

## Detailed Remaining Phase Planning (Begin)

(Will be expanded with tasks, files, verification per turn. Start with Phase 2 as next.)

**Phase 2 Tasks (high level to start)**:
1. Create or extend dedicated .tcss (or use/extend grok_tui.tcss) with full two-layer Gutter + TCSS examples from the new guide. Add Gutter toggle to AWESOME launcher (binding + button + reactive chrome).
2. Refactor TUI screens to multi-pane layout (Horizontal/Vertical + Grid per guide). Replace simple buttons with proper ListView for discovered zips (searchable/selectable).
3. Enhance streaming: ensure all harness output + launcher messages go through RichLog with markup for levels. Add live status for current chunk/overall exit.
4. Improve harness runner + chunk loop: add resume support, parse special progress from stdout, per-chunk log subdirs optional.
5. Recording v2: richer json (include full config + argv snapshot), CLI + TUI replay modes.
6. Usability + CLI: argparse full support for direct execution, --help, list-menus, etc.
7. Stability: safe_extract function (path validation), manifest schema (light), try/except everywhere with user messages.
8. Update demo harness + sample zip to showcase more (e.g. emit "progress: 50%").
9. Docs & cleanup: fill or reference the TCSS guide with actual examples from our code, update TUI_Launcher_Planning.md + README, add minimal .gitignore.
10. Verification: full run of range + record + replay + gutter toggle + direct CLI run.

**Phase 3 high-level outline** (to be detailed later):
- Replay engine (deterministic simulation or direct exec).
- Advanced menus / library management.
- Efficiency extras + self-tests.
- Light integration points + packaging notes.
- Final sovereign texture + future-proof contract lock.

This keeps us focused, builds directly on the inspected commit, and delivers a solid, not-overgrown tool.

Next: user turns loose for Phase 2 implementation (or more details on approach). 

Repo now checked out + merged with latest (including the guide commit). All Phase 1 changes committed.