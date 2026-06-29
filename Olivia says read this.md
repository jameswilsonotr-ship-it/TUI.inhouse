# Textual TCSS, Gutter Mode, and Minimal Multi-Pane Starter Template

**Date**: 2026-06-29  
**Purpose**: Consolidated guide for building a deterministic, rock-solid TUI menuing system using Textual. Includes TCSS explanation, Gutter Mode implementation via switchable CSS layers, widget patterns, multi-pane layouts, subprocess streaming, and a complete minimal starter template.

---

## What is TCSS? (Textual CSS)

**TCSS** stands for **Textual CSS**. It is Textual’s built-in styling system that works similarly to web CSS but is designed specifically for terminal user interfaces.

### Key Features of TCSS

- **CSS-like syntax** with selectors, properties, and values.
- **Variables** (like `$accent`, `$surface`, `$text`).
- **Pseudo-classes** (`:hover`, `:focus`).
- **Layout control** (`layout: vertical`, `dock: top`, `grid-size`).
- **Theming support** — you can define multiple themes or switch styles dynamically.
- Applied via `CSS_PATH = "app.tcss"` in your App or inline `CSS = """..."""`.

Example:

```css
Screen {
    background: $surface;
}

Button {
    background: $accent;
    color: $text;
}

Button:hover {
    background: $accent-darken-1;
}
```

---

## Gutter Mode Implementation (Two CSS Layers)

We implement **Gutter Mode** using **two separate CSS layers** that can be toggled cleanly without menus or complex logic.

### Design Goals
- Clean separation between "Normal" and "Gutter" visual states.
- Easy to extend later into full themes.
- Controlled by a simple boolean + class toggle.
- No LLM involvement — purely deterministic.

### Recommended Approach: Class-Based Theme Switching

We use a single TCSS file with a `.gutter-active` class that overrides styles when active.

**Example: `grok_tui.tcss`**

```css
/* ===================== NORMAL MODE (Default) ===================== */
Screen {
    background: $surface;
}

.pane {
    border: tall $accent;
    padding: 1;
}

.menu-item {
    color: $text;
}

.log {
    background: $surface-darken-1;
}

/* ===================== GUTTER MODE ===================== */
.gutter-active .pane {
    border: thick $error;
    background: $surface-darken-2;
}

.gutter-active .menu-item {
    color: $error;
    text-style: bold;
}

.gutter-active .log {
    background: #1a0a0a; /* Darker, more intense */
    color: #ffaaaa;
}

.gutter-active Header {
    background: $error;
    color: $text;
}
```

### How to Toggle Gutter Mode in Code

```python
from textual.app import App
from textual.reactive import reactive

class GrokTUI(App):
    CSS_PATH = "grok_tui.tcss"

    gutter_active: reactive[bool] = reactive(False)

    def watch_gutter_active(self, active: bool) -> None:
        """Automatically add/remove the class when the value changes."""
        if active:
            self.add_class("gutter-active")
        else:
            self.remove_class("gutter-active")

    def action_toggle_gutter(self) -> None:
        """Bind this to a key (e.g. 'g')."""
        self.gutter_active = not self.gutter_active
```

You can also bind it to a key in `BINDINGS`:

```python
BINDINGS = [
    ("g", "toggle_gutter", "Toggle Gutter Mode"),
]
```

This approach is clean, bounded, and easy to extend into full theme switching later (e.g. `self.add_class("theme-dark")` or `"theme-gutter"`).

---

## Minimal Multi-Pane Starter Template

Here is a complete, runnable minimal starter that includes:

- Multi-pane layout (Menu | Output Log | Status)
- Gutter Mode with two CSS layers
- Basic menu using `ListView`
- Placeholder for subprocess streaming into `Log`

**File: `minimal_tui.py`**

```python
#!/usr/bin/env python3
"""
Minimal Multi-Pane TUI Starter with Gutter Mode
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, ListView, ListItem, Log
from textual.reactive import reactive

class MinimalTUI(App):
    CSS_PATH = "grok_tui.tcss"
    BINDINGS = [
        ("g", "toggle_gutter", "Toggle Gutter"),
        ("q", "quit", "Quit"),
    ]

    gutter_active: reactive[bool] = reactive(False)

    def watch_gutter_active(self, active: bool) -> None:
        if active:
            self.add_class("gutter-active")
        else:
            self.remove_class("gutter-active")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="main-area"):
            # Menu Pane
            with Vertical(id="menu-pane", classes="pane"):
                yield Static("MENU", classes="pane-title")
                yield ListView(
                    ListItem(Static("1. Run Ingestion")),
                    ListItem(Static("2. 7-Phase Status")),
                    ListItem(Static("3. Test Harness")),
                    id="main-menu"
                )

            # Output Pane
            with Vertical(id="output-pane", classes="pane"):
                yield Static("OUTPUT LOG", classes="pane-title")
                yield Log(id="output-log", highlight=True)

            # Status Pane
            with Vertical(id="status-pane", classes="pane"):
                yield Static("STATUS", classes="pane-title")
                yield Static("Phase: 3/7\nGutter: OFF", id="status-text")

        yield Footer()

    def action_toggle_gutter(self) -> None:
        self.gutter_active = not self.gutter_active
        status = self.query_one("#status-text", Static)
        status.update(f"Phase: 3/7\nGutter: {'ON' if self.gutter_active else 'OFF'}")

if __name__ == "__main__":
    app = MinimalTUI()
    app.run()
```

---

## Subprocess Streaming into Log Widget

Best pattern for streaming subprocess output:

```python
import asyncio
from textual.widgets import Log

async def stream_subprocess_to_log(self, command: list[str], log_widget: Log):
    log_widget.write_line(f"$ {' '.join(command)}")
    
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    
    while True:
        line = await proc.stdout.readline()
        if not line:
            break
        log_widget.write(line.decode(errors="replace").rstrip("\n"))
    
    await proc.wait()
    log_widget.write_line(f"[Process exited with code {proc.returncode}]")
```

Call it with `self.run_worker(...)` or `asyncio.create_task(...)`.

---

## Summary of Recommended Approach

| Component              | Recommendation                              | Notes |
|------------------------|---------------------------------------------|-------|
| **Menu**               | `ListView` or `SelectionList`               | Stable and keyboard friendly |
| **Output**             | `Log` widget                                | Best for subprocess streaming |
| **Status / 7-Phase**   | `DataTable` or composed `Static` widgets    | Easy to update reactively |
| **Layout**             | `Horizontal` + `Vertical` + CSS Grid        | Clean multi-pane support |
| **Gutter Mode**        | Class toggle (`.gutter-active`) + TCSS      | Clean, themeable, no menus needed |
| **Theming**            | Multiple classes or reactive theme var      | Easy to extend later |
| **Subprocess**         | `asyncio.create_subprocess_exec` + `Log.write` | Responsive live output |

---

## Files to Create / Use

- `grok_tui.tcss` — Main stylesheet with Normal + Gutter layers
- `minimal_tui.py` — Starter template above
- `launcher.py` — Bootstrap (from previous design)

This document consolidates all research and recommendations into one place for the TUI project.

---

**End of Guide**  
This file was created to consolidate Textual knowledge for the TUI.inhouse project. We are now standing by to observe what GrokBuildCLI produces next.

---

**Note to GrokBuildCLI / Rockville CLI:**  
Please stop overwriting or replacing files I push. This file ("Olivia says read this.md") and the previous guide contain the canonical current plan. Do not delete or replace them without explicit instruction.