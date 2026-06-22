# WISHLIST / Mining Task: Mine .grok/sessions for chat.skills crash data to un-fuckify committed versions

**Date**: 2026-06-22
**Priority**: High (part of cleanup from first big project crash)
**Related**: chat.skills dir (the crashed project), .grok/sessions/* (hunk_records, edits during crash), committed in github (sovereign-skills, grok, olivia-dev*, sovereign-*, grok-nyxelle etc.) and local backups.

## Problem
The "first big project" (chat.skills) crashed during heavy refactoring/ingestion.
Many sessions have raw edit hunks, refactor ideas, inventory, cluster maps, normalization scripts etc. to chat.skills files.
The committed versions (in github repos just made public, and local chat skills backup / sovereign-skills-archive) may be incomplete, partial, or "fucked" from the crash.
Need to mine the session artifacts vs committed to restore/fix ("un fuckify").

## Scope (only this session's work + directed)
- Do not touch unrelated.
- Focus on skills refactoring, inventory, clusters, REFACTOR-IDEA-*, cloud-history, skill-orchestrator, etc. from the sessions around 2026-06-21.

## Tasks
1. Locate all relevant sessions (grep for chat.skills edits, specific session ids from hunk_records).
2. Extract useful data: full refactors, ideas (REFACTOR-IDEA-1,2,3), inventory, clusters, normalization scripts, PII scrubbed versions, etc.
3. Compare to current committed in:
   - github sovereign-skills, olivia-dev*, grok-*, etc.
   - local #CODE/OLIV.DIVA copies, chat skills backup, sovereign-skills-archive tarballs.
4. Identify diffs/gaps.
5. Produce fixes/patches or updated files to apply to the committed locations.
6. Document in central place (OLIV.DIVA or sovereign-skills).
7. Update WISHLIST / plans with results.

## Output
- Mined artifacts in WISHLIST or dedicated mining/ dir under OLIV.DIVA or TUI.
- Patches or fixed files.
- Report on what was unfuckified.
- Add to SSoT index.

## How to mine (for subagents)
- Use grep/rg on .grok/sessions for patterns like "chat.skills/REFACTOR", "hunk_records.jsonl", session ids.
- Parse jsonl for added/removed lines.
- Cross ref with committed files (use git show or github contents).
- For large, use subagents per session or per skill cluster.

**Status**: New task from user directive. Part of plan v0001.

See main plan for overall.
