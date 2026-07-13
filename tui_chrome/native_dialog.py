"""Native OS file dialogs with Textual DirectoryTree fallback.

Order of attempts:
  1. tkinter.filedialog (works on many desktops if Tcl/Tk present)
  2. Windows PowerShell OpenFileDialog (native Win32 / also WSL→powershell.exe)
  3. zenity / kdialog on Linux (optional)
  4. None → caller should open Textual MenuFilePicker

Never raises to the UI thread for "not available" — returns None so Olivia
can fall through to the in-TUI picker or demo.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence


def _is_wsl() -> bool:
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        return "microsoft" in platform.release().lower()
    except Exception:
        return False


def try_tkinter_open(
    *,
    title: str = "Pick a menu zip",
    start: Optional[Path] = None,
    filetypes: Optional[Sequence[tuple]] = None,
) -> Optional[Path]:
    """Block with a native tk file dialog if DISPLAY/Tk available."""
    filetypes = filetypes or (("Zip menus", "*.zip"), ("All files", "*.*"))
    start_dir = str((start or Path.cwd()).resolve())
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None
    try:
        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        path = filedialog.askopenfilename(
            parent=root,
            title=title,
            initialdir=start_dir,
            filetypes=list(filetypes),
        )
        root.destroy()
        if path:
            p = Path(path)
            return p if p.exists() else None
    except Exception:
        return None
    return None


def try_windows_openfiledialog(
    *,
    title: str = "Pick a menu zip",
    start: Optional[Path] = None,
) -> Optional[Path]:
    """Win32 OpenFileDialog via PowerShell (Windows host or WSL)."""
    start_dir = str((start or Path.cwd()).resolve())
    # From WSL, prefer Windows path if under /mnt/c
    if _is_wsl() and start_dir.startswith("/mnt/"):
        # /mnt/c/foo → C:\foo
        parts = start_dir.split("/")
        if len(parts) >= 3 and len(parts[2]) == 1:
            drive = parts[2].upper()
            rest = "\\".join(parts[3:])
            start_dir = f"{drive}:\\{rest}" if rest else f"{drive}:\\"

    ps = r"""
Add-Type -AssemblyName System.Windows.Forms
$f = New-Object System.Windows.Forms.OpenFileDialog
$f.Title = '{title}'
$f.Filter = 'Zip menus (*.zip)|*.zip|All files (*.*)|*.*'
$f.InitialDirectory = '{initial}'
$f.CheckFileExists = $true
if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {{
  Write-Output $f.FileName
}}
""".format(
        title=title.replace("'", "''"),
        initial=start_dir.replace("'", "''"),
    )

    candidates = []
    if sys.platform.startswith("win"):
        candidates.append("powershell")
        candidates.append("powershell.exe")
    else:
        # WSL / Linux with Windows host
        for name in (
            "powershell.exe",
            "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        ):
            if name.startswith("/") and Path(name).exists():
                candidates.append(name)
            elif shutil.which(name):
                candidates.append(name)

    for exe in candidates:
        try:
            proc = subprocess.run(
                [exe, "-NoProfile", "-STA", "-Command", ps],
                capture_output=True,
                text=True,
                timeout=120,
            )
            line = (proc.stdout or "").strip().splitlines()
            if line:
                raw = line[-1].strip()
                # WSL: convert C:\path to /mnt/c/path
                p = Path(raw)
                if _is_wsl() and len(raw) >= 3 and raw[1] == ":":
                    drive = raw[0].lower()
                    rest = raw[2:].replace("\\", "/").lstrip("/\\")
                    p = Path(f"/mnt/{drive}/{rest}")
                if p.exists():
                    return p
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None


def try_zenity_or_kdialog(
    *,
    title: str = "Pick a menu zip",
    start: Optional[Path] = None,
) -> Optional[Path]:
    start_dir = str((start or Path.cwd()).resolve())
    if shutil.which("zenity"):
        try:
            proc = subprocess.run(
                [
                    "zenity",
                    "--file-selection",
                    f"--title={title}",
                    f"--filename={start_dir}/",
                    "--file-filter=Zip menus | *.zip",
                    "--file-filter=All | *",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                p = Path(proc.stdout.strip())
                return p if p.exists() else None
        except (OSError, subprocess.TimeoutExpired):
            pass
    if shutil.which("kdialog"):
        try:
            proc = subprocess.run(
                [
                    "kdialog",
                    "--getopenfilename",
                    start_dir,
                    "*.zip|Zip menus",
                    "--title",
                    title,
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                p = Path(proc.stdout.strip())
                return p if p.exists() else None
        except (OSError, subprocess.TimeoutExpired):
            pass
    return None


def pick_menu_file_native(
    *,
    title: str = "Hey — pick your menu zip, idiot",
    start: Optional[Path] = None,
) -> Optional[Path]:
    """Best-effort native picker. Returns Path or None if user cancel / unavailable."""
    # Prefer Windows dialog when on Windows or WSL (most of this project's hosts)
    if sys.platform.startswith("win") or _is_wsl():
        p = try_windows_openfiledialog(title=title, start=start)
        if p is not None:
            return p
    p = try_tkinter_open(title=title, start=start)
    if p is not None:
        return p
    if not sys.platform.startswith("win"):
        p = try_zenity_or_kdialog(title=title, start=start)
        if p is not None:
            return p
    return None


def native_dialog_available() -> bool:
    """True if any native path is likely to work (not a guarantee)."""
    if sys.platform.startswith("win"):
        return True
    if _is_wsl() and (
        shutil.which("powershell.exe")
        or Path(
            "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
        ).exists()
    ):
        return True
    try:
        import tkinter  # noqa: F401

        return True
    except Exception:
        pass
    return bool(shutil.which("zenity") or shutil.which("kdialog"))
