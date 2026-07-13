# PR-03 — Launch harden + visible error logging

## Bug fixed

```text
NameError: name 'Screen' is not defined
```

Cause: `LauncherHome(Screen)` used `Screen` without `from textual.screen import Screen`.

## Scope

- Import `Screen` correctly; guard Textual ImportError → `logs/error.log`
- Wrap `app.run()` / `main` launch path with traceback → `logs/tui_crash.log` + `logs/error.log`
- Console always prints path to crash log
- `install.sh` documents where to look after failure

## Acceptance

- [x] `Screen` import fixed  
- [ ] Launch without NameError (when TTY available)  
- [ ] Forced exception writes traceback to `logs/tui_crash.log`  
