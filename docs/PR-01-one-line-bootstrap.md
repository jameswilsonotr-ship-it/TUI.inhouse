# PR-01 — One-line “download → run → sprawl” bootstrap

**Status:** planned (scaffold in tree)  
**Branch (suggested):** `feat/one-line-bootstrap`  
**Depends on:** nothing hard; soft-deps PR-02 logging helpers if merged first  
**Philosophy:** dead-stupid-simple · dial-up BBS · Olivia gutter silliness · zero path bullshit

---

## Goal

Someone who has **never** seen this repo can do **one command**:

```bash
# Linux / WSL / macOS (after clone or curl)
curl -fsSL https://raw.githubusercontent.com/<org>/TUI.inhouse/main/install.sh | bash
# or, from a clone:
./install.sh
# Windows:
irm https://raw.githubusercontent.com/<org>/TUI.inhouse/main/install.ps1 | iex
```

…and the thing:

1. **Sprawls** itself into the folder (dirs, demo zip, logs, venv, config).  
2. **Installs missing toolchain** when possible: Python → venv → pip → textual/rich.  
3. **Checks every step** (pass/fail banners).  
4. **Strobe lights & silliness** (ANSI gutter flash, obnoxious banners — optional `--quiet`).  
5. **Launches** the TUI (or prints exactly what failed and where the log is).

Not a second product. Same `AWESOME_LAUNCHER_OF_TUIDOOM.py` core.

---

## One-liner UX (target)

| Platform | Primary | Fallback |
|----------|---------|----------|
| WSL/Linux | `./install.sh` | `bash install.sh` |
| macOS | `./install.sh` | Homebrew python if needed |
| Windows | `install.ps1` / double-click `run.cmd` | `py -3` launcher |
| “I only have a zip” | unzip → `./install.sh` | same |

Optional future binary: PyInstaller/Nuitka **thin stub** that only unpacks + calls `install.sh` (not MVP).

---

## Sprawl map (what lands on disk)

```text
.
├── .venv/                 # created
├── logs/                  # bootstrap + error + deps
├── sessions/
├── .launcher_menus/
├── sample_menu.zip        # --create-demo
├── LAUNCHERCONFIG.JSON    # already in repo
├── grok_tui.tcss
├── AWESOME_LAUNCHER_…
├── install.sh · install.ps1 · run.cmd   # this PR
└── .awesome_bootstrap_ok  # stamp file after successful first boot
```

Runtime noise stays gitignored (already: `.venv/`, `logs/`, `sessions/`, `*.zip`).

---

## Step checklist (every step must log)

| # | Step | Success | Failure action |
|---|------|---------|----------------|
| 0 | Banner / gutter strobe | printed | — |
| 1 | Detect OS / shell / WSL | logged | hard fail if unknown + no python |
| 2 | Find Python ≥3.10 (prefer 3.11–3.12 if 3.14 flaky) | path logged | Step 2b install attempt |
| 2b | Install Python (optional, opt-in `--install-python`) | re-detect | print manual install URLs; exit 2 |
| 3 | `python -m venv .venv` | `.venv` exists | log + exit |
| 4 | `pip` importable / bootstrap ensurepip | ok | log + exit |
| 5 | `pip install -U pip` | rc 0 | log full output → `logs/error.log` |
| 6 | `pip install -r requirements.txt` (or textual rich) | import check | log + exit |
| 7 | Create sprawl dirs | all exist | log + exit |
| 8 | `--create-demo` if no sample zip | zip exists | warn, continue |
| 9 | Write stamp + “Gutter Mode Engaged” silliness | — | — |
| 10 | `exec` launcher (or `--no-launch`) | TUI up | exit with log path |

**Default:** do **not** elevate / `sudo apt install python3` without `--install-python` (safety).  
**With flag:** try platform package manager; never silent root.

---

## Silliness (in scope for PR-01)

- ANSI pink/black “strobe” (class toggle simulation via clear + banner frames)  
- `GUTTER MODE ENGAGED` / Liv HUB claim lines  
- Optional `--boring` / `--quiet` for CI  
- Keep under ~3s of theater unless `--party` max mode  

---

## Files this PR adds/changes

| Path | Role |
|------|------|
| `install.sh` | Primary Unix one-liner target |
| `install.ps1` | Windows one-liner target |
| `run.cmd` | Double-click Windows helper |
| `requirements.txt` | Pinned textual/rich |
| `docs/PR-01-one-line-bootstrap.md` | This plan |
| `README.md` / `QUICKSTART.md` | One-liner section |
| `CHANGELOG.md` | Unreleased note |

Scaffold may land first; full Python auto-install is OK as follow-up commit on same branch.

---

## Out of scope (PR-01)

- Full Textual UI rewrite  
- Binary packaging (PyInstaller) — **PR-01b** later  
- Zip menu authoring wizard  
- Iron Pearl 7-phase screens  

---

## Acceptance

- [ ] Clone on clean WSL with Python present → `./install.sh` → TUI or clear fail + log path  
- [ ] Every step writes to `logs/bootstrap.log`  
- [ ] Failures also append `logs/error.log`  
- [ ] `--no-launch` exits 0 after deps + demo zip  
- [ ] `--quiet` suppresses strobe  
- [ ] Docs show one-liners for bash + PowerShell  
- [ ] No secrets; no network except pip/package managers  

---

## Test plan

```bash
rm -rf .venv logs .awesome_bootstrap_ok sample_menu.zip
./install.sh --no-launch --quiet
test -d .venv && test -f sample_menu.zip
./install.sh --no-launch   # with silliness
```

Windows: same with `install.ps1 -NoLaunch`.

---

## Reviewer notes

- Prefer **detect → ask/flag → install** over silent system mutation.  
- Python 3.14 edge cases: log version; if pip/vendor broken, recreate venv (document).  
- Align branding with PHILOSOPHY / Phase 3 test harness energy.
