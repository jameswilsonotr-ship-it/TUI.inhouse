# TUI Menu Research - Copyable Examples

## Overview
Research based on the Grok TUI design files (principles and walkthrough) and Textual framework for building modular, branded TUI menus.

The design calls for:
- Home grid with big friendly buttons/tiles for major areas (Grok Build Phases, Roster Inventory, Overlap Engine, Hardware Rig, Voice Pipeline, Drive Partitions, etc.).
- Command palette for typing commands like "roster inventory", "advance phase 3", "enter gutter".
- Status bar for Heat/FILTH/Gutter indicators.
- Gutter Mode toggle affecting chrome.
- Modular screens launched from menu.
- C-64 bordered, Olivia Dev Alpha hacker-girl feel (dark terminal, glowing accents, gem-red highlights, clean bordered panels, heat-reactive).

Textual provides:
- `Horizontal` and `Vertical` containers for layouts.
- `Button`, `Static`, `Label`, `DataTable`, `Log`, etc.
- `App` with `compose`, `BINDINGS`, `CSS`.
- Command palette via `textual.command` or custom.
- Screens for switching views.
- CSS for texture and Gutter Mode (e.g., .gutter-active classes).

## Copyable Examples

### Example 1: Basic Home Grid Menu (from schema and design)
```python
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Header, Footer, Label
from textual.binding import Binding

class HomeGridScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("[bold]GROK BUILD — IRON PEARL TUI[/]", id="title")
        with Grid(id="home-grid"):
            yield Button("Grok Build Phases", id="phase_dashboard", variant="primary")
            yield Button("Roster", id="roster")
            yield Button("Hardware", id="hardware")
            yield Button("Wrap Python", id="wrap_any")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        self.app.notify(f"Would launch: {btn_id}")
        # In full: self.app.push_screen(PhaseDashboardScreen() etc.)

class GrokTUIApp(App):
    CSS = """
    Screen { align: center middle; }
    #home-grid { grid-size: 2; grid-gutter: 1 2; padding: 1; }
    Button { width: 100%; height: 3; }
    .gutter-active { background: #1a0a0a; color: #ffaa00; }
    """

    BINDINGS = [
        Binding("g", "toggle_gutter", "Gutter Mode"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self):
        self.title = "GROK BUILD — IRON PEARL TUI"
        self.push_screen(HomeGridScreen())

    def action_toggle_gutter(self):
        if "gutter-active" in self.classes:
            self.remove_class("gutter-active")
        else:
            self.add_class("gutter-active")

if __name__ == "__main__":
    GrokTUIApp().run()
```

### Example 2: Sidebar Menu (modular navigation)
```python
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static, ListView, ListItem

class SidebarMenu(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Menu", classes="title")
        yield ListView(
            ListItem(Button("Phases", id="phases")),
            ListItem(Button("Roster", id="roster")),
            ListItem(Button("Hardware", id="hardware")),
            ListItem(Button("Wrap", id="wrap")),
        )

    def on_button_pressed(self, event: Button.Pressed):
        # Route to screen
        pass

class MainApp(App):
    CSS = """
    SidebarMenu { width: 20; background: $surface; }
    .title { text-style: bold; padding: 1; }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield SidebarMenu()
            yield Static("Main Content Area", id="content")

if __name__ == "__main__":
    MainApp().run()
```

### Example 3: Command Palette Integration (Textual built-in)
```python
from textual.app import App
from textual.command import Provider, Hit

class TUICommands(Provider):
    async def search(self, query: str):
        commands = [
            ("phases", "Launch Phases Dashboard"),
            ("roster", "Roster Inventory"),
            ("gutter", "Toggle Gutter Mode"),
        ]
        for cmd, desc in commands:
            if query.lower() in cmd:
                yield Hit(1, desc, lambda: self.app.notify(f"Ran {cmd}"))

class MenuApp(App):
    COMMANDS = {TUICommands}

    def on_mount(self):
        self.action_show_command_palette()
```

### Example 4: Gutter Mode Reactive Menu
Add CSS:
```
.gutter-active SidebarMenu { background: #330000; color: #ff4444; }
```

Toggle as in previous examples.

## Notes from Design
- Make it feel like Grok Build CLI + Olivia Dev Alpha.
- Map 7-phase pipeline to menu items/screens.
- Support wrap for arbitrary scripts.
- C-64 borders via CSS or Static with borders.
- Async for streaming logs in menu areas.
- Modular: each menu item can be a registered module.

These examples are directly inspired by the walkthrough's home grid, screens, command palette, and texture requirements. Adapt for full launcher integration.
