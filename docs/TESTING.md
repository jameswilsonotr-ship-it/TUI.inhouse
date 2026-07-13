# Testing — TUI.inhouse

**Updated:** 2026-07-13 · **PR-09**  
**Runner:** `scripts/run_harness.py`  
**Framework:** Python stdlib `unittest` (no pytest required)

---

## Quick run

```bash
cd /mnt/c/out/grokbuild/TUI.inhouse

# Prefer project venv (has textual for import smoke)
./.venv/bin/python scripts/run_harness.py

# Or system python3 (unit tests that need only stdlib + importable package path)
python3 scripts/run_harness.py
```

Expect **exit code 0** and a summary line `HARNESS OK`.

### Unit only

```bash
python3 -m unittest discover -s tests -v
```

### Product demo zip only (no TUI)

```bash
python3 AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
```

Interactive TUI / `--test` Phase-3 self-test still exist for humans; they are **not** required for CI-style harness green.

---

## Test layers

| Layer | Location | Needs Textual? |
|-------|----------|----------------|
| Unit pure | `tests/test_effects.py`, `test_layouts.py` | No |
| Config / zip | `tests/test_config.py`, `test_menus.py` | No (imports launcher module) |
| Contract | demo zip extract + harness subprocess | No |
| Optional smoke | `--create-demo` via runner flag | No |

---

## Writing new tests

1. Add `tests/test_<area>.py` with `unittest.TestCase`.  
2. Use `tempfile.TemporaryDirectory` — never write into live `.launcher_menus` unless intentional.  
3. Keep tests offline (no network).  
4. Cross-check public names in [API.md](./API.md).  
5. Re-run `scripts/run_harness.py`.

---

## Harness contract assertions (canonical)

See [HARNESS-CONTRACT.md](./HARNESS-CONTRACT.md):

- Demo zip extracts with `menu.json` → `main_script=harness.py`  
- `run_harness_once` with a chunk returns `exit_level == 0`  
- Missing harness → `exit_level == 1`

---

## Failures

| Symptom | Check |
|---------|--------|
| Import error `textual` | Activate `.venv` or `pip install -r requirements.txt` |
| Path errors | Run from repo root (`TUI.inhouse/`) |
| Zip permission | WSL `/mnt/c` sometimes slow — re-run once |

Logs for product crashes remain under `logs/` (not the unit harness).  
