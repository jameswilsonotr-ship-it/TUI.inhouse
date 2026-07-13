# PR-05 — Six-panel carousel + nested menus

## Intent

A **gallery screen** (key `G` / button Gallery):

- **Six panels** in a ring navigation (←/→ or h/l cycle focus)
- Layout modes cycled with `L`:
  - 2 stacked + rest horizontal
  - 3 vertical columns
  - 2×3 grid
  - 1 main + sidebar stack
- **Nested submenu** on panel 1 (open with Enter / nested menu)
- Demo content: text banners + optional effects (PR-06)

## Navigation

| Key | Action |
|-----|--------|
| `G` | Open gallery from launcher |
| `escape` | Back to launcher home |
| `←` `→` / `h` `l` | Cycle active panel around the circle |
| `L` | Next layout mode |
| `Enter` | Open nested submenu on active panel |
| `e` | Toggle effects on active panel |

## Acceptance

- [ ] Six labeled panels visible  
- [ ] Circular focus works  
- [ ] At least 3 layout modes  
- [ ] Nested submenu screen pushes/pops  
