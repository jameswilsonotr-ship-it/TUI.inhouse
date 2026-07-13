# Harness contract — zip menus (legacy + bridge)

**Updated:** 2026-07-13 · **PR-07** (bridge clarified **PR-11**)  
**Implemented by:** `run_harness_once` / `run_chunked_harness` / `extract_menu_zip`  
**Public map:** [API.md](./API.md)  
**v1 menu system (preferred for new packs):** [menu-system/MENU-SYSTEM.md](./menu-system/MENU-SYSTEM.md)

Legacy `main_script` packs remain valid. New packs SHOULD use `schema_version: "1.0.0"` and `menus[]`; the action type `legacy_harness` bridges to this CLI.

---

## Zip layout

Minimum viable menu zip:

```text
my-menu.zip
├── menu.json          # required for custom main_script (recommended)
├── harness.py         # default main script
└── (optional assets)
```

### `menu.json`

```json
{
  "name": "demo-memory-processor",
  "description": "Human label",
  "main_script": "harness.py",
  "version": "0.1.0"
}
```

| Field | Required | Default |
|-------|:--------:|---------|
| `main_script` | no | `harness.py` |
| `name` | no | zip stem |
| `description` | no | — |
| `version` | no | — |

If `menu.json` is missing or invalid, launcher still extracts and looks for `harness.py`.

---

## Harness CLI (subprocess)

Launcher invokes (from extracted dir):

```bash
python <main_script> [--chunk YYYY-MM-DD] --log-dir <path>
```

| Arg | Meaning |
|-----|---------|
| `--chunk` | Optional single day (`ISO date`). Omitted = harness-defined full/default run |
| `--log-dir` | Directory for harness logs (created by launcher) |

### Exit codes (launcher mapping)

| Process `returncode` | `exit_level` | Meaning |
|---------------------:|-------------:|---------|
| `0` | `0` | Success |
| `2` | `2` | Partial (non-fatal; chunked loop may continue) |
| other | `1` | Hard error (chunked loop **stops**) |

Timeout: **120s** per `run_harness_once` invocation.

---

## Chunked ranges

`run_chunked_harness(start, end)` walks inclusive ISO dates day-by-day.  
On hard error (`exit_level == 1` and `returncode != 2`) the loop breaks.

---

## Demo zip

```bash
python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
# → sample_menu.zip (or config demo name)
```

Demo harness logs to `--log-dir`:

- `processing.log`
- `error.log` (if errors)
- `run_summary.json`

---

## Authoring checklist

1. Zip contains runnable `harness.py` (or set `main_script`).  
2. Harness accepts `--chunk` and `--log-dir`.  
3. Harness uses only exit `0` / `1` / `2` as above.  
4. Prefer writing progress to stdout; errors to stderr + log files.  
5. Drop zip on a configured search path (see `LAUNCHERCONFIG.JSON`).  
6. Verify with:

```bash
python scripts/run_harness.py
# includes contract test: extract + run demo harness
```

---

## Non-contract (out of scope)

- Arbitrary module `REGISTERED_MODULE` discovery (design-only).  
- Wrap-any path without a zip (**P-20 not approved**).  
