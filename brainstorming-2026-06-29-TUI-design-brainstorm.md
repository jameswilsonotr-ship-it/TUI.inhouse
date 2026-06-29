# Brainstorming Session: TUI Design Files Review
**Date**: 2026-06-29
**Folder**: C:\Users\chast\#CODE\TUI
**Context**: Post-refactor cleanup. Reviewing kept design files for the modular robust Python TUI (Textual-based).
**User choice from clarifying**: B - Separate launcher.py (stdlib-only venv sniffing + re-exec + module discovery, then imports/runs the schema-driven app).

## Files Reviewed
- grok_tui_design_principles.md
- grok_tui_implementation_walkthrough.md
- textual_main_app_schema.py (with baby step runnable code)
- grok_tui.tcss
- FOLDER-STANDARDS.md (reference)
- Current README.md (post-cleanup)

## What Makes Sense (Strong Points)
- Extremely modular registration system (ModuleRegistration dataclass, REGISTERED_MODULE concept) aligns perfectly with request for "extremely modular set of components".
- Textual + Rich is the right choice for a robust TUI with screens, widgets, styling, async.
- Gutter Mode / Liv HUB / C-64 / sovereign branding is consistent and flavorful (toggleable visuals, status bar with Heat/Filth/Symmetry/Gem).
- Bootstrap philosophy in walkthrough (stdlib launcher, per-module venvs) is excellent for resilience.
- Schema/contract separation is good design practice.
- Baby step approach (minimal home grid + stubs) is pragmatic.
- Alignment to Grok Build 7-phases, roster, hardware, "wrap any".

## What Needs Clarification
- Relationship between the launcher.py described in walkthrough vs. the GrokBuildTUI class in schema.py.
- Dynamic discovery vs hardcoded in build_default_schema().
- Depth of "wrap any" feature.
- How real existing grok-build logic integrates vs reimplementation.
- Gutter Mode beyond CSS (real state driving visuals?).
- Status bar components: static or live data driven?

## Critiques
- Implementation in schema.py is partial (stubs, embedded CSS while .tcss exists, some code duplication).
- Design docs are aspirational; current code is early baby step.
- Need clearer boundaries between launcher bootstrap and app logic.

## Suggestions
- Keep schema pure (data only).
- Implement launcher.py per walkthrough as entry.
- Use the copied design .md as source of truth.
- Add proper module discovery.
- Plan test harness per Olivia Dev / sprint review.
- Start with core: launcher bootstrap + home + 1-2 screens using schema.

## Next Steps in Brainstorm (as of commit)
Continuing to refine based on choice B.
Will capture design decisions in this file and/or docs/.

This file documents the current brainstorming for commit.
