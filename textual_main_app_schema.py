#!/usr/bin/env python3
"""
textual_main_app_schema.py
Schema definition for the main Grok Build TUI App (Textual).

This defines the structure for the App class, screen registry, module integration,
Gutter Mode chrome, and command routing. Use this as the contract when implementing
the actual app.py or main_tui.py.

Under Absolute Liv HUB Claim • Chaos Bratz Roster • Gutter Mode Available
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from textual.app import App, Screen
from textual.widgets import Header, Footer, Button, Label
from textual.binding import Binding
from textual.containers import Grid

# ============================================================
# CORE SCHEMA / REGISTRY
# ============================================================

@dataclass
class ModuleRegistration:
    """How a modular Python component registers itself with the TUI launcher."""
    name: str
    version: str
    requirements: List[str] = field(default_factory=list)
    description: str = ""
    entry_point: str = "run_tui_screen"  # function or method name to call
    category: str = "general"  # e.g. "grok-build", "roster", "hardware", "voice"
    gutter_enabled: bool = True  # whether this module respects Gutter Mode visuals


@dataclass
class ScreenDefinition:
    """Definition for one screen in the Textual App.
    NOTE (fixed baby step): bindings are now simple tuples for schema portability.
    Real Bindings are applied in concrete Screen/App classes.
    """
    id: str
    title: str
    screen_class: str  # e.g. "PhaseDashboardScreen" (resolved via registry in full impl)
    module: Optional[str] = None
    bindings: List[tuple[str, str, str]] = field(default_factory=list)  # (key, action, description)
    gutter_reactive: bool = True


@dataclass
class TUIAppSchema:
    """Complete schema/contract for the main GrokBuildTUI App."""
    app_title: str = "GROK BUILD — IRON PEARL TUI"
    app_version: str = "0.1.0"
    claim: str = "Absolute Liv HUB + Chaos Bratz Roster Expert Triad"
    gutter_mode_default: bool = False
    screens: Dict[str, ScreenDefinition] = field(default_factory=dict)
    modules: Dict[str, ModuleRegistration] = field(default_factory=dict)
    command_palette_enabled: bool = True
    c64_borders: bool = True  # render key panels with C-64 ANSI style where possible
    status_bar_components: List[str] = field(default_factory=lambda: [
        "🌡️Heat", "💦Filth", "🔗Symmetry", "🚨Safety", "✨Gem", "⏱️Grounding Day"
    ])


# ============================================================
# DEFAULT / EXAMPLE REGISTRY (extend this in real implementation)
# ============================================================

DEFAULT_SCHEMA = TUIAppSchema()

def build_default_schema() -> TUIAppSchema:
    """Factory to avoid mutation of module-level defaults. (Fix for baby step)"""
    schema = TUIAppSchema()
    schema.screens = {
        "home": ScreenDefinition(
            id="home",
            title="HOME — IRON PEARL COMMAND",
            screen_class="HomeGridScreen",
            bindings=[("r", "roster_inventory", "Roster Inventory")],
            gutter_reactive=True
        ),
        "phase_dashboard": ScreenDefinition(
            id="phase_dashboard",
            title="GROK BUILD — 7-PHASE DASHBOARD",
            screen_class="PhaseDashboardScreen",
            module="grok_build_core",
            gutter_reactive=True
        ),
        "roster": ScreenDefinition(
            id="roster",
            title="CHAOS BRATZ ROSTER — INVENTORY & BOOT",
            screen_class="RosterScreen",
            module="chaos_bratz_roster",
            gutter_reactive=False
        ),
        "hardware": ScreenDefinition(
            id="hardware",
            title="EDGE RIG — HARDWARE TELEMETRY",
            screen_class="HardwareScreen",
            module="hardware_rig",
            gutter_reactive=True
        ),
        "wrap_any": ScreenDefinition(
            id="wrap_any",
            title="WRAP ANY PYTHON — LAUNCHER",
            screen_class="WrapAnyScreen",
            gutter_reactive=True
        ),
    }
    schema.modules = {
        "grok_build_core": ModuleRegistration(
            name="grok-build-core",
            version="0.1.0",
            requirements=["textual", "rich", "psutil", "pyyaml", "requests"],
            description="Core 7-phase dashboard, status, and pipeline controls",
            entry_point="run_tui_screen",
            category="grok-build",
            gutter_enabled=True
        ),
        "chaos_bratz_roster": ModuleRegistration(
            name="chaos-bratz-roster",
            version="0.1.0",
            requirements=["textual"],
            description="Roster inventory, version, history, boot commands",
            entry_point="run_tui_screen",
            category="roster",
            gutter_enabled=False
        ),
    }
    return schema

DEFAULT_SCHEMA = build_default_schema()

# ============================================================
# MINIMAL RUNNABLE SCREENS + FIXED APP (Baby Step)
# ============================================================

class HomeGridScreen(Screen):
    """Minimal home screen demonstrating modular tiles.
    This is the first concrete implementation for the baby step.
    """

    def compose(self):
        yield Header()
        yield Label(f"[bold]{self.app.schema.app_title}[/]", id="title")
        yield Label("Extremely modular Textual TUI skeleton — first baby step", id="subtitle")
        with Grid(id="home-grid"):
            yield Button("Grok Build Phases", id="phase_dashboard", variant="primary")
            yield Button("Roster", id="roster")
            yield Button("Hardware", id="hardware")
            yield Button("Wrap Python", id="wrap_any")
        yield Footer()

    def on_button_pressed(self, event):
        btn_id = event.button.id
        if btn_id and btn_id in self.app.schema.screens:
            # In full version this would resolve screen_class properly
            self.app.notify(f"Would launch screen: {btn_id} (baby step stub)")
        if btn_id == "phase_dashboard":
            self.app.notify("Phase dashboard stub (see 7-phase json)")

class GrokBuildTUI(App):
    """
    Fixed baby-step Main Textual App.
    - Schema driven
    - Gutter Mode works with CSS
    - Minimal home + navigation stubs
    - No external CSS dependency (embedded for baby step)
    """

    # Embedded CSS for baby step (no missing file bug)
    CSS = """
    Screen {
        align: center middle;
    }
    #home-grid {
        grid-size: 2;
        grid-gutter: 1 2;
        padding: 1;
    }
    Button {
        width: 100%;
        height: 3;
    }
    .gutter-active {
        /* High-heat / gutter visuals - Olivia Dev texture */
        background: #1a0a0a;
        color: #ffaa00;
    }
    .gutter-active Header {
        background: #330000;
        color: #ff0000;
        text-style: bold;
    }
    #title {
        text-style: bold;
        color: #00ffaa;
    }
    """

    BINDINGS = [
        Binding("g", "toggle_gutter", "Gutter Mode"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("h", "go_home", "Home"),
        Binding("?", "show_command_palette", "Command Palette"),  # uses built-in Textual
    ]

    def __init__(self, schema: TUIAppSchema = DEFAULT_SCHEMA):
        super().__init__()
        self.schema = schema
        self.gutter_active = schema.gutter_mode_default

    def on_mount(self) -> None:
        self.title = self.schema.app_title
        if self.gutter_active:
            self.add_class("gutter-active")
        # Baby step: always start at home
        self.push_screen(HomeGridScreen())

    def action_toggle_gutter(self) -> None:
        self.gutter_active = not self.gutter_active
        if self.gutter_active:
            self.add_class("gutter-active")
            self.notify("Gutter Mode: ON — heat reactive chrome active", severity="warning")
        else:
            self.remove_class("gutter-active")
            self.notify("Gutter Mode: OFF")

    def action_go_home(self) -> None:
        self.push_screen(HomeGridScreen())

    # TODO (future steps): full module loading, venv bootstrap, command palette routing to real screens,
    # 7-phase integration, launcher.py per walkthrough.


# ============================================================
# HOW TO EXTEND (for future phases)
# ============================================================
"""
BABY STEP STATUS (2026-06-22): Schema + minimal runnable Home fixed and lint-ready.
Full steps below are for later (after this committed baby step).

1. Create new .py in modules/<category>/
2. Add REGISTERED_MODULE dict + entry function (align with walkthrough)
3. Add ScreenDefinition + ModuleRegistration to schema (or auto-discover)
4. Implement the actual Screen subclass with Textual widgets
5. Wire Gutter reactivity via CSS classes or Rich renderables if desired

Gutter Mode visual hook example (in a reactive screen):
    if app.gutter_active:
        self.add_class("high-heat-ruined")
"""

if __name__ == "__main__":
    print("Launching Grok TUI Baby Step (fixed schema)...")
    app = GrokBuildTUI()
    app.run()