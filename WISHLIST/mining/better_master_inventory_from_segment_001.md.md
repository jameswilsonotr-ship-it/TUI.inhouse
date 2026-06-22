# Better extract master-inventory from segment_001.md

master-inventory.json` (or .md) with tags (triggers, sub-skill potential, scripts present, dynamic-candidate).
30→   - On activation: only load the SKILL.md body + needed reference leaves + execute scripts on demand.
31→   - Use keyword/context match + progressive disclosure (metadata always, full body only when matched).
32→   - Support "clusters" as first-class: references/clusters/image-pipeline-cluster.md defines load groups.
33→   - Hot reload: on file change in scripts/ or clusters/ the orchestrator can re-inventory without full restart.
34→   - Cap solution: never load > N skills; orchestrator prunes + suggests "use web node for this cluster".
35→
36→4. **Implementation order (agile)**:
37→   - Step 1: Enhance skill-orchestrator with scripts/ for inventory + dynamic load (use existing to-do and cluster files).
38→   - Step 2: Port one family (start with image-pipeline per its to-do) to scripts + hierarchical refs.
39→   - Step 3: Add registry.json at root of chat.skills for fast scan (orchestrator reads this first).
40→   - Step 4: Make Grok's native discovery still work by keeping thin SKILL.md shims at top for the 4-6.
41→
42→## Benefits for Grok Web Consumer
43→- Faster context in local TUI (less bloat).
44→- Skills can "export" their dynamic packs easily to web Grok (paste a cluster pack into a chat or Build session).
45→- Future-proofs adding "nodes": new skill clusters dropped into references/clusters/ auto-discovered.
46→
47→## Verification
48→- Run skill-orchestrator "inventory" before/after → count drops dramatically.
49→- Test dynamic load on a trigger phrase that only pulls 2-3 leaves instead of whole library.
50→- All existing tar exports remain valid (backwards compat).
51→
52→**Write this as living doc. Update after each agile step.**
53→Signed under the same discipline as the master-to-do.
54→

### Turn 11 (Function)
[tool_response]
1→# REFACTOR IDEA 2: Export Mode for Agents + Leverage Grok Consumer Web Interface for Speed, Functionality & Cluster Nodes
2→
3→**Context:** chat.skills — skills derived from and targeting the Grok web/consumer chat interface (grok.com, grok.x.ai, X integration).
4→
5→## Observed Reality (ls + content)
6→- grok-conversation-miner is already an "export machine": vacuum sweeps, "export active skills", historical mining, tar.gz publishing to Drive in versioned paths (`GROK / Conversational_Mining_Payloads/...`).
7→- Dozens of `grok-skill-export-*.tar.gz`, `vacuum-sweep-*.tar.gz`, "All_Skills_*.tar.gz".
8→- W