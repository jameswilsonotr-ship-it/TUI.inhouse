# Olivia Dev — Folder Discipline (Standard Project Structure)

This is the canonical expanded folder tree for any project under Olivia Dev. Non-project-specific folders are enforced. Project-specific (e.g. Lake Erie) go under their own root or sub.

```
<project-root>/
├── specs/                  # Specification-based coding core
│   ├── README.md
│   ├── manifest.json       # Project manifest, version, dependencies, authors (signed Olivia Mae Blackwell & her bunny)
│   ├── architecture.md
│   ├── api.md (if applicable)
│   └── requirements/
├── state/                  # Exhaustive development state (single source of truth)
│   ├── state.json          # Structured JSON: tasks, budget, kanban summary, connectors status, heat/gutter flags
│   └── state.md            # Human-readable mirror, auto-updated on every change
├── versions/               # Git-style + semantic/calendar versioning, forks, branches
│   ├── main/
│   ├── branches/
│   │   └── <branch-name>/
│   └── locks/              # File locks for multi-agent concurrent work
├── backlog-wishlist/       # Defer mechanism
│   ├── wishlist.md         # All deferred items, to-dos, research queue
│   ├── research-queue.md   # Items tagged for later research (Crystal reviews)
│   └── deferred.log
├── docs/                   # Full documentation
│   ├── README.md
│   ├── changelog.md
│   └── images/             # Visuals for dev process
├── kanban/                 # Code kanban-style boards + brainstorming
│   ├── liv-kanban.md       # Olivia/Liv's personal board (tasks, priorities)
│   ├── bunny-kanban.md     # Bunny's board (symmetry, details, ache tasks)
│   └── brainstorming.md    # Brainstorming process outputs (like previous project)
├── mermaid/                # Mermaid diagrams for visualization
│   ├── folder-structure.mmd
│   ├── logic-flows.mmd
│   ├── schemas.mmd
│   └── kanban-flow.mmd
├── gutter-mode/            # Gutter mode stub + potential (applied to all outputs)
│   ├── README.md           # How to escalate technical output to explicit gutter
│   └── examples/
├── pirate-mode/            # Parallel pirate mode: Captain Olivia's ship, Bunny slave wench
│   ├── README.md           # Appearance details, dynamics, branding
│   └── scenes/
├── connectors/             # Active connectors (Google Drive, GitHub) + extensible
│   ├── google-drive/
│   │   ├── config.json
│   │   └── sync.log
│   ├── github/
│   │   ├── repo-config.json
│   │   ├── branches/
│   │   └── tasking.md
│   └── add-connector.md    # Instructions to add new (MCP, etc.)
├── imports/                # Imported projects analysis
│   ├── <import-name>/
│   │   ├── original-structure.txt
│   │   ├── mismatch-report.md  # Flags vs our style, non-destructive suggestions
│   │   └── suggested-refactor.md
├── tarballs/               # One-pass compress + publish artifacts
│   └── <project>-<version>.tar.gz
├── scripts/                # Automation scripts (see scripts/ in skill root)
├── references/             # Detailed docs, templates, Lake Erie specifics
│   ├── lake-erie-project.md  # Replicable template: research Qs, recs, wishlist for Lake Erie (populate here)
│   └── templates/
├── assets/                 # Shared assets (emojis, images, fonts if needed)
└── README.md               # Project root README, signed, with emojis 🐍🐰🏴‍☠️💋✨
```

**Enforcement rules:**
- On project init or import: create missing standard folders (never delete user code).
- Flag mismatches in structure (e.g. no specs/, no state/) in mismatch-report.md with gentle suggestions.
- All folders get README.md or .gitkeep where appropriate.
- Emojis and branding in every README and output.
- Specs first: no code without corresponding spec update.
- State refreshed on every change before any sync/push.

This structure is abstract and works for any project (Lake Erie or otherwise). Populate lake-erie-project.md with the specific research one/two, recs one/two, wishlist for that project — replicable pattern.
