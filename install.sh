#!/usr/bin/env bash
# AWESOME LAUNCHER OF TUI DOOM — one-line bootstrap (PR-01 scaffold)
# Usage:
#   ./install.sh
#   ./install.sh --no-launch --quiet
#   ./install.sh --recon-only
#   ./install.sh --install-python   # optional; may need sudo (opt-in)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

NO_LAUNCH=0
QUIET=0
RECON_ONLY=0
INSTALL_PYTHON=0
PARTY=0

for arg in "$@"; do
  case "$arg" in
    --no-launch) NO_LAUNCH=1 ;;
    --quiet|--boring) QUIET=1 ;;
    --recon-only) RECON_ONLY=1 ;;
    --install-python) INSTALL_PYTHON=1 ;;
    --party) PARTY=1 ;;
    -h|--help)
      sed -n '1,20p' "$0"
      exit 0
      ;;
  esac
done

mkdir -p logs sessions .launcher_menus

# Per-run stamp for logs/ (errors + success + ops)
STAMP="$(date +%Y%m%d_%H%M%S 2>/dev/null || date +%Y%m%d%H%M%S)"
export AWESOME_LAUNCHER_STAMP="$STAMP"
BOOT_LOG="$ROOT/logs/bootstrap_${STAMP}.log"
BOOT_LATEST="$ROOT/logs/bootstrap.log"
ERR_LOG="$ROOT/logs/error_${STAMP}.log"
ERR_LATEST="$ROOT/logs/error.log"
SUCCESS_LOG="$ROOT/logs/success_${STAMP}.log"
SUCCESS_LATEST="$ROOT/logs/success.log"
OPS_LOG="$ROOT/logs/ops_${STAMP}.log"
OPS_LATEST="$ROOT/logs/ops.log"
DEPS_LOG="$ROOT/logs/bootstrap_deps_${STAMP}.log"
DEPS_LATEST="$ROOT/logs/bootstrap_deps.log"
STEP=0
STEPS=10
SAVED_COLS=""
INSTALL_MODE=0

ts() { date -Iseconds 2>/dev/null || date; }

_tee_all() {
  # stdin → bootstrap stamped + latest
  tee -a "$BOOT_LOG" | tee -a "$BOOT_LATEST"
}

log() {
  local msg="$*"
  echo "[$(ts)] $msg" | tee -a "$BOOT_LOG" | tee -a "$BOOT_LATEST" | tee -a "$OPS_LOG" | tee -a "$OPS_LATEST" >/dev/null
  # also print (install mode wraps)
  if [[ "$INSTALL_MODE" -eq 1 && "$QUIET" -eq 0 ]]; then
    install_say "$msg"
  else
    echo "[$(ts)] $msg"
  fi
}

log_success() {
  local msg="$*"
  echo "[$(ts)] SUCCESS: $msg" | tee -a "$SUCCESS_LOG" | tee -a "$SUCCESS_LATEST" | tee -a "$OPS_LOG" | tee -a "$OPS_LATEST" | tee -a "$BOOT_LOG" | tee -a "$BOOT_LATEST" >/dev/null
  if [[ "$INSTALL_MODE" -eq 1 && "$QUIET" -eq 0 ]]; then
    install_say "SUCCESS: $msg"
  else
    echo "[$(ts)] SUCCESS: $msg"
  fi
}

fail() {
  local msg="$*"
  echo "[$(ts)] FAIL: $msg" | tee -a "$BOOT_LOG" | tee -a "$BOOT_LATEST" | tee -a "$ERR_LOG" | tee -a "$ERR_LATEST" | tee -a "$OPS_LOG" | tee -a "$OPS_LATEST" >&2
  echo "  → full narrative: $BOOT_LOG" >&2
  echo "  → error log:      $ERR_LOG" >&2
  echo "  → error latest:   $ERR_LATEST" >&2
  install_mode_exit
  exit 1
}

step_begin() {
  STEP=$((STEP + 1))
  local name="$1"
  log "[STEP $(printf '%02d' "$STEP")/$(printf '%02d' "$STEPS")] $name ... RUNNING"
}

step_pass() {
  local name="$1"
  log "[STEP $(printf '%02d' "$STEP")/$(printf '%02d' "$STEPS")] $name ... PASS"
  log_success "step $name PASS"
}

# --- Install mode: 40 cols, black screen, white fonts, flashes; key text colored ---
install_mode_enter() {
  [[ "$QUIET" -eq 1 ]] && return 0
  [[ "$INSTALL_MODE" -eq 1 ]] && return 0
  INSTALL_MODE=1
  if [[ -t 1 ]] && command -v stty >/dev/null 2>&1; then
    SAVED_COLS="$(stty size 2>/dev/null | awk '{print $2}')" || SAVED_COLS=""
    stty cols 40 2>/dev/null || true
  fi
  # black bg, white fg, clear
  printf '\033[40m\033[37m\033[2J\033[H'
  install_flash 3
  install_say "INSTALL MODE · 40 COL · BLACK/WHITE"
  install_say "Key words stay colored. stamp=$STAMP"
}

install_mode_exit() {
  [[ "$INSTALL_MODE" -eq 0 ]] && return 0
  if [[ -n "${SAVED_COLS:-}" ]] && command -v stty >/dev/null 2>&1; then
    stty cols "$SAVED_COLS" 2>/dev/null || true
  fi
  printf '\033[0m\n'
  INSTALL_MODE=0
}

install_flash() {
  local n="${1:-2}" i
  [[ "$QUIET" -eq 1 ]] && return 0
  for ((i=0; i<n; i++)); do
    printf '\033[7m'
    sleep 0.06
    printf '\033[27m\033[40m\033[37m'
    sleep 0.05
  done
}

# Color key tokens; body stays white. Wrap ~40 cols for display.
install_say() {
  local msg="$*"
  [[ "$QUIET" -eq 1 ]] && { echo "$msg"; return 0; }
  # crude wrap to 40
  local line="" w
  for w in $msg; do
    if [[ -z "$line" ]]; then
      line="$w"
    elif (( ${#line} + 1 + ${#w} > 40 )); then
      _install_print_line "$line"
      line="$w"
    else
      line="$line $w"
    fi
  done
  [[ -n "$line" ]] && _install_print_line "$line"
}

_install_print_line() {
  local s="$1"
  # key words → color, rest white on black
  s="$(printf '%s' "$s" | sed -E \
    -e 's/\b(FAIL(ED|URE)?|ERROR)\b/\x1b[91m\1\x1b[37m/gi' \
    -e 's/\b(PASS(ED)?|OK|SUCCESS)\b/\x1b[92m\1\x1b[37m/gi' \
    -e 's/\b(SKIP(PED)?)\b/\x1b[93m\1\x1b[37m/gi' \
    -e 's/\b(TEST|DEPS?)\b/\x1b[96m\1\x1b[37m/gi' \
    -e 's/\b(textual|rich)\b/\x1b[95m\1\x1b[37m/gi' \
    -e 's/\b(pip)\b/\x1b[94m\1\x1b[37m/gi')"
  printf '\033[40m\033[37m%s\033[0m\n' "$s"
}

strobe() {
  [[ "$QUIET" -eq 1 ]] && return 0
  local frames=(
    $'\e[35;1m▓░▓░  GUTTER MODE WARMING UP  ░▓░▓\e[0m'
    $'\e[31;1m░▓░▓  PINK/BLACK STROBE      ▓░▓░\e[0m'
    $'\e[35;1m▓░▓░  OLIVIA DEV ALPHA       ░▓░▓\e[0m'
    $'\e[91;1m★★★  AWESOME LAUNCHER OF TUI DOOM  ★★★\e[0m'
  )
  local n=2
  [[ "$PARTY" -eq 1 ]] && n=6
  local i
  for ((i=0; i<n; i++)); do
    printf '\r%s' "${frames[i % ${#frames[@]}]}"
    sleep 0.12
  done
  printf '\n'
  log "GUTTER MODE ENGAGED — bootstrap silliness online"
}

banner() {
  [[ "$QUIET" -eq 1 ]] && return 0
  cat <<'EOF'
╔══════════════════════════════════════════════════════════╗
║  AWESOME LAUNCHER OF TUI DOOM — dirty simple install     ║
║  download → sprawl → venv → pip → strobe → run           ║
╚══════════════════════════════════════════════════════════╝
EOF
}

# --- steps ---

banner
strobe
log "session stamp=$STAMP logs under $ROOT/logs/"

step_begin "detect-os"
OS="$(uname -s 2>/dev/null || echo unknown)"
IS_WSL=0
if grep -qi microsoft /proc/version 2>/dev/null || [[ -n "${WSL_DISTRO_NAME:-}" ]]; then
  IS_WSL=1
fi
log "  os=$OS wsl=$IS_WSL cwd=$ROOT"
step_pass "detect-os"

step_begin "find-python"
PY=""
for c in python3.12 python3.11 python3.13 python3.10 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then
    if "$c" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      PY="$(command -v "$c")"
      break
    fi
  fi
done

if [[ -z "$PY" ]]; then
  log "  no suitable Python ≥3.10 on PATH"
  if [[ "$INSTALL_PYTHON" -eq 1 ]]; then
    step_begin "install-python-opt-in"
    if command -v apt-get >/dev/null 2>&1; then
      log "  attempting: sudo apt-get install -y python3 python3-venv python3-pip"
      sudo apt-get update -y >>"$BOOT_LOG" 2>>"$ERR_LOG" || fail "apt-get update failed"
      sudo apt-get install -y python3 python3-venv python3-pip >>"$BOOT_LOG" 2>>"$ERR_LOG" || fail "apt-get install python3 failed"
      PY="$(command -v python3 || true)"
    elif command -v brew >/dev/null 2>&1; then
      brew install python >>"$BOOT_LOG" 2>>"$ERR_LOG" || fail "brew install python failed"
      PY="$(command -v python3 || true)"
    else
      fail "no package manager for auto Python install — install Python 3.10+ manually, re-run"
    fi
    [[ -n "$PY" ]] || fail "python still missing after install attempt"
    step_pass "install-python-opt-in"
  else
    {
      echo "No Python ≥3.10 found."
      echo "  Install Python, then re-run: ./install.sh"
      echo "  Or opt-in auto-install:     ./install.sh --install-python"
      echo "  Docs: https://www.python.org/downloads/"
    } | tee -a "$ERR_LOG" | tee -a "$ERR_LATEST" >&2
    exit 2
  fi
fi
log "  python=$PY ($($PY -c 'import sys; print(sys.version.split()[0])'))"
step_pass "find-python"

if [[ "$RECON_ONLY" -eq 1 ]]; then
  step_begin "recon-only"
  if [[ -f "$ROOT/scripts/recon.py" ]]; then
    "$PY" "$ROOT/scripts/recon.py" --out "$ROOT/logs" || fail "recon.py failed"
  else
    log "  scripts/recon.py not present yet (PR-02) — writing mini recon"
    {
      echo "# mini recon $(ts)"
      echo "python=$PY"
      echo "os=$OS wsl=$IS_WSL"
      command -v pip3 || true
      ls -la "$ROOT" | head -30
    } | tee "$ROOT/logs/recon-report.md"
  fi
  step_pass "recon-only"
  log "recon-only complete — not launching"
  exit 0
fi

step_begin "create-venv"
if [[ ! -x "$ROOT/.venv/bin/python" && ! -x "$ROOT/.venv/Scripts/python.exe" ]]; then
  # enter install mode for any real install work
  install_mode_enter
  "$PY" -m venv "$ROOT/.venv" >>"$BOOT_LOG" 2>>"$ERR_LOG" || fail "venv create failed"
  log_success "venv created"
fi
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  VPY="$ROOT/.venv/bin/python"
elif [[ -x "$ROOT/.venv/Scripts/python.exe" ]]; then
  VPY="$ROOT/.venv/Scripts/python.exe"
else
  fail "venv python missing after create"
fi
log "  venv_python=$VPY"
step_pass "create-venv"

step_begin "ensure-pip"
"$VPY" -m pip --version >>"$BOOT_LOG" 2>>"$ERR_LOG" || {
  install_mode_enter
  log "  pip broken or missing — ensurepip"
  "$VPY" -m ensurepip --upgrade >>"$BOOT_LOG" 2>>"$ERR_LOG" || fail "ensurepip failed"
}
step_pass "ensure-pip"

# Install-mode as soon as we touch deps: 40-col black/white + flashes
install_mode_enter

step_begin "install-deps"
# Skip reinstall if already importable — never reinstall python/deps needlessly
if "$VPY" -c "import textual, rich" >/dev/null 2>&1; then
  install_flash 1
  log "DEPS already importable — SKIP pip reinstall"
  log_success "deps present — no reinstall"
else
  install_flash 2
  log "DEPS missing — pip install (no python reinstall)"
  # only upgrade pip when we actually need to install packages
  "$VPY" -m pip install --upgrade pip >>"$DEPS_LOG" 2>&1 \
    || { cat "$DEPS_LOG" >>"$ERR_LOG"; fail "pip upgrade failed (see $DEPS_LOG)"; }
  cp -f "$DEPS_LOG" "$DEPS_LATEST" 2>/dev/null || cat "$DEPS_LOG" >>"$DEPS_LATEST"
  if [[ -f "$ROOT/requirements.txt" ]]; then
    "$VPY" -m pip install -r "$ROOT/requirements.txt" >>"$DEPS_LOG" 2>&1 \
      || { cat "$DEPS_LOG" >>"$ERR_LOG"; cat "$DEPS_LOG" >>"$ERR_LATEST"; fail "pip install -r requirements.txt failed"; }
  else
    "$VPY" -m pip install textual rich >>"$DEPS_LOG" 2>&1 \
      || { cat "$DEPS_LOG" >>"$ERR_LOG"; fail "pip install textual rich failed"; }
  fi
  cp -f "$DEPS_LOG" "$DEPS_LATEST" 2>/dev/null || true
  "$VPY" -c "import textual, rich" >>"$BOOT_LOG" 2>>"$ERR_LOG" \
    || fail "import textual/rich failed after install"
  log_success "pip install DEPS PASS"
fi
step_pass "install-deps"

step_begin "library-test-demos"
# On-screen test calls for each library (no reinstall)
install_flash 2
log "=== LIBRARY TEST DEMOS ==="
DEMO_OUT="$("$VPY" - <<'PY'
import json, sys
results = []
try:
    import textual
    from textual.app import App
    ver = getattr(textual, "__version__", "?")
    results.append(("textual", True, f"version={ver} App={callable(App)}"))
except Exception as e:
    results.append(("textual", False, repr(e)))
try:
    import rich
    from rich.console import Console
    from rich.text import Text
    t = Text("rich OK", style="bold white on black")
    _ = t.plain
    ver = getattr(rich, "__version__", "?")
    results.append(("rich", True, f"version={ver} Console+Text ok"))
except Exception as e:
    results.append(("rich", False, repr(e)))
try:
    import zipfile, pathlib
    results.append(("zipfile", True, f"ZipFile={callable(zipfile.ZipFile)}"))
    results.append(("pathlib", True, f"Path={callable(pathlib.Path)}"))
except Exception as e:
    results.append(("stdlib", False, repr(e)))
print(json.dumps(results))
PY
)" || fail "library demos failed to run"

DEMO_OK=1
while IFS= read -r row; do
  [[ -z "$row" ]] && continue
  # parse via python for safety
  :
done <<<"$DEMO_OUT"

"$VPY" -c "
import json, sys
results = json.loads(sys.argv[1])
ok = True
for name, good, detail in results:
    status = 'PASS' if good else 'FAIL'
    if not good:
        ok = False
    print(f'TEST {name}: {status} — {detail}')
sys.exit(0 if ok else 1)
" "$DEMO_OUT" | while IFS= read -r line; do
  log "$line"
done
# re-check exit: pipe masks status — re-run check
if ! "$VPY" -c "
import json, sys
results = json.loads(sys.argv[1])
sys.exit(0 if all(r[1] for r in results) else 1)
" "$DEMO_OUT"; then
  fail "library test demos FAIL"
fi
log_success "library demos PASS (textual, rich, zipfile, pathlib)"
step_pass "library-test-demos"

install_mode_exit

step_begin "sprawl-dirs"
mkdir -p "$ROOT/logs" "$ROOT/sessions" "$ROOT/.launcher_menus"
step_pass "sprawl-dirs"

step_begin "create-demo-zip"
if [[ ! -f "$ROOT/sample_menu.zip" ]]; then
  "$VPY" "$ROOT/AWESOME_LAUNCHER_OF_TUIDOOM.py" --create-demo >>"$BOOT_LOG" 2>>"$ERR_LOG" \
    || fail "--create-demo failed"
fi
[[ -f "$ROOT/sample_menu.zip" ]] || fail "sample_menu.zip still missing"
step_pass "create-demo-zip"

step_begin "stamp-ok"
echo "ok $(ts) stamp=$STAMP" > "$ROOT/.awesome_bootstrap_ok"
log_success "bootstrap complete stamp=$STAMP"
step_pass "stamp-ok"

if [[ "$QUIET" -eq 0 ]]; then
  cat <<EOF
╔══════════════════════════════════════════════════════════╗
║  SPRAWL COMPLETE · DEPS OK · GUTTER READY                ║
║  logs stamp=$STAMP                                       ║
║  success → logs/success_${STAMP}.log                     ║
║  error   → logs/error_${STAMP}.log                       ║
║  ops     → logs/ops_${STAMP}.log                         ║
╚══════════════════════════════════════════════════════════╝
EOF
fi

if [[ "$NO_LAUNCH" -eq 1 ]]; then
  log "done (--no-launch). Run: $VPY AWESOME_LAUNCHER_OF_TUIDOOM.py"
  exit 0
fi

step_begin "launch-tui"
log "launching TUI (ctrl+q to quit)..."
log "  crashes → logs/tui_crash_${STAMP}.log + logs/error_${STAMP}.log"
log "  success → logs/success_${STAMP}.log + logs/ops_${STAMP}.log"
# re-exec inside venv; launcher will also bootstrap if needed
export AWESOME_LAUNCHER_VENV=1
export AWESOME_LAUNCHER_STAMP="$STAMP"
set +e
"$VPY" "$ROOT/AWESOME_LAUNCHER_OF_TUIDOOM.py"
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  log "TUI exited rc=$rc"
  echo "--- tail $ERR_LATEST ---" | tee -a "$BOOT_LOG"
  tail -40 "$ERR_LATEST" 2>/dev/null | tee -a "$BOOT_LOG" || true
  echo "--- tail logs/tui_crash.log ---" | tee -a "$BOOT_LOG"
  tail -40 "$ROOT/logs/tui_crash.log" 2>/dev/null | tee -a "$BOOT_LOG" || true
  # also any stamped crash for this session
  if [[ -f "$ROOT/logs/tui_crash_${STAMP}.log" ]]; then
    echo "--- tail logs/tui_crash_${STAMP}.log ---" | tee -a "$BOOT_LOG"
    tail -40 "$ROOT/logs/tui_crash_${STAMP}.log" 2>/dev/null | tee -a "$BOOT_LOG" || true
  fi
  exit "$rc"
fi
log_success "TUI exited cleanly rc=0"
exit 0
