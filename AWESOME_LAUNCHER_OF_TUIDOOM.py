#!/usr/bin/env python3
"""
AWESOME_LAUNCHER_OF_TUIDOOM.py

Rock-solid, dead-stupid-simple Python TUI launcher for zip-packaged menus.

- python AWESOME_LAUNCHER_OF_TUIDOOM.py   (if Python in PATH)
- Default menu: "Go find a real menu"
- Zips: search, select, extract, run via harness
- Harnesses support chunked ops (e.g. one day of "memory files"), loops, exit levels (0=success,1=error,2=partial), logs
- Full TUI (Textual): header, footer, screens, prompts, live logs, file I/O
- Session recording + replay for automation on data/script/env changes
- BBS god-tier simple but powerful

Phase 1: minimal working bits. Bootstrap per design (stdlib first, venv, deps).

Usage examples:
  python AWESOME_LAUNCHER_OF_TUIDOOM.py
  python AWESOME_LAUNCHER_OF_TUIDOOM.py --create-demo
  python AWESOME_LAUNCHER_OF_TUIDOOM.py --replay sessions/xxx.json

Config: LAUNCHERCONFIG.JSON (same dir)
"""

from __future__ import annotations
import os
import sys
import subprocess
import platform
import json
import zipfile
import argparse
import datetime
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# -------------------------------
# BOOTSTRAP (stdlib only - design principle)
# -------------------------------

CORE_DEPS = ["textual", "rich"]

def detect_env() -> Dict[str, Any]:
    print("Detecting environment...")
    env_info = {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "is_wsl": "WSL_DISTRO_NAME" in os.environ or "microsoft" in platform.release().lower(),
        "is_windows": sys.platform.startswith("win"),
        "is_linux": sys.platform.startswith("linux"),
        "cwd": str(Path.cwd()),
    }
    for k, v in env_info.items():
        print(f"  {k}: {v}")
    return env_info

def find_or_create_venv() -> Path:
    venv_path = Path(__file__).parent / ".venv"
    if not venv_path.exists():
        print(f"Creating venv at {venv_path}...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
    return venv_path

def ensure_deps(venv_path: Path) -> Path:
    if sys.platform.startswith("win"):
        python_bin = venv_path / "Scripts" / "python.exe"
    else:
        python_bin = venv_path / "bin" / "python"
    pip = [str(python_bin), "-m", "pip"]
    print("Ensuring core deps (textual, rich) for TUI...")
    try:
        subprocess.check_call(pip + ["install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
        subprocess.check_call(pip + ["install"] + CORE_DEPS, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Dep install failed: {e}")
        sys.exit(1)
    return python_bin

def reexec_if_needed(venv_python: Path) -> None:
    if os.environ.get("AWESOME_LAUNCHER_VENV") != "1":
        print("Re-executing inside venv...")
        os.environ["AWESOME_LAUNCHER_VENV"] = "1"
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

# -------------------------------
# CONFIG + PATH HELPERS
# -------------------------------

DEFAULT_CONFIG = {
    "menu_search_paths": [".", "./menus", "./.launcher_menus", "~/.tui/menus"],
    "menus_dir": ".launcher_menus",
    "logs_dir": "logs",
    "sessions_dir": "sessions",
    "branding": {
        "header": "AWESOME LAUNCHER OF TUI DOOM",
        "footer": "BBS-Level | Zip Menus + Harnesses | Chunked Ops | Record/Replay | Phase 1"
    },
    "harness": {
        "default_chunk": "",
        "chunk_size": "1day",
        "log_files": ["processing.log", "error.log"]
    },
    "demo": {"sample_zip_name": "sample_menu.zip"}
}

def load_config() -> Dict[str, Any]:
    cfg_path = Path(__file__).parent / "LAUNCHERCONFIG.JSON"
    if cfg_path.exists():
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg = {**DEFAULT_CONFIG, **user_cfg}
            return cfg
        except Exception as e:
            print(f"Config load failed ({e}), using defaults.")
    return DEFAULT_CONFIG.copy()

def ensure_dirs(cfg: Dict[str, Any]) -> Dict[str, Path]:
    base = Path(__file__).parent
    dirs = {
        "menus": base / cfg["menus_dir"],
        "logs": base / cfg["logs_dir"],
        "sessions": base / cfg["sessions_dir"],
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs

def expand_search_paths(paths: List[str]) -> List[Path]:
    out = []
    for p in paths:
        pp = Path(p).expanduser()
        if pp.exists() or str(pp).startswith("."):
            out.append(pp)
    return out

# -------------------------------
# ZIP MENU + EXTRACT
# -------------------------------

def find_menu_zips(search_paths: List[str]) -> List[Path]:
    zips: List[Path] = []
    for base in expand_search_paths(search_paths):
        try:
            for z in base.glob("*.zip"):
                if z.is_file():
                    zips.append(z.resolve())
        except Exception:
            pass
    # dedupe + sort by name
    seen = set()
    unique = []
    for z in sorted(zips, key=lambda p: p.name.lower()):
        if z not in seen:
            seen.add(z)
            unique.append(z)
    return unique

def extract_menu_zip(zip_path: Path, menus_dir: Path) -> tuple[Path, str]:
    """Extract and return (extracted_dir, main_script_name)"""
    name = zip_path.stem
    target = menus_dir / name
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target)

    manifest = target / "menu.json"
    main_script = "harness.py"
    if manifest.exists():
        try:
            info = json.loads(manifest.read_text(encoding="utf-8"))
            main_script = info.get("main_script", "harness.py")
        except Exception:
            pass
    return target, main_script

# -------------------------------
# HARNESS RUNNER + CHUNKED LOGIC + EXIT LEVELS
# -------------------------------

def run_harness_once(
    extracted_dir: Path,
    main_script: str,
    chunk: Optional[str],
    log_dir: Path,
) -> Dict[str, Any]:
    harness = extracted_dir / main_script
    if not harness.exists():
        harness = extracted_dir / "harness.py"
    if not harness.exists():
        return {"returncode": 1, "stdout": "", "stderr": f"No harness found in {extracted_dir}", "exit_level": 1}

    log_dir.mkdir(parents=True, exist_ok=True)
    proc_log = log_dir / "processing.log"
    err_log = log_dir / "error.log"

    cmd = [sys.executable, str(harness)]
    if chunk:
        cmd += ["--chunk", chunk]
    cmd += ["--log-dir", str(log_dir)]

    start = datetime.datetime.now()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(extracted_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as te:
        return {"returncode": 1, "stdout": te.stdout or "", "stderr": "TIMEOUT", "exit_level": 1}

    # Append to logs
    ts = start.isoformat()
    with open(proc_log, "a", encoding="utf-8") as f:
        f.write(f"\n=== RUN {ts} chunk={chunk or 'full'} ===\n")
        f.write(result.stdout or "")
    if result.stderr:
        with open(err_log, "a", encoding="utf-8") as f:
            f.write(f"\n=== ERR {ts} ===\n{result.stderr}\n")

    rc = result.returncode
    # Map to exit levels: 0 success, 1 error, 2 partial (non-zero but partial work done)
    if rc == 0:
        level = 0
    elif rc == 2:
        level = 2
    else:
        level = 1

    return {
        "returncode": rc,
        "stdout": result.stdout or "",
        "stderr": result.stderr or "",
        "exit_level": level,
        "chunk": chunk,
        "started": ts,
    }

def run_chunked_harness(
    extracted_dir: Path,
    main_script: str,
    start_chunk: Optional[str],
    end_chunk: Optional[str],
    log_dir: Path,
) -> List[Dict[str, Any]]:
    results = []
    if start_chunk and end_chunk:
        try:
            d = datetime.date.fromisoformat(start_chunk)
            end_d = datetime.date.fromisoformat(end_chunk)
            current = d
            while current <= end_d:
                res = run_harness_once(extracted_dir, main_script, current.isoformat(), log_dir)
                results.append(res)
                if res["exit_level"] == 1 and res["returncode"] != 2:
                    # hard error - stop
                    break
                current += datetime.timedelta(days=1)
        except Exception as e:
            results.append({"returncode": 1, "stderr": f"Date range error: {e}", "exit_level": 1})
    else:
        chunk = start_chunk or end_chunk
        res = run_harness_once(extracted_dir, main_script, chunk, log_dir)
        results.append(res)
    return results

# -------------------------------
# DEMO ZIP GENERATOR (self-contained sample menu)
# -------------------------------

DEMO_HARNESS_CODE = r'''#!/usr/bin/env python3
"""
Demo harness (packaged inside sample_menu.zip)
Simulates chunked processing of daily "memory files".
Supports: --chunk YYYY-MM-DD , --log-dir DIR
Exit codes: 0=success, 1=error, 2=partial
"""
import argparse
import sys
import datetime
from pathlib import Path
import time
import json

def main():
    parser = argparse.ArgumentParser(description="Demo chunked memory processor")
    parser.add_argument("--chunk", default=None, help="Single day YYYY-MM-DD")
    parser.add_argument("--log-dir", default="logs")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    proc = log_dir / "processing.log"
    err = log_dir / "error.log"

    def log(msg: str, error: bool = False):
        fh = err if error else proc
        line = f"[{datetime.datetime.now().isoformat()}] {msg}\n"
        with open(fh, "a", encoding="utf-8") as f:
            f.write(line)
        print(msg, file=sys.stderr if error else sys.stdout)

    log(f"DEMO HARNESS start. chunk={args.chunk}")

    chunks = []
    if args.chunk:
        chunks = [args.chunk]
    else:
        today = datetime.date.today()
        chunks = [(today - datetime.timedelta(days=i)).isoformat() for i in range(0, 2)]

    processed = 0
    for ch in chunks:
        log(f"Processing memory files for {ch}...")
        for i in range(3):
            fname = f"mem-{ch}-{i:02d}.log"
            log(f"  + {fname}: read -> parse -> index (demo)")
            time.sleep(0.05)
        processed += 1
        log(f"Chunk {ch} done.")

    summary = {
        "harness": "demo",
        "chunks": len(chunks),
        "processed": processed,
        "exit_level": 0
    }
    (log_dir / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    log(f"DEMO complete. exit=0")
    sys.exit(0)

if __name__ == "__main__":
    main()
'''

DEMO_MENU_JSON = {
    "name": "demo-memory-processor",
    "description": "Phase 1 demo menu. Chunked daily memory file processing via harness.",
    "main_script": "harness.py",
    "version": "phase1-demo"
}

def create_demo_menu_zip(dest: Path) -> Path:
    dest = Path(dest).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("menu.json", json.dumps(DEMO_MENU_JSON, indent=2))
        z.writestr("harness.py", DEMO_HARNESS_CODE)
        z.writestr("README.txt",
            "Demo zip for AWESOME LAUNCHER OF TUI DOOM\n\n"
            "Select this menu, enter a chunk like 2026-06-20 or range, hit Run.\n"
            "Harness writes processing.log + error.log and run_summary.json.\n")
    return dest

# -------------------------------
# RECORDING + REPLAY
# -------------------------------

def save_recording(session_dir: Path, actions: List[Dict[str, Any]]) -> Path:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = session_dir / f"session_{ts}.json"
    data = {
        "recorded_at": datetime.datetime.now().isoformat(),
        "launcher": "AWESOME_LAUNCHER_OF_TUIDOOM",
        "phase": "1",
        "actions": actions,
    }
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out

def replay_session(session_path: Path) -> None:
    print(f"Replaying session: {session_path}")
    data = json.loads(session_path.read_text(encoding="utf-8"))
    actions = data.get("actions", [])
    print(f"  {len(actions)} recorded actions")
    for a in actions:
        print(f"  - {a.get('ts')} {a.get('action')}: {a.get('data')}")
        if a.get("action") == "run_harness":
            d = a.get("data", {})
            print(f"    -> would run zip={d.get('zip')} chunk={d.get('chunk')}")
            # For full replay you could resolve zip + call runner here
    print("Replay complete (non-interactive log of recorded steps).")

# -------------------------------
# TEXTUAL TUI (after bootstrap)
# -------------------------------

def launch_launcher_tui(cfg: Dict[str, Any]) -> None:
    # Heavy imports only after venv is ready
    from textual.app import App, ComposeResult
    from textual.containers import Grid, Horizontal, Vertical
    from textual.widgets import Button, Header, Footer, Label, Static, ListView, ListItem, Input, Log
    from textual.binding import Binding
    from textual.reactive import reactive
    from textual import work

    class LauncherHome(Screen):
        """Main menu + controls screen."""
        def compose(self) -> ComposeResult:
            yield Header()
            yield Label(cfg["branding"]["header"], id="brand")
            yield Static("Default: Go find a real menu  |  Zip menus + harnesses + chunked work + record/replay", id="subtitle")

            # Multi-pane inspired by Olivia guide starter template
            with Horizontal(id="main-area"):
                with Vertical(id="menu-pane", classes="pane"):
                    yield Static("MENUS", classes="pane-title")
                    yield ListView(id="menu-list")  # Per Olivia guide: ListView for menu

                with Vertical(id="controls-pane", classes="pane"):
                    with Grid(id="main-grid"):
                        yield Button("Scan / Find Menu", id="scan", variant="primary")
                        yield Button("Create Demo Zip", id="demo")
                        yield Button("Run Harness", id="run", variant="success")
                        yield Button("Library", id="library")
                        yield Button("Toggle Rec", id="rec")
                        yield Button("Save Rec", id="save_rec")
                        yield Button("Replay", id="replay")
                        yield Button("Toggle Gutter", id="gutter", variant="default")

                    with Horizontal():
                        yield Input(placeholder="Chunk (YYYY-MM-DD)", id="chunk")
                        yield Input(placeholder="End (optional)", id="end_chunk")

                    yield Static("Selected: (none)", id="selected")

            yield Log(id="runlog")  # Per Olivia guide: Log for streaming output
            yield Footer()

        def on_mount(self) -> None:
            self.app.query_one("#runlog", Log).write("[dim]Launcher ready. Scan for zips or create demo.[/dim]")

        def on_list_view_selected(self, event) -> None:
            """Handle selection from ListView (per Olivia guide recommendation for menu)."""
            if hasattr(self.app, "_zips") and event.item is not None:
                try:
                    idx = list(event.list_view.children).index(event.item)
                    if idx < len(self.app._zips):
                        self.app.current_zip = self.app._zips[idx]
                        sel = self.query_one("#selected", Static)
                        sel.update(f"Selected: {self.app.current_zip.name}")
                        self.app.log(f"[cyan]ListView selected: {self.app.current_zip.name}[/cyan]")
                except Exception:
                    pass

        def on_button_pressed(self, event: Button.Pressed) -> None:
            bid = event.button.id
            if bid == "scan":
                self.app.scan_for_zips()
            elif bid == "demo":
                dest = Path.cwd() / self.app.config["demo"]["sample_zip_name"]
                create_demo_menu_zip(dest)
                self.app.log(f"[green]Demo menu created: {dest.name}[/green]")
                self.app.log("Now press 'Go find a real menu (Scan)' or run directly.")
            elif bid == "run":
                chunk = self.query_one("#chunk", Input).value
                endc = self.query_one("#end_chunk", Input).value
                self.app.run_current_harness(chunk, endc)
            elif bid == "library":
                self.app.show_library()
            elif bid == "rec":
                self.app.is_recording = not self.app.is_recording
            elif bid == "save_rec":
                self.app.action_save_recording()
            elif bid == "replay":
                self.app.replay_last()
            elif bid == "gutter":
                self.app.action_toggle_gutter()

    class AwesomeLauncherApp(App):
        CSS_PATH = "grok_tui.tcss"  # From Olivia's canonical "Olivia says read this.md" (full guide, master a40a52d). Do not overwrite the source file. See that file for the complete TCSS layers, reactive Gutter, ListView+Log multi-pane starter template, and asyncio streaming example. This launcher is a slight extension/alignment.

        CSS = """
        Screen { align: center middle; }
        #brand { text-style: bold; color: #00ffaa; margin: 1; }
        #main-grid { grid-size: 3 2; grid-gutter: 1 2; padding: 1; }
        Button { width: 100%; height: 3; }
        #runlog { height: 18; border: solid #444; margin: 1; }
        #selected { color: #ffaa00; margin: 1 0; }
        """

        gutter_active: reactive[bool] = reactive(False)

        def watch_gutter_active(self, active: bool) -> None:
            """Automatically add/remove the class when the value changes (per Olivia guide)."""
            if active:
                self.add_class("gutter-active")
            else:
                self.remove_class("gutter-active")

        def action_toggle_gutter(self) -> None:
            """Bind this to a key (e.g. 'g'). Per the canonical guide."""
            self.gutter_active = not self.gutter_active

        BINDINGS = [
            Binding("ctrl+q", "quit", "Quit"),
            Binding("s", "scan_menus", "Scan"),
            Binding("r", "toggle_record", "Record"),
            Binding("ctrl+s", "save_recording", "Save Rec"),
            Binding("g", "toggle_gutter", "Toggle Gutter"),  # From Olivia guide
        ]

        current_zip: reactive[Optional[Path]] = reactive(None)
        is_recording: reactive[bool] = reactive(False)
        recording: List[Dict[str, Any]] = []

        def __init__(self, config: Dict[str, Any], dirs: Dict[str, Path], **kwargs):
            super().__init__(**kwargs)
            self.config = config
            self.dirs = dirs
            self.current_zip = None
            self.is_recording = False
            self.recording = []

        def compose(self) -> ComposeResult:
            yield LauncherHome()

        def on_mount(self) -> None:
            self.title = self.config["branding"]["header"]
            self.sub_title = "Phase 1 - BBS Simple + Harnesses"

        def watch_current_zip(self, zip_path: Optional[Path]) -> None:
            sel = self.query_one("#selected", Static)
            if zip_path:
                sel.update(f"Selected: {zip_path.name} (extracted on run)")
            else:
                sel.update("Selected: (none)")

        def watch_is_recording(self, recording: bool) -> None:
            try:
                btn = self.query_one("#rec", Button)
                btn.label = "Recording: ON" if recording else "Toggle Recording"
            except Exception:
                pass

        def log(self, msg: str) -> None:
            try:
                lw = self.query_one("#runlog", Log)
                if hasattr(lw, "write_line"):
                    lw.write_line(msg)
                else:
                    lw.write(msg)
            except Exception:
                print(msg)

        def record_action(self, action: str, data: Dict[str, Any]) -> None:
            if self.is_recording:
                self.recording.append({
                    "ts": datetime.datetime.now().isoformat(),
                    "action": action,
                    "data": data
                })

        # --- Actions ---
        def action_scan_menus(self) -> None:
            self.scan_for_zips()

        def action_toggle_record(self) -> None:
            self.is_recording = not self.is_recording
            self.log(f"[bold]{'RECORDING ON' if self.is_recording else 'RECORDING OFF'}[/bold]")

        def action_save_recording(self) -> None:
            if not self.recording:
                self.log("[yellow]No actions recorded yet.[/yellow]")
                return
            out = save_recording(self.dirs["sessions"], self.recording)
            self.log(f"[green]Saved recording: {out.name}[/green]")
            self.recording.clear()

        def scan_for_zips(self) -> None:
            zips = find_menu_zips(self.config.get("menu_search_paths", []))
            self.log(f"Scanned. Found {len(zips)} menu zip(s).")
            if not zips:
                self.log("[yellow]No zips found. Use 'Create Demo Menu Zip' first.[/yellow]")
                return

            try:
                lv = self.query_one("#menu-list", ListView)
                lv.clear()
                for z in zips:
                    lv.append(ListItem(Static(z.name, classes="menu-item")))
                self._zips = zips
                if lv.children:
                    lv.index = 0  # select first per guide-friendly list behavior
            except Exception:
                for i, z in enumerate(zips[:5]):
                    self.log(f"  [{i+1}] {z.name}")

            self.current_zip = zips[0]
            self.log(f"[cyan]Selected: {self.current_zip.name}[/cyan]")

        # Button handling lives in LauncherHome screen (forwards to app)

        def show_library(self) -> None:
            menus_dir = self.dirs["menus"]
            if not menus_dir.exists():
                self.log("No extracted menus yet.")
                return
            entries = list(menus_dir.glob("*"))
            self.log("Extracted menus / library:")
            for e in entries:
                self.log(f"  - {e.name}")
            if not entries:
                self.log("(empty - extract a zip first)")

        def replay_last(self) -> None:
            sessions = sorted(self.dirs["sessions"].glob("session_*.json"), reverse=True)
            if not sessions:
                self.log("[yellow]No session files found.[/yellow]")
                return
            latest = sessions[0]
            self.log(f"Replaying {latest.name} (non-interactive)...")
            try:
                replay_session(latest)
                self.log("[green]Replay done.[/green]")
            except Exception as e:
                self.log(f"[red]Replay error: {e}[/red]")

        # Live harness runner (Phase 2 streaming per Olivia guide - line by line to Log)
        def _run_harness_live(self, extracted_dir: Path, main_script: str, chunk: Optional[str], log_dir: Path) -> Dict[str, Any]:
            harness = extracted_dir / main_script
            if not harness.exists():
                harness = extracted_dir / "harness.py"
            if not harness.exists():
                self.call_from_thread(self.log, "[red]No harness found[/red]")
                return {"returncode": 1, "exit_level": 1, "chunk": chunk}

            log_dir.mkdir(parents=True, exist_ok=True)
            cmd = [sys.executable, str(harness)]
            if chunk:
                cmd += ["--chunk", chunk]
            cmd += ["--log-dir", str(log_dir)]

            self.call_from_thread(self.log, f"$ {' '.join(cmd)}")

            try:
                import subprocess
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(extracted_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                for line in proc.stdout:
                    line = line.rstrip("\n")
                    if line:
                        self.call_from_thread(self.log, line)
                proc.wait()
                rc = proc.returncode
                level = 0 if rc == 0 else (2 if rc == 2 else 1)
                self.call_from_thread(self.log, f"[Process exited with code {rc}]")
                return {
                    "returncode": rc,
                    "exit_level": level,
                    "chunk": chunk,
                }
            except Exception as e:
                self.call_from_thread(self.log, f"[red]Stream error: {e}[/red]")
                return {"returncode": 1, "exit_level": 1, "chunk": chunk}

        # Main run action - attached to a dynamic button or we trigger via code
        def run_current_harness(self, chunk: str = "", end_chunk: str = "") -> None:
            if not self.current_zip:
                self.scan_for_zips()
                if not self.current_zip:
                    self.log("[red]No menu selected. Create demo or scan first.[/red]")
                    return

            extracted, main_script = extract_menu_zip(self.current_zip, self.dirs["menus"])
            self.log(f"[cyan]Extracted {self.current_zip.name} -> {extracted.name}[/cyan]")

            start_c = chunk.strip() or None
            end_c = end_chunk.strip() or None

            self.record_action("run_harness", {
                "zip": str(self.current_zip.name),
                "chunk": start_c,
                "end_chunk": end_c
            })

            self.log(f"[bold]Running harness[/bold] chunk={start_c or 'default'} range_end={end_c or '-'} ...")

            @work(exclusive=True, thread=True)
            def _do_run() -> None:
                try:
                    # Live streaming version inspired by the Olivia guide's asyncio/subprocess to Log pattern
                    # (adapted to thread worker for compatibility with existing harness)
                    results = []
                    if start_c and end_c:
                        try:
                            d = datetime.date.fromisoformat(start_c)
                            end_d = datetime.date.fromisoformat(end_c)
                            current = d
                            while current <= end_d:
                                res = self._run_harness_live(extracted, main_script, current.isoformat(), self.dirs["logs"])
                                results.append(res)
                                if res.get("exit_level") == 1 and res.get("returncode") != 2:
                                    break
                                current += datetime.timedelta(days=1)
                        except Exception as e:
                            self.call_from_thread(self.log, f"[red]Date range error: {e}[/red]")
                    else:
                        chunk = start_c or end_c
                        res = self._run_harness_live(extracted, main_script, chunk, self.dirs["logs"])
                        results.append(res)

                    for r in results:
                        level = r.get("exit_level", 1)
                        color = "green" if level == 0 else ("yellow" if level == 2 else "red")
                        self.call_from_thread(
                            self.log,
                            f"[{color}]Chunk {r.get('chunk') or 'full'}: exit_level={level} rc={r.get('returncode')}[/{color}]"
                        )
                    overall = max((r.get("exit_level", 0) for r in results), default=0)
                    self.call_from_thread(self.log, f"[bold]Overall exit level: {overall}[/bold]  (0=done,1=error,2=partial)")
                    self.call_from_thread(self.log, "See logs/ for processing.log + error.log + run_summary.json")
                except Exception as ex:
                    self.call_from_thread(self.log, f"[red]Run error: {ex}[/red]")

            _do_run()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            # If user hits enter in chunk fields, offer to run
            if event.input.id in ("chunk", "end_chunk"):
                chunk = self.query_one("#chunk", Input).value
                endc = self.query_one("#end_chunk", Input).value
                self.run_current_harness(chunk, endc)

    # Boot the app
    dirs = ensure_dirs(cfg)
    app = AwesomeLauncherApp(cfg, dirs)
    # Add a run button on the home by monkey a bit or just tell user
    # For clean: we can add the run button in compose, but for simplicity we document in log
    # Users can use the chunk inputs + submit to run, or we expose via key.
    # Add a global run action
    app.run()

# -------------------------------
# MAIN
# -------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AWESOME LAUNCHER OF TUI DOOM - Phase 1"
    )
    parser.add_argument("--replay", metavar="SESSION.json", help="Replay a recorded session (non-interactive)")
    parser.add_argument("--create-demo", action="store_true", help="Create sample_menu.zip and exit")
    args = parser.parse_args()

    if args.create_demo:
        dest = Path.cwd() / "sample_menu.zip"
        p = create_demo_menu_zip(dest)
        print(f"Demo menu zip created: {p}")
        print("Run the launcher and scan or select it.")
        return

    if args.replay:
        sp = Path(args.replay)
        if not sp.exists():
            print(f"Session not found: {sp}")
            sys.exit(1)
        replay_session(sp)
        return

    # Full path (TUI or bootstrap)
    detect_env()
    venv_path = find_or_create_venv()
    venv_python = ensure_deps(venv_path)
    reexec_if_needed(venv_python)

    # Inside venv (or already good)
    cfg = load_config()
    ensure_dirs(cfg)
    launch_launcher_tui(cfg)

if __name__ == "__main__":
    main()
