"""TUI chrome package — layouts, gallery, effects, bootstrap stage, menu intake.

Product UI pieces used by ``AWESOME_LAUNCHER_OF_TUIDOOM.py`` after venv bootstrap.

Modules
-------
effects
    Stdlib-only ANSI/ASCII effects (safe to import without Textual).
layouts
    Gallery ``LAYOUT_MODES``, panel specs, ``mount_layout``.
gallery
    Six-panel gallery + nested submenu + effects demo screens.
menu_intake
    Olivia voice menu locate / file picker / six-panel demo fallback.
bootstrap_stage
    Pre-TUI Stage A/B install theater (TTY-safe).
native_dialog
    OS file dialogs with graceful ``None`` fallback.

See Also
--------
docs/API.md, docs/ARCHITECTURE.md, docs/PR-08-docstrings.md
"""

__all__ = [
    "effects",
    "layouts",
    "gallery",
    "bootstrap_stage",
    "menu_intake",
    "native_dialog",
    "menu_model",
    "action_runner",
    "menu_screen",
]
