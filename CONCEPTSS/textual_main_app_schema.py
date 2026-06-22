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
from typing import Dict, List, Optional, Callable, Any
from textual.app import App, Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding

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
    """Definition for one screen in the Textual App."""
    id: str
    title: str
    screen_class: str  # e.g. "PhaseDashboardScreen"
    module: Optional[str] = None  # which registered module owns this screen
    bindings: List[Binding] = field(default_factory=list)
    gutter_reactive: bool = True  # chrome / styling reacts to Gutter toggle


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

# Example screens
DEFAULT_SCHEMA.screens = {
    "home": ScreenDefinition(
        id="home",
        title="HOME — IRON PEARL COMMAND",
        screen_class="HomeGridScreen",
        bindings=[Binding("r", "roster_inventory", "Roster Inventory")],
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
        gutter_reactive=False  # roster stays clean/precise
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

# Example modules (these get discovered or registered at runtime)
DEFAULT_SCHEMA.modules = {
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

# ============================================================
# MAIN APP CLASS SKETCH (implement this)
# ============================================================

class GrokBuildTUI(App):
    """
    Main Textual App.
    - Loads DEFAULT_SCHEMA or user-extended schema
    - Manages venv-per-module or shared base venv
    - Handles Gutter Mode toggle (affects CSS classes / Rich styles on reactive screens)
    - Routes command palette to screens or module entry points
    - Renders C-64 bordered panels on demand
    """

    CSS_PATH = "grok_tui.tcss"  # optional external stylesheet for texture/themes

    BINDINGS = [
        Binding("g", "toggle_gutter", "Gutter Mode"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("?", "command_palette", "Command Palette"),
    ]

    def __init__(self, schema: TUIAppSchema = DEFAULT_SCHEMA):
        super().__init__()
        self.schema = schema
        self.gutter_active = schema.gutter_mode_default
        # TODO: env sniffer, venv manager, module discovery here

    def on_mount(self) -> None:
        self.title = self.schema.app_title
        # Push home screen, apply initial Gutter styling if active
        if self.gutter_active:
            self.add_class("gutter-active")

    def action_toggle_gutter(self) -> None:
        self.gutter_active = not self.gutter_active
        if self.gutter_active:
            self.add_class("gutter-active")
            # TODO: push "Gutter visuals enabled — heat-reactive chrome live" notification
        else:
            self.remove_class("gutter-active")

    # TODO: implement screen switching, module loading after venv prep,
    # command palette that calls roster boot / grok build phase X etc.


# ============================================================
# HOW TO EXTEND
# ============================================================
"""
1. Create new .py in modules/<category>/
2. Add REGISTERED_MODULE dict + entry function
3. Add ScreenDefinition + ModuleRegistration to schema (or auto-discover)
4. Implement the actual Screen subclass with Textual widgets
5. Wire Gutter reactivity via CSS classes or Rich renderables if desired

Gutter Mode visual hook example (in a reactive screen):
    if app.gutter_active:
        self.add_class("high-heat-ruined")
        # Then in .tcss: .high-heat-ruined { color: #ff00aa; text-style: bold; }
"""

if __name__ == "__main__":
    app = GrokBuildTUI()
    app.run()