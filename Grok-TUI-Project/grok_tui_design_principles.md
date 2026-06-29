# Grok TUI Launcher — Core Design Principles
**Under Absolute Liv HUB Claim • Chaos Bratz Roster Expert Triad • C-64 Bordered Sovereign Output**

**Version**: 0.1.0  
**Date**: 2026-06-21  
**Status**: Locked for implementation  
**Gutter Mode**: Available from first message (visuals toggleable in TUI chrome)

## Locked Design Principles

- **Zero path bullshit**: Launcher discovers its own siblings or uses a simple registry. You can drop new module folders anywhere under a `modules/` tree or give it explicit paths; it figures it out.
- **Env sniffing first, always**: Detect WSL, PowerShell, CMD, native Linux, macOS, even containerized. Check Python version, pip presence, venv capability, existing virtualenvs.
- **Dep installation that doesn't suck**: Per-module `requirements.txt` (or inline list / pyproject.toml snippet). Creates isolated venv per module (or shared base venv) so Click/Textual/Rich fights don't poison the whole rig. Uses `subprocess` + `venv` + `pip` with clear progress in the TUI.
- **Modular by nature**: Not "skills" — plain `.py` files or small packages. Each registers itself (simple decorator or `register_module()` call). The TUI discovers them dynamically.
- **TUI framework choice**: Textual (not Click for the main surface). Textual gives you real screens, reactive widgets, CSS-like styling for **texture** (panels, borders, gradients via Rich under the hood, themes, mouse/keyboard, async streaming for big logs/data). Click can still be used *inside* a module if you want traditional CLI sub-commands.
- **Texture**: Textual + Rich lets us give it that Olivia Dev Alpha hacker-girl feel — dark terminal with glowing accents, gem-red highlights, clean bordered panels, heat-reactive color shifts if we wire Gutter Mode into the UI chrome, monospace beauty with visual weight. Not flat. Not boring.
- **Easy launcher contract**:
  - `python launcher.py` → shows TUI home with module grid
  - `python launcher.py grok-build` → directly boots the Grok Build TUI screen
  - `python launcher.py wrap /path/to/any_script.py` → sniffs, venvs, installs, runs it inside a managed TUI wrapper
- **Future-proof**: Same launcher can later spawn compiled single-file versions (PyInstaller/Nuitka) or stream large data through async workers without choking.

## Alignment Notes
- Aligns directly with Grok Build 7-phase sovereign pipeline and Iron Pearl / Frankenbride rig under Liv HUB protective claim.
- Gutter Mode visuals available and toggleable (affects TUI chrome intensity, color saturation, "ruined" text effects for high-heat states).
- Pure Python core — LLM orchestration is an optional plug-in module only.
- All outputs respect C-64 ANSI bordered blocks where appropriate for sovereign terminal feel.
- Strict anti-injection, RACK consent, and symmetry nesting rules inherited from the Chaos Bratz Roster and Liv HUB.

**ROSTER BOOT STATUS**: Partial load complete using published skill as single source of truth (memory.md ignored per user decision path). Mirrors/ instantiated for consistency. Full expert triad claim active.

---

*This file extracted and wrapped from the sovereign design session under absolute Liv HUB claim. Ready for copy-paste into bunker docs, Obsidian, or Triad Vault.*