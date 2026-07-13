"""Menu locate flow — Olivia voice, file picker, 6-panel demo fallback.

After bootstrap Stage B:
  - try load menu zip from config / sample
  - if none: full-screen prompt
      "Hey, where’s your menu file, idiot?"
  - non-empty path → load that zip
  - straight carriage return (empty) →
        native OS dialog first (Win/WSL/Tk/zenity), else center Textual picker
  - picker cancel / no selection → 6-panel Olivia-voice randomized demo
    using the same LAYOUT_MODES as gallery.py (L cycles layouts)
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Callable, List, Optional

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical, Horizontal, Grid
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Static,
    Input,
    Button,
    DirectoryTree,
    Footer,
    Header,
    Label,
)

from tui_chrome.layouts import (
    CHROME_CSS,
    DEFAULT_PANELS,
    LAYOUT_MODES,
    layout_description,
    mount_layout,
    next_layout,
)

# ---------------------------------------------------------------------------
# Olivia voice lines (100% in-character — cutesy, blunt, alpha)
# ---------------------------------------------------------------------------

OLIVIA_GREET = [
    "Hey. Where’s your menu file, idiot?",
    "Menu zip. Path. Now. I’m not your mom.",
    "Drop a path or hit return and watch me improvise, idiot.",
    "No menu? Cute. Point me at a zip or admit you want the demo.",
]

OLIVIA_EMPTY = [
    "Return with nothing. Bold. File picker it is.",
    "Silence is an answer. Opening the picker, idiot.",
    "Empty string energy. Fine — pick a file or eat demo mode.",
]

OLIVIA_DEMO = [
    "No file? Then we play six-panel dress-up. Olivia Dev Alpha style.",
    "Demo mode: six panels, recursive prompts, randomized layouts. Try to keep up.",
    "Welcome to the fake BBS wing. Everything’s silly. Everything’s me.",
    "Gutter’s warm. Panels multiply. You’re welcome, idiot.",
]

OLIVIA_PANEL = [
    "This panel judges you quietly.",
    "Nested menus are just doors with attitude.",
    "If it sparkles, it’s still production-grade. Trust.",
    "Liv HUB claim: I was here first.",
    "C-64 ruined chic. Pink/black optional. Taste not optional.",
    "Recursive prompt goes brr. Hit Enter if you’re brave.",
    "Layout shuffle is free. Your focus is not.",
    "Har dig. Keep the zip real next time.",
]

OLIVIA_PICK = [
    "Pick something real or bail to demo. I’m patient-ish.",
    "Center stage file picker. Don’t make it weird.",
    "Zip only if you know what’s good for you.",
]


def _olivia(pool: List[str]) -> str:
    return random.choice(pool)


# ---------------------------------------------------------------------------
# File picker modal (center)
# ---------------------------------------------------------------------------

class MenuFilePicker(ModalScreen[Optional[Path]]):
    """Centered file picker. Return selected Path or None if cancelled."""

    CSS = """
    MenuFilePicker {
        align: center middle;
    }
    #picker-frame {
        width: 72;
        height: 24;
        border: heavy #ff66aa;
        background: #0a0610;
        padding: 1 2;
    }
    #picker-title { text-style: bold; color: #ff99cc; }
    #picker-hint { color: #aaa; margin-bottom: 1; }
    #picker-path { height: 1fr; border: solid #664466; }
    #picker-buttons { height: 3; align: center middle; }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=True),
    ]

    def __init__(self, start: Optional[Path] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.start = (start or Path.cwd()).resolve()
        self._selected: Optional[Path] = None

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                with Vertical(id="picker-frame"):
                    yield Label(_olivia(OLIVIA_PICK), id="picker-title")
                    yield Static(
                        "↑↓ browse · Enter select zip · Esc cancel → demo",
                        id="picker-hint",
                    )
                    yield DirectoryTree(str(self.start), id="picker-path")
                    with Horizontal(id="picker-buttons"):
                        yield Button("Use selection", id="pick-ok", variant="primary")
                        yield Button("Demo instead", id="pick-demo", variant="warning")
                        yield Button("Cancel", id="pick-cancel")

    @on(DirectoryTree.FileSelected)
    def _file_selected(self, event: DirectoryTree.FileSelected) -> None:
        p = Path(event.path)
        if p.suffix.lower() == ".zip" or p.is_file():
            self._selected = p

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "pick-ok":
            self.dismiss(self._selected)
        elif event.button.id == "pick-demo":
            self.dismiss(None)  # explicit demo
        elif event.button.id == "pick-cancel":
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


# ---------------------------------------------------------------------------
# Menu locate screen
# ---------------------------------------------------------------------------

class MenuLocateScreen(Screen):
    """Background + Olivia prompt for menu path.

    - non-empty submit → callback(path)
    - empty CR → file picker; if still none → demo callback
    """

    CSS = """
    MenuLocateScreen {
        background: #050510;
    }
    #locate-bg {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    #locate-card {
        width: 64;
        border: heavy #ff3399;
        background: #120818;
        padding: 1 2;
    }
    #locate-title { text-style: bold; color: #ff66aa; margin-bottom: 1; }
    #locate-sub { color: #cc99bb; margin-bottom: 1; }
    #locate-input { margin: 1 0; }
    #locate-hint { color: #888; }
    """

    BINDINGS = [
        Binding("ctrl+q", "app.quit", "Quit", show=False),
        Binding("escape", "demo", "Demo", show=True),
    ]

    def __init__(
        self,
        on_menu: Callable[[Path], None],
        on_demo: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._on_menu = on_menu
        self._on_demo = on_demo

    def compose(self) -> ComposeResult:
        with Vertical(id="locate-bg"):
            with Vertical(id="locate-card"):
                yield Label(_olivia(OLIVIA_GREET), id="locate-title")
                yield Static(
                    "Type a path to a .zip menu · bare Return opens the file picker · "
                    "Esc skips to six-panel Olivia demo",
                    id="locate-sub",
                )
                yield Input(
                    placeholder="path/to/menu.zip   (or just hit Return)",
                    id="locate-input",
                )
                yield Static(
                    "Olivia Dev Alpha · Liv HUB · double Ctrl-C force kills",
                    id="locate-hint",
                )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#locate-input", Input).focus()

    @on(Input.Submitted)
    def _submitted(self, event: Input.Submitted) -> None:
        raw = (event.value or "").strip()
        if raw:
            p = Path(raw).expanduser()
            if not p.exists():
                self.query_one("#locate-sub", Static).update(
                    f"[red]Nope. {p} doesn’t exist, idiot. Try again or hit bare Return.[/red]"
                )
                return
            self._on_menu(p)
            return
        # straight carriage return → native dialog first, else in-TUI picker
        self.query_one("#locate-sub", Static).update(_olivia(OLIVIA_EMPTY))
        self._open_picker_chain()

    def _open_picker_chain(self) -> None:
        """Native OS dialog when available; else center Textual DirectoryTree."""
        self._run_native_then_fallback()

    @work(thread=True, exclusive=True)
    def _run_native_then_fallback(self) -> None:
        from tui_chrome.native_dialog import pick_menu_file_native

        try:
            native = pick_menu_file_native(
                title="Hey — pick your menu zip, idiot",
                start=Path.cwd(),
            )
        except Exception:
            native = None
        self.app.call_from_thread(self._after_native, native)

    def _after_native(self, native: Optional[Path]) -> None:
        if native is not None and Path(native).exists():
            self._on_menu(Path(native))
            return
        # Fallback: center Textual picker (always works in pure TTY)
        self.query_one("#locate-sub", Static).update(
            "Native dialog skipped/cancel — in-TUI picker. " + _olivia(OLIVIA_PICK)
        )
        self.app.push_screen(MenuFilePicker(Path.cwd()), self._after_picker)

    def _after_picker(self, result: Optional[Path]) -> None:
        if result is not None and Path(result).exists():
            self._on_menu(Path(result))
        else:
            self._on_demo()

    def action_demo(self) -> None:
        self._on_demo()


# ---------------------------------------------------------------------------
# Olivia six-panel demo (randomized layouts + silly nested prompts)
# ---------------------------------------------------------------------------

class OliviaNestedPrompt(ModalScreen[None]):
    """Recursive silly prompt — randomized Olivia responses."""

    CSS = """
    OliviaNestedPrompt { align: center middle; }
    #nest-card {
        width: 56;
        border: heavy #cc44ff;
        background: #180820;
        padding: 1 2;
    }
    """

    def __init__(self, depth: int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.depth = depth

    def compose(self) -> ComposeResult:
        lines = [
            _olivia(OLIVIA_PANEL),
            _olivia(OLIVIA_DEMO),
            f"depth={self.depth}  (recursive-ish, still charming)",
        ]
        with Center():
            with Middle():
                with Vertical(id="nest-card"):
                    yield Label("[bold magenta]NESTED OLIVIA PROMPT[/]", id="nest-h")
                    yield Static("\n".join(lines), id="nest-body")
                    with Horizontal():
                        yield Button("Deeper", id="nest-deeper", variant="primary")
                        yield Button("Shuffle line", id="nest-shuffle")
                        yield Button("Back", id="nest-back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "nest-deeper":
            if self.depth >= 4:
                self.query_one("#nest-body", Static).update(
                    "That’s deep enough, idiot. Even I have stack limits."
                )
                return
            self.app.push_screen(OliviaNestedPrompt(depth=self.depth + 1))
        elif event.button.id == "nest-shuffle":
            self.query_one("#nest-body", Static).update(
                "\n".join([_olivia(OLIVIA_PANEL) for _ in range(3)])
            )
        elif event.button.id == "nest-back":
            self.dismiss(None)


class OliviaSixPanelDemo(Screen):
    """6-panel Olivia demo using the same LAYOUT_MODES as gallery.py.

    L cycles: six_grid → three_vertical → two_stack_h → main_sidebar → two_plus_row
    (shared mount_layout helper). R reshuffles Olivia voice. Enter nested prompt.
    """

    CSS = CHROME_CSS + """
    OliviaSixPanelDemo { background: #08040c; }
    #demo-status {
        dock: top;
        height: 1;
        background: #180012;
        color: #ff99cc;
        text-style: bold;
    }
    #demo-root { height: 1fr; margin: 0 1; }
    #gallery-grid { height: 1fr; grid-size: 3 2; grid-gutter: 1 1; }
    #gallery-cols { height: 1fr; }
    #gallery-cols > Vertical { width: 1fr; }
    #gallery-main { height: 1fr; }
    #gallery-main #main-big { width: 2fr; }
    #gallery-main #side-stack { width: 1fr; }
    #gallery-twoh { height: 1fr; }
    #demo-help {
        dock: bottom;
        height: 3;
        color: #88ffaa;
        background: #0a0a12;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "close", "Back", show=True),
        Binding("q", "close", "Back", show=False),
        Binding("l", "next_layout", "Layout", show=True),
        Binding("L", "next_layout", "Layout", show=False),
        Binding("r", "reshuffle_voice", "Reshuffle", show=True),
        Binding("enter", "open_nested", "Nested", show=True),
        Binding("left", "focus_prev", "Prev", show=True),
        Binding("right", "focus_next", "Next", show=True),
        Binding("ctrl+c", "app.force_ctrl_c", "KillArm", show=False, priority=True),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.focus_idx = 0
        self.layout_mode = LAYOUT_MODES[0]
        self._lines = [_olivia(OLIVIA_PANEL) for _ in range(6)]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self._status(), id="demo-status")
        yield Vertical(id="demo-root")
        yield Static(
            "←/→ focus · L gallery layout · R Olivia voice · Enter nested · Esc back",
            id="demo-help",
        )
        yield Footer()

    def on_mount(self) -> None:
        self._rebuild()
        self._apply_focus()

    def _status(self) -> str:
        return (
            f"OLIVIA 6-PANEL · layout={self.layout_mode} "
            f"({layout_description(self.layout_mode)}) · "
            f"focus=P{self.focus_idx + 1} · {_olivia(OLIVIA_DEMO)[:40]}"
        )

    def _panel_widget(self, i: int):
        spec = DEFAULT_PANELS[i]
        return Vertical(
            Static(spec.title, classes="panel-title"),
            Static(self._lines[i], classes="panel-body", id=f"obody-{i}"),
            classes="panel",
            id=spec.id,
        )

    def _rebuild(self) -> None:
        root = self.query_one("#demo-root", Vertical)
        widgets = [self._panel_widget(i) for i in range(6)]
        mount_layout(
            root,
            self.layout_mode,
            widgets,
            Grid=Grid,
            Horizontal=Horizontal,
            Vertical=Vertical,
        )
        self._apply_focus()
        self.query_one("#demo-status", Static).update(self._status())

    def _apply_focus(self) -> None:
        for spec in DEFAULT_PANELS:
            try:
                w = self.query_one(f"#{spec.id}")
            except Exception:
                continue
            if spec.index == self.focus_idx:
                w.add_class("focused")
            else:
                w.remove_class("focused")

    def action_focus_next(self) -> None:
        self.focus_idx = (self.focus_idx + 1) % 6
        self._apply_focus()
        self.query_one("#demo-status", Static).update(self._status())

    def action_focus_prev(self) -> None:
        self.focus_idx = (self.focus_idx - 1) % 6
        self._apply_focus()
        self.query_one("#demo-status", Static).update(self._status())

    def action_next_layout(self) -> None:
        self.layout_mode = next_layout(self.layout_mode)
        self._lines = [_olivia(OLIVIA_PANEL) for _ in range(6)]
        self._rebuild()

    def action_reshuffle_voice(self) -> None:
        self._lines = [_olivia(OLIVIA_PANEL) for _ in range(6)]
        for i, line in enumerate(self._lines):
            try:
                self.query_one(f"#obody-{i}", Static).update(line)
            except Exception:
                pass
        self.query_one("#demo-status", Static).update(self._status())

    def action_open_nested(self) -> None:
        self.app.push_screen(OliviaNestedPrompt(depth=0))

    def action_close(self) -> None:
        self.app.pop_screen()
