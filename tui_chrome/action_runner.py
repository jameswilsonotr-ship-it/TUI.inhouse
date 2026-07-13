"""PR-13 runtime — invoke menu actions and stream output (CODE-CALL-DISPLAY).

See docs/menu-system/CODE-CALL-DISPLAY.md.
"""
from __future__ import annotations

import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence


LineCallback = Callable[[str, str], None]  # (stream, text) stream in out|err|ctrl|sys


@dataclass
class RunResult:
    """Result of one action run."""

    returncode: int
    exit_level: int
    stdout: str = ""
    stderr: str = ""
    duration_sec: float = 0.0
    render_as: str = "log"
    window_title: Optional[str] = None
    timed_out: bool = False


def _safe_under_root(pack_root: Path, target: str) -> Path:
    """Resolve target under pack_root; raise if escapes."""
    pack_root = pack_root.resolve()
    # disallow absolute targets outside pack
    raw = Path(target)
    if raw.is_absolute():
        resolved = raw.resolve()
    else:
        resolved = (pack_root / target).resolve()
    try:
        resolved.relative_to(pack_root)
    except ValueError as exc:
        raise ValueError(f"target outside pack root: {target}") from exc
    return resolved


def build_env(
    *,
    pack_root: Path,
    menu_id: str,
    item_id: str,
    action: Dict[str, Any],
    log_dir: Path,
    session_id: str,
    schema_version: str = "1.0.0",
    extra: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Build environment for a menu action subprocess."""
    output = action.get("output") or {}
    env = os.environ.copy()
    env.update(
        {
            "TUI_MENU_SCHEMA": schema_version,
            "TUI_MENU_ID": menu_id,
            "TUI_ITEM_ID": item_id,
            "TUI_ACTION_TYPE": str(action.get("type") or ""),
            "TUI_OUTPUT_WINDOW": str(output.get("window") or "main_output"),
            "TUI_RENDER_AS": str(output.get("render_as") or "log"),
            "TUI_PACK_ROOT": str(pack_root.resolve()),
            "TUI_LOG_DIR": str(log_dir.resolve()),
            "TUI_SESSION_ID": session_id,
            "PYTHONUNBUFFERED": "1",
        }
    )
    action_env = action.get("env") or {}
    if isinstance(action_env, dict):
        for k, v in action_env.items():
            env[str(k)] = str(v)
    if extra:
        env.update(extra)
    return env


def build_argv(action: Dict[str, Any], pack_root: Path, *, chunk: Optional[str] = None) -> List[str]:
    """Build process argv for run_python / legacy_harness."""
    atype = action.get("type") or ""
    target = str(action.get("target") or "")
    if not target:
        raise ValueError("action missing target")

    if atype == "legacy_harness":
        script = _safe_under_root(pack_root, target)
        if not script.is_file():
            # try harness.py fallback
            alt = pack_root / "harness.py"
            if alt.is_file():
                script = alt
            else:
                raise FileNotFoundError(f"harness not found: {target}")
        cmd = [sys.executable, str(script)]
        if chunk:
            cmd += ["--chunk", chunk]
        log_dir = action.get("_log_dir")  # injected by runner
        if log_dir:
            cmd += ["--log-dir", str(log_dir)]
        return cmd

    if atype == "run_python":
        script = _safe_under_root(pack_root, target)
        if not script.is_file():
            raise FileNotFoundError(f"script not found: {target}")
        cmd = [sys.executable, str(script)]
        args = action.get("args")
        if isinstance(args, list):
            cmd.extend(str(a) for a in args)
        elif isinstance(args, dict):
            for key, val in args.items():
                flag = f"--{key}" if not str(key).startswith("-") else str(key)
                if val is None:
                    continue
                if isinstance(val, bool):
                    if val:
                        cmd.append(flag)
                    continue
                cmd.extend([flag, str(val)])
        return cmd

    if atype == "run_shell":
        raise PermissionError("run_shell is disabled by default")

    raise ValueError(f"unsupported action type for subprocess: {atype}")


def map_exit_level(returncode: int) -> int:
    """Map process returncode → exit_level (0/1/2)."""
    if returncode == 0:
        return 0
    if returncode == 2:
        return 2
    return 1


def _handle_control_line(line: str, state: Dict[str, Any]) -> Optional[str]:
    """Process TUI_* control lines; return None if consumed."""
    s = line.strip()
    if s.startswith("TUI_RENDER:"):
        mode = s.split(":", 1)[1].strip().lower()
        if mode in ("log", "markdown", "html", "ansi", "json"):
            state["render_as"] = mode
        return None
    if s.startswith("TUI_TITLE:"):
        state["window_title"] = s.split(":", 1)[1].strip()
        return None
    if s == "TUI_CLEAR":
        state["clear"] = True
        return None
    if s.startswith("TUI_EVENT:"):
        # host may handle; still suppress raw line
        state.setdefault("events", []).append(s.split(":", 1)[1].strip())
        return None
    return line


def run_action(
    *,
    pack_root: Path,
    menu_id: str,
    item_id: str,
    action: Dict[str, Any],
    log_dir: Path,
    session_id: str,
    schema_version: str = "1.0.0",
    chunk: Optional[str] = None,
    on_line: Optional[LineCallback] = None,
    python_exe: Optional[str] = None,
) -> RunResult:
    """Run a menu action as subprocess; stream lines via ``on_line``.

    Args:
        pack_root: Menu pack root.
        menu_id / item_id: For env.
        action: Resolved ActionSpec (with output defaults).
        log_dir: Host log directory.
        session_id: Correlation id.
        chunk: Optional date for legacy_harness.
        on_line: Callback(stream, text) for live UI.
        python_exe: Override interpreter (defaults to sys.executable).
    """
    atype = action.get("type") or ""
    if atype in ("noop", "open_menu", "open_url", "builtin"):
        if on_line:
            on_line("sys", f"action type {atype!r} is host-side (not subprocess)\n")
        return RunResult(returncode=0, exit_level=0, render_as="log")

    # inject log dir for legacy argv builder
    action = dict(action)
    action["_log_dir"] = str(log_dir.resolve())
    log_dir.mkdir(parents=True, exist_ok=True)

    try:
        argv = build_argv(action, pack_root, chunk=chunk)
    except Exception as exc:
        if on_line:
            on_line("err", f"{exc}\n")
        return RunResult(returncode=1, exit_level=1, stderr=str(exc))

    if python_exe and argv and argv[0] == sys.executable:
        argv = [python_exe] + argv[1:]

    env = build_env(
        pack_root=pack_root,
        menu_id=menu_id,
        item_id=item_id,
        action=action,
        log_dir=log_dir,
        session_id=session_id,
        schema_version=schema_version,
    )
    cwd = pack_root
    rel_cwd = action.get("cwd") or "."
    if rel_cwd and rel_cwd != ".":
        try:
            cwd = _safe_under_root(pack_root, rel_cwd)
        except ValueError as exc:
            if on_line:
                on_line("err", f"{exc}\n")
            return RunResult(returncode=1, exit_level=1, stderr=str(exc))

    timeout = float(action.get("timeout_sec") or 120)
    output = action.get("output") or {}
    state: Dict[str, Any] = {
        "render_as": str(output.get("render_as") or "log"),
        "window_title": None,
        "events": [],
    }

    if on_line:
        on_line("sys", f"$ {' '.join(shlex.quote(a) for a in argv)}\n")

    stdout_acc: List[str] = []
    stderr_acc: List[str] = []
    start = time.time()
    timed_out = False
    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
    except Exception as exc:
        if on_line:
            on_line("err", f"spawn failed: {exc}\n")
        return RunResult(returncode=1, exit_level=1, stderr=str(exc))

    assert proc.stdout is not None and proc.stderr is not None

    def _read_stream(stream_name: str, pipe) -> None:
        for line in pipe:
            if stream_name == "out":
                handled = _handle_control_line(line.rstrip("\n"), state)
                if handled is None:
                    if state.pop("clear", False) and on_line:
                        on_line("ctrl", "CLEAR")
                    continue
                line_out = handled + "\n" if not handled.endswith("\n") else handled
                stdout_acc.append(line_out)
                if on_line:
                    on_line("out", line_out)
            else:
                stderr_acc.append(line if line.endswith("\n") else line + "\n")
                if on_line:
                    on_line("err", line if line.endswith("\n") else line + "\n")

    # Sequential read is simpler/safer for Textual workers (small demos)
    # Read stdout then stderr after wait with communicate for reliability
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        timed_out = True
        if on_line:
            on_line("err", "TIMEOUT\n")

    rc = proc.returncode if proc.returncode is not None else 1
    if timed_out:
        rc = 1

    for line in (out or "").splitlines():
        handled = _handle_control_line(line, state)
        if handled is None:
            if state.pop("clear", False) and on_line:
                on_line("ctrl", "CLEAR")
            continue
        text = handled + "\n"
        stdout_acc.append(text)
        if on_line:
            on_line("out", text)
    for line in (err or "").splitlines():
        text = line + "\n"
        stderr_acc.append(text)
        if on_line:
            on_line("err", text)

    duration = time.time() - start
    level = map_exit_level(rc)
    if on_line:
        on_line(
            "sys",
            f"── exit {rc} · level {level} · {duration:.2f}s ──\n",
        )
    return RunResult(
        returncode=rc,
        exit_level=level,
        stdout="".join(stdout_acc),
        stderr="".join(stderr_acc),
        duration_sec=duration,
        render_as=str(state.get("render_as") or "log"),
        window_title=state.get("window_title"),
        timed_out=timed_out,
    )
