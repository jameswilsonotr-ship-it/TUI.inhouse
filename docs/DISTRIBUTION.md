# Distribution — wheels, wheelhouse, optional binary

**Updated:** 2026-07-13 · **PR-10**  
**Plan:** [PR-10-distribution-wheel.md](./PR-10-distribution-wheel.md)

Ship **AWESOME LAUNCHER OF TUI DOOM** as a normal Python distribution so deps arrive as **prebuilt wheels** where platforms support them (textual, rich, and transitive deps).

---

## Paths (pick one)

| Path | Who | Command sketch |
|------|-----|----------------|
| **A. Wheel** | Online machine | `pip install dist/awesome_tui_doom-*.whl` |
| **B. Wheelhouse** | Offline / air-gap | `pip install --no-index --find-links=wheelhouse awesome-tui-doom` |
| **C. Clone + install.sh** | Dev / monorepo | `./install.sh` (PR-01; unchanged) |
| **D. Frozen exe** | Optional later | PyInstaller/Nuitka — **PR-10b**, not required |

---

## Build (releaser)

From repo root (`TUI.inhouse/`):

```bash
# Dev venv recommended
python -m pip install -U pip build wheel

# sdist + wheel → dist/
python scripts/build_dist.py

# Also pack product + all dependency wheels for offline install
python scripts/build_dist.py --wheelhouse
```

Outputs (gitignored):

```text
dist/
  awesome_tui_doom-X.Y.Z-py3-none-any.whl
  awesome_tui_doom-X.Y.Z.tar.gz
wheelhouse/          # only with --wheelhouse
  *.whl              # product + textual + rich + …
```

---

## Install (operator)

### Online (from a built wheel file)

```bash
python -m venv .venv-run
source .venv-run/bin/activate   # Windows: .venv-run\Scripts\activate
python -m pip install dist/awesome_tui_doom-*.whl
awesome-tui --create-demo
awesome-tui
```

### Offline wheelhouse

```bash
python -m venv .venv-run
source .venv-run/bin/activate
python -m pip install --no-index --find-links=wheelhouse awesome-tui-doom
awesome-tui
```

### Still supported: git checkout

```bash
./install.sh
# or
python AWESOME_LAUNCHER_OF_TUIDOOM.py
```

---

## Entry points

| Console script | Purpose |
|----------------|---------|
| `awesome-tui` | Launch product (bootstrap + TUI) |
| `awesome-tui-harness` | Run unit/contract harness (PR-09) |

If entry points are missing after install, run module form:

```bash
python -m awesome_tui
```

(Scaffold may expose module path via `pyproject.toml` `[project.scripts]`.)

---

## What is “precompiled” here?

| Layer | Precompiled? |
|-------|----------------|
| **Dependency wheels** (textual, rich, …) | Yes — platform wheels from PyPI / wheelhouse |
| **Our package** | Pure Python wheel (`py3-none-any`) unless we add native extensions later |
| **Frozen binary** | Optional PR-10b — embeds interpreter + deps in one executable |

You do **not** need to compile C extensions for this product today.  
“Wrapped with all dependencies through wheel” = **declare deps in the wheel metadata** + optional **wheelhouse** so every install is wheel-only.

---

## Verify after install

```bash
awesome-tui-harness
# or from source tree still:
python scripts/run_harness.py
```

Expect `HARNESS OK`.

---

## Version / release checklist

1. Bump version in `pyproject.toml` and CHANGELOG.  
2. `python scripts/run_harness.py` → green.  
3. `python scripts/build_dist.py --wheelhouse`.  
4. Smoke-install into a **fresh** venv from `dist/` or `wheelhouse/`.  
5. Tag `vX.Y.Z` if cutting a release.  
6. Do **not** publish to public PyPI unless explicitly approved.

---

## Related

- [ARCHITECTURE.md](./ARCHITECTURE.md)  
- [PR-01-one-line-bootstrap.md](./PR-01-one-line-bootstrap.md)  
- [TESTING.md](./TESTING.md)  
