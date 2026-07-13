# PR-02 — Error handling, reconnaissance & step telemetry

**Status:** planned (partial land already in `ensure_deps` logging)  
**Branch (suggested):** `feat/bootstrap-error-recon`  
**Depends on:** PR-01 preferred first (or merge logging core first, bootstrap shell second)  
**Philosophy:** if it fails, you know **exactly** which step, **why**, and **what to run next**

---

## Goal

Make bootstrap + launcher **recon-grade**:

1. Every step has a name, start/end timestamp, pass/fail.  
2. Failures always hit **console tail + `logs/error.log` + structured JSON**.  
3. “Reconnaissance report” on demand: env, python, pip, disk, network-ish, textual import.  
4. No more silent `DEVNULL` on critical paths.  
5. Optional `--recon-only` produces a report **without** launching the TUI.

This is the **brains**; PR-01 is the **one-line face**.

---

## Layers

```text
install.sh / install.ps1     → step runner (shell)
        ↓
python -m tools.recon        → deep recon (optional pure python)
        ↓
ensure_deps / bootstrap.py   → pip + import checks (python)
        ↓
logs/
  bootstrap.log              # full narrative
  bootstrap_deps.log         # raw pip
  error.log                  # failures only (+ BOOTSTRAP DEP FAILURE)
  recon-report.json          # machine-readable
  recon-report.md            # human
```

---

## Recon report contents

| Section | Data |
|---------|------|
| Host | OS, WSL?, arch, cwd, user |
| Python | path, version, implementation, venv? |
| Pip | version, path, can import self |
| Deps | textual/rich importable? versions |
| Disk | free space on project root |
| Network | can reach pypi.org? (optional timeout 3s) |
| Tree | expected files present? (launcher, tcss, config) |
| Runtime dirs | logs/sessions/menus/venv exist? |
| Last errors | tail of `logs/error.log` |
| Suggested next | copy-paste commands |

---

## Step protocol (shared)

Each step emits:

```text
[STEP 05/10] pip-install-core ... RUNNING
[STEP 05/10] pip-install-core ... PASS (12.4s)
# or
[STEP 05/10] pip-install-core ... FAIL (rc=1)
  → see logs/error.log
  → tip: rm -rf .venv && ./install.sh --no-launch
```

JSONL optional: `logs/steps.jsonl` one object per step.

---

## Files this PR adds/changes

| Path | Role |
|------|------|
| `scripts/recon.py` | Recon CLI → JSON + MD |
| `scripts/step_log.py` or shell helpers | Shared step formatting |
| `AWESOME_… ensure_deps` | Already improved; extend to shared module |
| `bootstrap.py` (optional extract) | Shared by shell + python entry |
| `docs/PR-02-error-recon.md` | This plan |
| `docs/TROUBLESHOOTING.md` | Human map from symptoms → fixes |

---

## Acceptance

- [ ] `./install.sh --recon-only` or `python scripts/recon.py` writes recon-report.{json,md}  
- [ ] Forced failure (bad pip index / missing network mock) leaves clear step name + logs  
- [ ] `logs/error.log` contains `BOOTSTRAP` marker and pip stderr  
- [ ] TROUBLESHOOTING covers: broken pip._vendor.rich, no python, WSL, Windows py launcher  
- [ ] CI job: recon-only on ubuntu  

---

## Relationship to existing code

| Already landed (2026-07-13) | Still needed |
|----------------------------|--------------|
| `ensure_deps` full pip capture | Shell step runner |
| `logs/bootstrap_deps.log` | `scripts/recon.py` |
| `logs/error.log` on dep fail | JSONL steps |
| Import check post-install | Network/disk recon |
| smoke-results/DEP-ERROR-LOGGING.md | TROUBLESHOOTING.md |

---

## Acceptance scenarios

1. **Happy path:** recon shows all PASS; install --no-launch succeeds.  
2. **Broken venv:** recon flags pip import error; tip says `rm -rf .venv`.  
3. **No textual:** recon FAIL deps; install repairs.  
4. **No python:** recon FAIL; install without `--install-python` exits 2 with URLs.

---

## Non-goals

- Centralized cloud crash reporting  
- Auto-filing GitHub issues  
- Changing zip harness exit-level semantics (already OK)
