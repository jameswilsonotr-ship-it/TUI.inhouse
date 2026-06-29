#!/usr/bin/env python3
"""
minimal_tui.py - Minimal working TUI based on the design principles and walkthrough.
Uses Textual for home grid menu as per Grok TUI Launcher design.
Supports Gutter Mode, basic navigation.
Run with: python minimal_tui.py
"""

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Header, Footer, Label, Static
from textual.binding import Binding
from textual.screen import Screen

class HomeScreen(Screen):
    """Home grid menu as per design."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("[bold]GROK BUILD — IRON PEARL TUI[/]", id="title")
        yield Static("Modular launcher for 7-phase pipeline + more", id="subtitle")
        with Grid(id="home-grid"):
            yield Button("Grok Build Phases", id="phases", variant="primary")
            yield Button("Roster", id="roster")
            yield Button("Hardware", id="hardware")
            yield Button("Wrap Script", id="wrap")
            yield Button("Toggle Gutter", id="gutter")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "phases":
            self.app.notify("Launching Phases Dashboard (stub)")
        elif button_id == "roster":
            self.app.notify("Launching Roster (stub)")
        elif button_id == "hardware":
            self.app.notify("Launching Hardware Telemetry (stub)")
        elif button_id == "wrap":
            self.app.notify("Wrap mode (stub) - point to a .py")
        elif button_id == "gutter":
            self.app.action_toggle_gutter()

class MinimalTUI(App):
    """Minimal TUI per design."""
    CSS = """
    Screen {
        align: center middle;
    }
    #home-grid {
        grid-size: 2 3;
        grid-gutter: 1 2;
        padding: 1;
    }
    Button {
        width: 100%;
        height: 3;
    }
    #title {
        text-style: bold;
        color: #00ffaa;
    }
    .gutter-active {
        background: #1a0a0a;
        color: #ffaa00;
    }
    .gutter-active Header {
        background: #330000;
        color: #ff4444;
    }
    """

    BINDINGS = [
        Binding("g", "toggle_gutter", "Gutter Mode"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("h", "go_home", "Home"),
    ]

    def on_mount(self) -> None:
        self.title = "GROK BUILD — IRON PEARL TUI"
        self.push_screen(HomeScreen())

    def action_toggle_gutter(self) -> None:
        if "gutter-active" in self.classes:
            self.remove_class("gutter-active")
            self.notify("Gutter Mode: OFF")
        else:
            self.add_class("gutter-active")
            self.notify("Gutter Mode: ON — heat reactive chrome active", severity="warning")

    def action_go_home(self) -> None:
        self.push_screen(HomeScreen())

if __name__ == "__main__":
    MinimalTUI().run()
