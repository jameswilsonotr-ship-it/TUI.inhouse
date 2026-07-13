# FOLDER STANDARDS

**Applies to**: All projects using this development environment.  
**Related**: See `.research/dev-process-codified.md` for the full codified development process (this document is the companion reference).

## Purpose
Define canonical folder layout, dot-directories, and organization rules that enable the parallel agentic dev process, CQCS, reviews, and reusability.

## Required Top-Level Structure

- `FOLDER-STANDARDS.md` (this file) - Root reference. Update when layout evolves.
- `.research/` - Codified process, schemas, templates, skills docs.
  - `dev-process-codified.md` (MANDATORY - full engine spec)
  - `schemas/` - JSON/YAML schemas for plans, reports, dispatches (olivia-dev-alpha enforced)
  - `templates/` - Report/plan templates
  - `skills/` - dispatching-parallel-agents.md, requesting-code-review.md, sentry-*.md etc.
- `.aux/` - Auxiliary runtime artifacts (never committed as primary source, but git-tracked for history).
  - `plans/` - **MANDATORY location for recurring CQCS + phase reports**.
    - `<phase>-plan.md`
    - `<phase>-report-YYYYMMDD-HHMM.md`
  - `archive/` - Parked/killed work (Hunter-Killer moves here).
  - `scratch/` - Transient parallel subagent outputs.
  - `logs/` - Dispatch, kill, review logs.
- `src/` or language-specific (e.g. `app/`, `lib/`) - Primary implementation.
- `scripts/` - Includes `enforcer*` (see below), dispatch helpers.
- `docs/` - Human-facing (cross-ref the codified process).
- `.aux/plans/` must be populated before any commit involving changes.

## Dot-Directories Rules
- All `.aux/`, `.research/` are **project-owned** and portable (copy to new repos).
- Never put generated build artifacts here; use `.gitignore` appropriately.
- Hidden dirs enable the engine without polluting visible project tree.

## Integration with Codified Process
**See `.research/dev-process-codified.md`** for:
- Full loop: plan → parallel subagents (8-12 via spawn_subagent) → reviews → phase report → commit → scan.
- Hunter-Killer usage (safe kills only, logged in .aux).
- Mandatory phase reports + CQCS in `.aux/plans/`.
- Review skills (`requesting-code-review`, `sentry-*`) at milestones.
- `dispatching-parallel-agents` skill usage.
- Terminal aggression + enforcer on **every output**.
- olivia-dev-alpha discipline, flags, and schema enforcement.
- Reusable engine copy instructions.

**All folder decisions must support** parallel dispatch, safe Hunter-Killer, and gate enforcement.

## Enforcer
- The `enforcer` (in `scripts/enforcer.sh` or equivalent) **MUST** be run on containing folders after any structural or document edits.
- Typical: `enforcer .` or `enforcer .research .aux FOLDER-STANDARDS.md src/`
- Enforcer validates:
  - Presence of required dot dirs and reports.
  - References between FOLDER-STANDARDS.md and dev-process-codified.md.
  - No violations of naming or layout.
  - CQCS / olivia-dev-alpha schema compliance on reports.
- Failure blocks progression in the loop.

## Usage Examples

### Example: Bootstrap New Project with Engine
```bash
# From a source project that has the codified process
cp -r source/.research target/
cp -r source/.aux target/
cp source/FOLDER-STANDARDS.md target/
mkdir -p target/.aux/plans target/scripts
# Copy enforcer and skills if not already in .research
cd target
# Edit FOLDER-STANDARDS.md if project-specific folders needed (e.g. add `hardware/`)
./scripts/enforcer.sh .   # Run enforcer on containing folders
# Create initial phase plan + report
```

### Example: During Active Parallel Work
```
# Layout in use:
.aux/
  plans/
    feature-x-plan.md
    feature-x-report-20260621-1430.md   <--- produced by loop
    feature-x-report-20260621-1515.md
  archive/
    dead-subagent-03-notes.md
.research/dev-process-codified.md   <--- reference from prompts
FOLDER-STANDARDS.md
src/
scripts/enforcer.sh
```

### Example: Adding a New Folder Type
1. Update FOLDER-STANDARDS.md with description + justification.
2. Update `.research/dev-process-codified.md` if it impacts the loop / CQCS.
3. Add example usage.
4. Run enforcer on root + .research + .aux .
5. Create phase report noting the change.
6. Commit referencing the report.

### Example: Hunter-Killer + Folder Hygiene
- Dead work found in `scratch/old-experiment/` → Hunter-Killer moves to `.aux/archive/` (never deletes root files directly).
- Update `.aux/plans/hunter-activity.log`
- Enforcer run confirms no stray dirs violate standards.

## Enforcement Notes
- Root must always have `FOLDER-STANDARDS.md` + `.research/dev-process-codified.md` (or symlinks in monorepos).
- Phase reports in `.aux/plans/` are **non-negotiable**.
- When copying engine to other projects (LIV, Coven, new repos), replicate exact dot-folder layout for consistency.

## Test Harnesses Convention (Phase 4.5 Addition)
**Applies to**: All test harnesses (regression, validation, image-pipeline, grok-imagine, biomimetic, etc.) and their analysis artifacts.
**Justification**: Phase 4.5 formal analysis locked rules into stone. Harnesses are first-class deliverables and must themselves obey the full engine (prevents drift in testing layer).

- **Structure**: Harness concepts live under e.g. `harnesses/<concept>/` or skill-local `test-harness/` (respect <=5 files/concept: TOC/README + runner + seeds + schema + cqcs-template). Use subdirs only if count would exceed.
- **Blade Law on Harnesses**: Every harness file + runner MUST carry full header (version, timestamps, synthetic note, PII PASSED), cross-TOC, feature flags section, expandable schema (JSON for cases/metrics), character prompt ref where creative/subjective.
- **CQCS + Synthetic + PII**: Harnesses use synthetic data exclusively. Runner must enforce + report PII scan. Include CQCS checklist pass in every run report.
- **CI Runnability**: Runners provide flag-driven entrypoints (e.g. `--synthetic --cqcs --report-json --character=...`). Exit codes + JSON reports for pipelines. Archive to `.aux/plans/`.
- **Character / In-Char**: Image/creative harnesses (e.g. prompt seeds for overlay/gutter/velvet) ref C64-demo vibes + format bible.
- **Enforcer**: Mandatory post-edit on harness dirs + reports.
- **Examples / Mapping**: See `.research/test-harnesses-analysis.md` (Phase 4.5 locked stone). Existing (proxy) parser unittests, validation tables, prompt-seed collections map to template with gaps noted only.
- **Update Process**: Any new harness convention change: edit here + analysis doc + run enforcer + phase report.

**Example Usage**:
```
harnesses/image-pipeline-regression/
  README.md
  runner.py
  seeds.yaml
  schema.json
  cqcs-template.md
# Run: python -m harnesses.image_pipeline_regression.runner --synthetic --cqcs
```

Update `.research/dev-process-codified.md` (cross-ref) and `self.research/` indices when adding harness topics.

**This standards file + the codified process doc together form the portable development engine.**

See `.research/dev-process-codified.md` for complete details, full loop, and copy instructions.
