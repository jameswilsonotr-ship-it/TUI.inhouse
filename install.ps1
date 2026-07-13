# AWESOME LAUNCHER OF TUI DOOM — Windows one-line bootstrap (PR-01 scaffold)
# Usage:
#   .\install.ps1
#   .\install.ps1 -NoLaunch -Quiet
#   irm https://raw.githubusercontent.com/<org>/TUI.inhouse/main/install.ps1 | iex
param(
  [switch]$NoLaunch,
  [switch]$Quiet,
  [switch]$ReconOnly,
  [switch]$InstallPython
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Root) { $Root = Get-Location }
Set-Location $Root

New-Item -ItemType Directory -Force -Path logs, sessions, .launcher_menus | Out-Null
$BootLog = Join-Path $Root "logs\bootstrap.log"
$ErrLog = Join-Path $Root "logs\error.log"
$script:Step = 0
$script:Steps = 10

function Log([string]$Msg) {
  $line = "[{0}] {1}" -f (Get-Date -Format o), $Msg
  Add-Content -Path $BootLog -Value $line
  Write-Host $line
}

function Fail([string]$Msg) {
  $line = "[{0}] FAIL: {1}" -f (Get-Date -Format o), $Msg
  Add-Content -Path $BootLog -Value $line
  Add-Content -Path $ErrLog -Value $line
  Write-Host $line -ForegroundColor Red
  Write-Host "  → $BootLog"
  Write-Host "  → $ErrLog"
  exit 1
}

function Step-Begin([string]$Name) {
  $script:Step++
  Log ("[STEP {0:D2}/{1:D2}] {2} ... RUNNING" -f $script:Step, $script:Steps, $Name)
}

function Step-Pass([string]$Name) {
  Log ("[STEP {0:D2}/{1:D2}] {2} ... PASS" -f $script:Step, $script:Steps, $Name)
}

if (-not $Quiet) {
  Write-Host "AWESOME LAUNCHER OF TUI DOOM — Windows bootstrap" -ForegroundColor Magenta
  Write-Host "GUTTER MODE ENGAGED (strobe lite)" -ForegroundColor DarkRed
}

Step-Begin "find-python"
$Py = $null
foreach ($c in @("py", "python", "python3")) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd) {
    try {
      & $cmd.Source -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" 2>$null
      if ($LASTEXITCODE -eq 0) { $Py = $cmd.Source; break }
    } catch {}
  }
}
if (-not $Py) {
  if ($InstallPython) {
    Log "  winget install Python.Python.3.12 (opt-in)"
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $Py = (Get-Command py -ErrorAction SilentlyContinue).Source
  }
  if (-not $Py) {
    Fail "No Python >=3.10. Install from python.org or re-run with -InstallPython"
  }
}
Log "  python=$Py"
Step-Pass "find-python"

if ($ReconOnly) {
  Step-Begin "recon-only"
  @"
# mini recon $(Get-Date -Format o)
python=$Py
root=$Root
"@ | Set-Content (Join-Path $Root "logs\recon-report.md")
  Step-Pass "recon-only"
  exit 0
}

Step-Begin "create-venv"
$Vpy = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Vpy)) {
  & $Py -m venv (Join-Path $Root ".venv")
  if ($LASTEXITCODE -ne 0) { Fail "venv create failed" }
}
Step-Pass "create-venv"

Step-Begin "install-deps"
& $Vpy -m pip install --upgrade pip *>> (Join-Path $Root "logs\bootstrap_deps.log")
if (Test-Path (Join-Path $Root "requirements.txt")) {
  & $Vpy -m pip install -r requirements.txt *>> (Join-Path $Root "logs\bootstrap_deps.log")
} else {
  & $Vpy -m pip install textual rich *>> (Join-Path $Root "logs\bootstrap_deps.log")
}
& $Vpy -c "import textual, rich"
if ($LASTEXITCODE -ne 0) { Fail "import textual/rich failed" }
Step-Pass "install-deps"

Step-Begin "create-demo-zip"
if (-not (Test-Path (Join-Path $Root "sample_menu.zip"))) {
  & $Vpy (Join-Path $Root "AWESOME_LAUNCHER_OF_TUIDOOM.py") --create-demo
}
Step-Pass "create-demo-zip"

"ok $(Get-Date -Format o)" | Set-Content (Join-Path $Root ".awesome_bootstrap_ok")

if ($NoLaunch) {
  Log "done (-NoLaunch). Run: $Vpy AWESOME_LAUNCHER_OF_TUIDOOM.py"
  exit 0
}

$env:AWESOME_LAUNCHER_VENV = "1"
& $Vpy (Join-Path $Root "AWESOME_LAUNCHER_OF_TUIDOOM.py")
