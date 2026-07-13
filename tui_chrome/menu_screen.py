"""PR-11/12/13 runtime — Textual screen for a loaded MenuPack.

Standard layout: title · menu list · help · output log · run controls.
"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, ListItem, ListView, Log, Static

from tui_chrome.action_runner import run_action
from tui_chrome.menu_model import (
    MenuPack,
    leaf_items,
    merge_output_defaults,
    resolve_action,
)


class MenuPackScreen(Screen):
    """Host a v1 menu pack: pick item → run action → stream to output window."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
        Binding("enter", "run_selected", "Run", show=True),
        Binding("r", "run_selected", "Run", show=False),
    ]

    CSS = """
    MenuPackScreen { layout: vertical; }
    #menu-title { text-style: bold; color: #00ffaa; padding: 0 1; height: 1; }
    #menu-body { height: 1fr; }
    #menu-left { width: 36; min-width: 24; border: heavy #664466; }
    #menu-right { width: 1fr; }
    #item-help {
        height: 6;
        border: solid #444;
        padding: 0 1;
        color: #e8d0e0;
        background: #120810;
    }
    #main-output {
        height: 1fr;
        border: double #ff44aa;
        background: #0a0610;
    }
    #menu-actions { height: 3; padding: 0 1; }
    .pane-title { text-style: bold; color: #ff88cc; background: #220018; padding: 0 1; }
    """

    def __init__(self, pack: MenuPack, **kwargs) -> None:
        super().__init__(**kwargs)
        self.pack = pack
        self._items: List[Dict[str, Any]] = leaf_items(pack.doc)
        self._selected_idx: int = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.pack.title, id="menu-title")
        with Horizontal(id="menu-body"):
            with Vertical(id="menu-left"):
                yield Static(" MENU ", classes="pane-title")
                yield ListView(id="menu-list")
            with Vertical(id="menu-right"):
                yield Static(" HELP ", classes="pane-title")
                yield Static("", id="item-help")
                yield Static(" OUTPUT ", classes="pane-title")
                yield Log(id="main-output", highlight=True, max_lines=5000)
        with Horizontal(id="menu-actions"):
            yield Button("Run", id="btn-run", variant="success")
            yield Button("Back", id="btn-back", variant="default")
        yield Static("Enter/r Run · Esc Back · ↑↓ select", id="key-help")
        yield Footer()

    def on_mount(self) -> None:
        lv = self.query_one("#menu-list", ListView)
        for node in self._items:
            label = str(node.get("label") or node.get("id") or "?")
            icon = node.get("icon") or ""
            hot = node.get("hotkey")
            text = f"{icon} {label}".strip()
            if hot:
                text = f"[{hot}] {text}"
            item = ListItem(Static(text))
            item.data = node  # type: ignore[attr-defined]
            lv.append(item)
        if self._items:
            self._select_idx(0)
        out = self.query_one("#main-output", Log)
        out.write_line(f"[dim]Pack:[/dim] {self.pack.id}  [dim]root:[/dim] {self.pack.pack_root}")
        out.write_line(f"[dim]schema:[/dim] {self.pack.schema_version}  [dim]items:[/dim] {len(self._items)}")
        out.write_line("[magenta]Select an item and press Run (or Enter).[/magenta]")

    def _select_idx(self, idx: int) -> None:
        if not self._items:
            return
        self._selected_idx = max(0, min(idx, len(self._items) - 1))
        node = self._items[self._selected_idx]
        help_w = self.query_one("#item-help", Static)
        help_txt = node.get("help") or node.get("description") or self.pack.doc.get("description") or ""
        label = node.get("label") or node.get("id")
        help_w.update(f"[bold]{label}[/bold]\n{help_txt}")
        try:
            lv = self.query_one("#menu-list", ListView)
            lv.index = self._selected_idx
        except Exception:
            pass

    @on(ListView.Selected)
    def _on_list_selected(self, event: ListView.Selected) -> None:
        try:
            idx = event.list_view.index
            if idx is not None:
                self._select_idx(int(idx))
        except Exception:
            pass

    @on(ListView.Highlighted)
    def _on_list_hi(self, event: ListView.Highlighted) -> None:
        try:
            if event.list_view.index is not None:
                self._select_idx(int(event.list_view.index))
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-run":
            self.action_run_selected()
        elif event.button.id == "btn-back":
            self.app.pop_screen()

    def action_run_selected(self) -> None:
        """Run the currently selected menu item action."""
        if not self._items:
            return
        node = self._items[self._selected_idx]
        action = resolve_action(node, self.pack.actions_registry)
        if not action:
            self._out("[yellow]No action on this item.[/yellow]")
            return
        action = merge_output_defaults(action, self.pack.defaults)
        atype = action.get("type")
        if atype == "builtin":
            self._handle_builtin(str(action.get("target") or ""))
            return
        if atype in ("open_menu", "open_url", "noop"):
            self._out(f"[dim]{atype}: {action.get('target')} (not a subprocess)[/dim]")
            return
        self._run_action_worker(node, action)

    def _handle_builtin(self, target: str) -> None:
        if target in ("gutter_toggle", "gutter"):
            if hasattr(self.app, "action_toggle_gutter"):
                self.app.action_toggle_gutter()  # type: ignore[attr-defined]
                self._out("[magenta]Gutter toggled[/magenta]")
            else:
                self._out("[yellow]Host has no gutter toggle[/yellow]")
        elif target == "quit":
            self.app.exit()
        else:
            self._out(f"[yellow]Unknown builtin: {target}[/yellow]")

    def _out(self, msg: str) -> None:
        try:
            self.query_one("#main-output", Log).write_line(msg)
        except Exception:
            pass

    def _clear_output(self) -> None:
        try:
            log = self.query_one("#main-output", Log)
            log.clear()
        except Exception:
            pass

    @work(exclusive=True, thread=True)
    def _run_action_worker(self, node: Dict[str, Any], action: Dict[str, Any]) -> None:
        """Thread worker: run action and stream lines to the Log."""
        output = action.get("output") or {}
        if output.get("clear", True):
            self.app.call_from_thread(self._clear_output)

        item_id = str(node.get("id") or "item")
        label = str(node.get("label") or item_id)
        self.app.call_from_thread(self._out, f"[bold cyan]▶ {label}[/bold cyan] ({action.get('type')})")

        # Resolve host log dir
        log_dir = Path(os.environ.get("TUI_LOG_DIR") or "logs")
        if hasattr(self.app, "dirs") and isinstance(getattr(self.app, "dirs"), dict):
            log_dir = Path(self.app.dirs.get("logs", log_dir))  # type: ignore[attr-defined]
        log_dir = log_dir / "menu_runs" / item_id
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        def on_line(stream: str, text: str) -> None:
            if stream == "ctrl" and text.strip() == "CLEAR":
                self.app.call_from_thread(self._clear_output)
                return
            # strip trailing newline for Log.write_line
            body = text.rstrip("\n")
            if stream == "err":
                body = f"[red]{body}[/red]"
            elif stream == "sys":
                body = f"[dim]{body}[/dim]"
            elif stream == "out":
                pass
            self.app.call_from_thread(self._out, body)

        result = run_action(
            pack_root=self.pack.pack_root,
            menu_id=self.pack.id,
            item_id=item_id,
            action=action,
            log_dir=log_dir,
            session_id=session_id,
            schema_version=self.pack.schema_version,
            on_line=on_line,
        )
        color = "green" if result.exit_level == 0 else ("yellow" if result.exit_level == 2 else "red")
        self.app.call_from_thread(
            self._out,
            f"[{color}]done exit_level={result.exit_level} rc={result.returncode} "
            f"render={result.render_as}[/{color}]",
        )
