# Docs — TUI.inhouse

Human-facing documentation. **Start at [DOC-INDEX.md](./DOC-INDEX.md).**

| Quality / dist PRs | Plan |
|--------------------|------|
| **07** Strong documentation | [PR-07-strong-documentation.md](./PR-07-strong-documentation.md) |
| **08** Docstrings | [PR-08-docstrings.md](./PR-08-docstrings.md) |
| **09** Test harness | [PR-09-test-harness.md](./PR-09-test-harness.md) |
| **10** Distribution (wheel / wheelhouse) | [PR-10-distribution-wheel.md](./PR-10-distribution-wheel.md) · [DISTRIBUTION.md](./DISTRIBUTION.md) |
| **11…15** Menu platform | [menu-system/README.md](./menu-system/README.md) |

Standards: [DOCUMENTATION-STANDARDS.md](./DOCUMENTATION-STANDARDS.md) · [LINTING-STANDARDS.md](./LINTING-STANDARDS.md)

```bash
python3 scripts/run_harness.py   # from repo root
python3 scripts/build_dist.py    # wheel → dist/
python3 scripts/validate_menu.py docs/menu-system/examples/capability-demo
```
