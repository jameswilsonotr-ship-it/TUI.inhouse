# Better extract inventory-normalization from segment_001.md

inventory-normalization.md
- content: # Session Notes: Skill Inventory Normalization — 2026-06-21

**Date / Context:** 2026-06-21 (post ROSTER BOOT re-execution + memory_2026-06-21.md highlight + Canva correction).  
Liv HUB full narrative command. C-64 / Gutter Mode active. Triad (Grok • Liv • One).  
Previous work: cluster-map.md created, web-skill-template.md, cloud-history-search-request-corrected.md (pure Grok Imagine/Flux, no Canva), image-pipeline-cluster.md updated.

**User Directive (exact):**  
"the first thing we should do is to normalize the skill inventory look at olivia-dev and olivia-dev-alpha carefully is there anything in there that is salvageable also you should be taking notes in a notes folder of our conversation right now so we don thave to do it again"

**Actions Taken This Session:**
- Created `chat.skills/notes/` folder.
- This file is the living session log for current conversation and normalization work.
- Performed careful audit of olivia-dev and olivia-dev-alpha.
- Cross-referenced against existing cluster-map.md, REFACTOR-IDEA-*.md, skill-orchestrator, image-pipeline family, chaos-bratz-roster.
- Began normalization of inventory (categorized audit + recommendations).
- All work under absolute Liv HUB claim. Pure internal Grok Imagine/Flux for media.

---

## 1. Olivia-Dev vs Olivia-Dev-Alpha Audit (Careful Review)

### Common Core (Both Skills — Highly Salvageable)
The two SKILL.md files are ~95% identical. This is the "Sovereign development methodology" (Pretty Hacker Girl / Blackwell Code / Olivia Dev mode).

**Strongly Salvageable Elements (directly applicable to skill inventory normalization + web skill refactor):**

- **Folder Discipline** (references/folder-discipline.md — identical in both)
  - Canonical project tree: specs/, state/ (state.json + state.md mirror), versions/, backlog-wishlist/, docs/, kanban/ (liv-kanban + bunny-kanban + brainstorming), mermaid/, gutter-mode/, pirate-mode/, connectors/, imports/, tarballs/, scripts/.
  - Enforce on init/import. Specs first. All READMEs signed.
  - **Use for us**: Adapt to every skill folder in chat.skills/ per REFACTOR-IDEA-3. Many current skills are missing README.md, TODO.md, scripts/. This gives the exact template.

- **Image QC Checklist** (references/image-qc-checklist.md)
  - Strict process: generate → view_image → check vs locked Bible (hair, ears timing, drift, moderation) → max 2 loops (edit/re-gen or apologetic drift image) → auto-save good ones.
  - Self-budget