"""PR-05 — Six-panel gallery + nested submenu + layout modes.
PR-06 — effects integration on panel bodies.
"""
from __future__ import annotations

from typing import Optional

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, Button, Label
from textual.timer import Timer

from tui_chrome.layouts import (
    CHROME_CSS,
    DEFAULT_PANELS,
    LAYOUT_MODES,
    circle_index,
    layout_description,
    mount_layout,
    next_layout,
)
from tui_chrome import effects


class NestedSubmenuScreen(Screen):
    """Nested submenu under a gallery panel."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
        Binding("q", "app.pop_screen", "Back", show=False),
    ]

    def __init__(self, parent_panel: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.parent_panel = parent_panel

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"[bold magenta]NESTED SUBMENU[/] ← from {self.parent_panel}", id="nest-title")
        yield Static(
            effects.ascii_box(
                "SUBMENU",
                "1) Show banner crawl\n"
                "2) Toggle glitter\n"
                "3) Fake 'open zip'\n"
                "4) Back (Esc)\n\n"
                "BBS energy: nested like a door inside a door.",
                46,
            ),
            id="nest-body",
        )
        with Horizontal():
            yield Button("Banner", id="nest-banner", variant="primary")
            yield Button("Glitter", id="nest-glitter")
            yield Button("Back", id="nest-back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        body = self.query_one("#nest-body", Static)
        if event.button.id == "nest-banner":
            body.update(effects.banner_crawl("*** NESTED CRAWL *** GUTTER ***", 44, 3))
        elif event.button.id == "nest-glitter":
            body.update(effects.glitter_line(44, 7) + "\n" + effects.sparkle_field(4, 44, 2))
        elif event.button.id == "nest-back":
            self.app.pop_screen()


class GalleryScreen(Screen):
    """Six panels, circular focus, layout modes, effects tick."""

    CSS = CHROME_CSS + """
    #gallery-grid { height: 1fr; grid-size: 3 2; grid-gutter: 1 1; }
    #gallery-cols { height: 1fr; }
    #gallery-cols > Vertical { width: 1fr; }
    #gallery-main { height: 1fr; }
    #gallery-main #main-big { width: 2fr; }
    #gallery-main #side-stack { width: 1fr; }
    #gallery-twoh { height: 1fr; }
    """

    BINDINGS = [
        Binding("escape", "close_gallery", "Back", show=True),
        Binding("q", "close_gallery", "Back", show=False),
        Binding("left", "focus_prev", "Prev", show=True),
        Binding("right", "focus_next", "Next", show=True),
        Binding("h", "focus_prev", "Prev", show=False),
        Binding("l", "focus_next", "Next", show=False),
        Binding("L", "next_layout", "Layout", show=True),
        Binding("enter", "open_nested", "Submenu", show=True),
        Binding("e", "toggle_effects", "FX", show=True),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.focus_idx = 0
        self.layout_mode = LAYOUT_MODES[0]
        self.effects_on = True
        self._tick = 0
        self._timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self._status_text(), id="gallery-status")
        # Default shell: six_grid container we rebuild on layout change
        yield Vertical(id="gallery-root")
        yield Static(
            "←/→ cycle panels · L layout · Enter nested · e effects · Esc back",
            id="gallery-help",
        )
        yield Footer()

    def on_mount(self) -> None:
        self._rebuild_layout()
        self._apply_focus()
        self._timer = self.set_interval(0.15, self._on_tick)

    def on_unmount(self) -> None:
        if self._timer:
            self._timer.stop()

    def _status_text(self) -> str:
        return (
            f"GALLERY · layout={self.layout_mode} ({layout_description(self.layout_mode)}) · "
            f"focus=P{self.focus_idx + 1} · FX={'ON' if self.effects_on else 'OFF'}"
        )

    def _panel_widget(self, spec) -> Vertical:
        body_text = effects.panel_effect_text(spec.index, 0, "sparkle") if self.effects_on else f"Panel {spec.index + 1}\n(static)"
        return Vertical(
            Static(spec.title, classes="panel-title"),
            Static(body_text, classes="panel-body", id=f"body-{spec.id}"),
            classes="panel",
            id=spec.id,
        )

    def _rebuild_layout(self) -> None:
        root = self.query_one("#gallery-root", Vertical)
        widgets = [self._panel_widget(spec) for spec in DEFAULT_PANELS]
        mount_layout(
            root,
            self.layout_mode,
            widgets,
            Grid=Grid,
            Horizontal=Horizontal,
            Vertical=Vertical,
        )
        self._apply_focus()
        self.query_one("#gallery-status", Static).update(self._status_text())

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

    def _on_tick(self) -> None:
        if not self.effects_on:
            return
        self._tick += 1
        modes = ["sparkle", "glitter", "crawl", "strobe", "sparkle", "glitter"]
        for spec in DEFAULT_PANELS:
            try:
                body = self.query_one(f"#body-{spec.id}", Static)
            except Exception:
                continue
            mode = modes[spec.index % len(modes)]
            # focused panel gets strobe emphasis
            if spec.index == self.focus_idx:
                mode = "strobe" if self._tick % 2 == 0 else mode
            body.update(effects.panel_effect_text(spec.index, self._tick, mode))

    def action_focus_next(self) -> None:
        self.focus_idx = circle_index(self.focus_idx, 1)
        self._apply_focus()
        self.query_one("#gallery-status", Static).update(self._status_text())

    def action_focus_prev(self) -> None:
        self.focus_idx = circle_index(self.focus_idx, -1)
        self._apply_focus()
        self.query_one("#gallery-status", Static).update(self._status_text())

    def action_next_layout(self) -> None:
        self.layout_mode = next_layout(self.layout_mode)
        self._rebuild_layout()

    def action_open_nested(self) -> None:
        spec = DEFAULT_PANELS[self.focus_idx]
        self.app.push_screen(NestedSubmenuScreen(spec.title))

    def action_toggle_effects(self) -> None:
        self.effects_on = not self.effects_on
        self.query_one("#gallery-status", Static).update(self._status_text())
        if not self.effects_on:
            for spec in DEFAULT_PANELS:
                try:
                    self.query_one(f"#body-{spec.id}", Static).update(
                        f"{spec.title}\n\nFX off · Enter=submenu · L=layout"
                    )
                except Exception:
                    pass

    def action_close_gallery(self) -> None:
        self.app.pop_screen()


class EffectsDemoScreen(Screen):
    """PR-06 standalone effects parade."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.pop_screen", "Back", show=False),
    ]

    CSS = """
    #fx-box { height: 1fr; border: double #ff44aa; padding: 1; background: #100810; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("ANSI / ASCII EFFECTS (PR-06) — Esc back", id="fx-title")
        yield Static("loading…", id="fx-box")
        yield Footer()

    def on_mount(self) -> None:
        self._tick = 0
        self.set_interval(0.12, self._tick_fx)

    def _tick_fx(self) -> None:
        self._tick += 1
        body = "\n".join(
            [
                effects.banner_crawl("*** GUTTER SPARKLE PARADE ***", 48, self._tick),
                effects.glitter_line(48, self._tick),
                effects.sparkle_field(6, 48, self._tick),
                effects.glitter_line(48, self._tick + 5),
                effects.strip_ansi(effects.gutter_banner(self._tick)),
            ]
        )
        self.query_one("#fx-box", Static).update(effects.ascii_box("EFFECTS", body, 50))
