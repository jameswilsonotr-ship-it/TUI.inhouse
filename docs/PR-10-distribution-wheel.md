# PR-10 — Distribution (wheel / precompiled Python + deps)

**Status:** planned (scaffold in tree)  
**Branch (suggested):** `feat/distribution-wheel`  
**Depends on:** PR-09 (tests green before cut); soft-deps PR-01 install story  
**Philosophy:** zero path bullshit for *operators* · pip/wheel first · optional frozen binary later · no bloat  

---

## Goal

Ship the launcher so someone can install **without cloning the monorepo**:

1. **Primary:** installable **Python package (wheel)** with declared deps (`textual`, `rich`).  
2. **Offline / air-gap:** a **wheelhouse** (directory of wheels for product + all deps) + one `pip install --no-index` command.  
3. **Optional later (PR-10b):** single-file frozen binary (PyInstaller/Nuitka) that embeds a runtime — only if wheel path is not enough for cab/OTR machines.

Not a second product. Same AWESOME core + `tui_chrome`.

---

## Deliverables

| Artifact | Purpose |
|----------|---------|
| [`pyproject.toml`](../pyproject.toml) | Project metadata, deps, console entry points, build backend |
| [`MANIFEST.in`](../MANIFEST.in) | Non-Python data (TCSS, default config, docs snippets) |
| [`docs/DISTRIBUTION.md`](./DISTRIBUTION.md) | Operator + releaser instructions |
| [`scripts/build_dist.py`](../scripts/build_dist.py) | Build sdist/wheel + optional wheelhouse |
| `dist/` (gitignored) | Build outputs |
| `wheelhouse/` (gitignored) | Offline bundle of wheels |

### Console entry points (target)

| Command | Maps to |
|---------|---------|
| `awesome-tui` | `AWESOME_LAUNCHER_OF_TUIDOOM:main` (or thin wrapper) |
| `awesome-tui-harness` | `scripts.run_harness` / test runner |

Exact module path may use a small `src/awesome_tui/` package layout in a follow-up commit if flat-repo packaging proves fragile; scaffold keeps **flat + package-dir** mapping first.

---

## Distribution modes

### A — PyPI-style wheel (default)

```bash
python -m pip install build
python scripts/build_dist.py            # → dist/*.whl + dist/*.tar.gz
python -m pip install dist/awesome_tui_doom-*.whl
awesome-tui --create-demo
```

Deps install from PyPI as **their** wheels (precompiled where available).

### B — Offline wheelhouse (all deps pre-downloaded)

```bash
python scripts/build_dist.py --wheelhouse
# produces wheelhouse/*.whl including textual, rich, …
python -m pip install --no-index --find-links=wheelhouse awesome-tui-doom
```

### C — Frozen binary (optional, not MVP of this PR)

```bash
# PR-10b — only after A/B stable
pyinstaller --onefile …   # or Nuitka
```

Keeps **PR-01b** / thin stub notes aligned: frozen binary is optional; wheel is the main story.

---

## Package data (must ship inside wheel)

| File | Why |
|------|-----|
| `LAUNCHERCONFIG.JSON` | Default search paths / dirs |
| `grok_tui.tcss` | Gutter / chrome styles |
| `tui_chrome/chrome.tcss` | Gallery chrome |
| `requirements.txt` | Optional pin reference |
| Short docs: `PHILOSOPHY.md` / `QUICKSTART.md` | Operator help offline |

Generated at runtime (not in wheel as required content): `.venv/`, `logs/`, `sessions/`, extracted menus.

Demo zip: either generate on first run (`--create-demo`) or include a tiny `sample_menu.zip` as package data if size stays small.

---

## Versioning

- Semantic version in `pyproject.toml` aligned with CHANGELOG (`0.1.6` → bump on release).  
- Tag `vX.Y.Z` when cutting a wheel.  
- `scripts/run_harness.py` must pass on the **installed** package (smoke: install wheel into clean venv + run harness if exposed).

---

## Acceptance

- [ ] `python scripts/build_dist.py` produces at least one `.whl`  
- [ ] Clean venv: `pip install dist/*.whl` succeeds  
- [ ] `awesome-tui --help` or equivalent entry works  
- [ ] `--wheelhouse` downloads/builds dependency wheels offline-installable  
- [ ] `docs/DISTRIBUTION.md` documents A/B (and notes C as optional)  
- [ ] `dist/` + `wheelhouse/` gitignored  
- [ ] PR-09 harness still green from source tree  

## Non-goals

- Publishing to public PyPI without explicit operator approval  
- Approving wrap-any (P-20) or 7-phase+roster (P-21)  
- Replacing `install.sh` (it remains clone/bootstrap path; wheel is alternate)

## See also

- [DISTRIBUTION.md](./DISTRIBUTION.md)  
- [PR-01-one-line-bootstrap.md](./PR-01-one-line-bootstrap.md) (install.sh path)  
- [TESTING.md](./TESTING.md)  
