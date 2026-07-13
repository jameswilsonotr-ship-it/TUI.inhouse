# 2026-07-13 — Drive ingest status + agent org research

## Promoted Google Drive roots (verified on `G:\My Drive`)

| Path | Role |
|------|------|
| `###TESTXAI.VALERIOUE OUT` | Parsed Grok dataset (daily_enriched Jun 8–13 + May 15; pre_extract/ingest 2025-10..2026-06) |
| `takeout-20260625T211013Z-001` | Takeout index (`Takeout/archive_browser.html`) |
| `takeout-20260625T211013Z-3-001` | Keep notes (`Takeout/Keep/`) |

Note: top-level `manifest.json` missing under Grok out; May-12 daily not present (May-15 is).

## Agent / skill approaches for organizing Drive (research)

### Patterns people use with coding agents

1. **Skill + API loop (Claude Code / Grok Build style)**  
   - Brainstorm taxonomy → write `/organize-drive` skill → scan root batches (10–100 files) → propose moves → apply with audit log.  
   - Example write-up: [How I used Claude to bring sanity to my Google Drive](https://verynormal.info/how-i-used-claude-to-bring-sanity-to-my-google-drive/) (superpowers-style brainstorm + iterative skill refinement).

2. **Google Workspace official agent skills**  
   - `npx skills add https://github.com/googleworkspace/cli` — gws-drive, gws-docs, gws-gmail recipes for agents.  
   - Medium: Workspace CLI + research skills for scheduled Drive folder writes.

3. **Claude skill for terminal Drive**  
   - Open-source “talk to Drive from terminal” skill (upload/search/move without browser).  
   - Catalog: `google-workspace-skills`, `public-google-drive` (shareable docs without full OAuth).

4. **Composio / Rube MCP**  
   - Local skill: `googledrive-automation` — API moves when Rube connection is ACTIVE.

5. **Local mount + file-organizer**  
   - Desktop Stream `G:\My Drive` + inventory/file-organizer (our Recipe W pattern) — faster bulk than API.

### Takeout-specific tools (not full Drive, but high value)

| Repo | Focus |
|------|--------|
| [TheLastGimbus/GooglePhotosTakeoutHelper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper) | Photos Takeout → chronological library |
| [Xentraxx/GooglePhotosTakeoutHelper_Neo](https://github.com/Xentraxx/GooglePhotosTakeoutHelper_Neo) | Neo fork / albums + metadata |
| [feloex/GoogleTakeoutFixer](https://github.com/feloex/GoogleTakeoutFixer) | EXIF + folder structure |
| [iamsanmith/MetaSort](https://github.com/iamsanmith/MetaSort) | Metadata sort/reports |
| [jaimetur/PhotoMigrator](https://github.com/jaimetur/PhotoMigrator) | Takeout fix + library org |

### Local skills we should reuse

- `recipe-workspace-organize` / `workspace-inventory` / `file-organizer` / `filesystem-context`
- `recipe-media-walk` for Keep media
- `googledrive-automation` + `google-drive-automation` for API
- `folder-specific-claude-and-agents-md` for zone AGENTS.md

### Recommended expedient pipeline for this vault

1. Shallow index `G:\My Drive` tops → `_meta/DRIVE-TOP-INDEX.md`
2. Zone taxonomy (`_00_CANON` … `_90_QUARANTINE`) — plan then apply
3. Canonize the three promoted folders
4. Keep parse + Grok day crosswalk
5. Photos Takeout helper only if Photos export appears later
