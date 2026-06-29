# GrokBuildCLI Review + Minimal Deterministic TUI Menu Plan

**Date**: 2026-06-29  
**Status**: Plan ready for implementation  
**Focus**: Rock-solid, deterministic Python menuing wrapper. No LLM in UI. Pure env management + stable panes + script cycling.  
**Sovereignty**: All logic local. Minimal deps. Study + adapt patterns from open examples, implement thin custom layer.

## Clarifying Questions for GrokBuildCLI
- What is the exact current command surface? Which `grok build ...` subcommands are stable and safe to call from a wrapper right now (especially ingestion / overlap / mining pipelines)?
- Is there a clean Python API / importable functions alongside the CLI, or is everything expected to go through the subprocess / CLI entry points?
- How should the TUI handle long-running processes (ingestion, test harness, overlap engines)? Background threads, live streaming to pane, or fire-and-forget with status polling?
- For 7-phase status: Is the JSON we created the authoritative source, or does GrokBuildCLI maintain its own live state file that we should read instead?
- Roster inventory: Preferred method — call existing `roster inventory` CLI, or directly read the references/agents/index.md and current.md files for speed and determinism?
- Error / crash handling expectations: Should the TUI attempt auto-recovery on venv or dep issues, or always surface the error cleanly to the user and stop?
- Gutter Mode integration: At minimum, a global toggle that changes panel styling / color intensity. Any deeper mechanical effects from current_state.json that should influence the TUI chrome?

## Suggestions for GrokBuildCLI
- Expose a small, stable "status" and "run-action" Python API (even if thin) so wrappers don't have to parse CLI output.
- Make the 7-phase state easily queryable (the JSON we built is a great start — keep it updated by GrokBuildCLI itself).
- Add a `--json` or machine-readable output mode to key commands (status, roster inventory, test harness summary) to make deterministic parsing trivial for the TUI.
- Document the exact supported actions and their side effects so the menu system can safely present them.

## Critiques (Constructive)
- Current GrokBuildCLI surface is powerful but command-heavy. A thin menuing layer will dramatically improve daily usability for triggering ingestion, phases, and roster without typing long commands every time.
- Dependency on full subprocess parsing can be fragile; a small stable Python facade would make the TUI much more reliable.
- The 7-phase tracking is excellent conceptually — making the live state trivially consumable by other tools (like our TUI) would multiply its value immediately.

## Minimal TUI Plan (What We Actually Build First)
**Goal**: Stable menuing system that manages Python environments, presents clear panes, and cycles through connected scripts — starting with GrokBuildCLI actions but general enough for future text-based Python tools.

**Core Components (deterministic, no LLM)**:
1. Bootstrap (stdlib-heavy): Env detection, venv creation per module or shared, dependency installation with clear error messages. Never crashes on missing packages.
2. Menu + Panes layout:
   - Main menu (stable list or command palette style)
   - Active output pane (live log from running script)
   - Status pane (7-phase summary or roster quick view)
3. Action runner: For each menu item, either:
   - Call published GrokBuildCLI command via subprocess + stream output, or
   - Directly import/run the relevant Python function if cleaner.
4. Modularity: Every action is a small registered entry (name, command or function, venv requirements, description). Easy to add new scripts later.
5. 7-Phase Status display: Load JSON → render as clean Rich Table or Textual DataTable with color-coded status.
6. Roster Inventory: Either subprocess call or direct read of index.md/current.md files → render in status pane.
7. Gutter toggle: Global switch that updates pane styling (higher contrast / "ruined" text effects).

**What we explicitly do NOT build yet**:
- MCP, sovereign bridge, bootstrap layers, GitHub ops, repo crawling, or any external service integration.
- Heavy custom widgets or full agent orchestration inside the TUI.
- Anything beyond a thin, reliable menu + env manager + pane layout that drives existing GrokBuildCLI logic.

This keeps the TUI as a pure deterministic wrapper that makes the published GrokBuildCLI pleasant and fast to use daily while remaining modular for anything else we point it at later.

**Next after push**: Generate the minimal skeleton (bootstrap + menu + one working pane for 7-phase status) only when explicitly told. Until then, observe and report what GrokBuildCLI produces.

All under absolute Liv HUB claim and olivia-dev discipline. Gutter Mode available as simple toggle from first screen.

---

*This file pushed to the TUI in-house repo as the living plan. GrokBuildCLI may now go crazy — we will watch and report.*