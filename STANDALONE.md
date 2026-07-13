# STANDALONE — TUI.inhouse

This package **must remain valid** when:

1. Nested under `/mnt/c/out/grokbuild` (or any monorepo), **or**
2. Checked out alone and edited as its own repository.

## Rules

1. Prefer **relative** paths inside this package.
2. Optional monorepo links go in `connectors/monorepo.md` (not required to build).
3. Do not require sibling folders to exist for enforcer / docs / specs / state.
4. Secrets never committed (`.env` gitignored).
5. `git init` is expected; remotes optional.

## Verify standalone

```bash
cd TUI.inhouse
python scripts/enforcer.py
test -f FOLDER-STANDARDS.md
test -f .research/dev-process-codified.md
test -d .aux/plans
test -f state/state.json || test -f state/state.md
```

## Init as repo

```bash
git init
git add .
git commit -m "chore: bootstrap TUI.inhouse under Olivia Dev discipline"
# git remote add origin <url>
```
