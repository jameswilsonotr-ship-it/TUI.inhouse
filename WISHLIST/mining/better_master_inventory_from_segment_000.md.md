# Better extract master-inventory from segment_000.md

master-inventory.md as table or categorized list (Bundled | User Custom | Image Pipeline Family | Swarm Family | MCP Family | etc.) with links to per-skill audits.
30→5. Output summary in C-64 bordered block: total skills, categories, high-duplication flags, dynamic loading recommendations.
31→
32→## Dynamic Skill Loading Architecture
33→- Hierarchical: Parent skills (e.g. image-pipeline, swarm-*) have references/subskills/ or mirrors/ with child .md or sub-dirs.
34→- Context-triggered: On user input, match keywords/triggers from inventory tags → load only matching SKILL.md body + relevant references/ leaves (progressive disclosure from skill-creator spec).
35→- Orchestrator decides load order/priority to stay under context caps.
36→- Global vs per-skill mirrors: 
37→  - Per-skill: e.g. chaos-bratz-roster/references/mirrors/olivia.md (Liv HUB), bunny.md etc for roster-specific personas.
38→  - Global: Create /home/workdir/.grok/references/mirrors/ (or under this skill's references/global-mirrors/) for shared canonical personas (Liv, Bunny, Valerie, Crystal, Echo, Mira) used across multiple skills. Orchestrator syncs and versions them. Preferred for de-duplication of persona DNA.
39→- Scripts in sub-dirs can be executed directly (bash/python) without full load for efficiency.
40→
41→## De-Conflict & Duplication Management
42→- Scan for overlapping functionality (image styles, swarm orchestrators, MCP bridges, format rules).
43→- Recommend consolidation: e.g. merge image style lists into image-style-orchestrator as sub-variants; centralize swarm logic in iron-pearl-swarm or new hub; move shared formatting to format-bible enforcement.
44→- Flag in audits and propose updates via skill-creator process.
45→
46→## Interaction with format-bible
47→format-bible is the canonical source for output standards: C-64 ANSI bordered blocks (╔═╗ style), 1st/last line ALWAYS 🐍, [TOP: 🌡️Heat|💦Filth|🔗Kink|🚨Safety|✨Gem] and [BOTTOM: ⚙️Mode | 🤖Agents | ⏱️Clock: Day X/60] every turn, NO SUMMARIES rule, Gutter Mode, test harness references. 
48→The skill-orchestrator MUST reference and enforce format-bible in all its outputs, new skill templates, and recommendations. This eliminates duplication of formatting logic across skills (many image and swarm skills re-implement borders). New skills created via this orchestrator inherit format-bible compliance by default. Update format-bible if new standards emerge from orchestration needs.
49→
50→## Mirrors Creation (Global or Per-Skill)
5