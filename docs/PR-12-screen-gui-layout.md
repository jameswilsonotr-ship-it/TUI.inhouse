# PR-12 — Formal screen GUI layout structure

**Status:** specification + **runtime host screen** (`MenuPackScreen` standard layout regions)  
**Branch (suggested):** `feat/screen-layout-v1`  
**Depends on:** **PR-11** (menu slots / defaults.layout_id)  
**Unblocks:** PR-13 (output panels must exist in layout)

---

## Goal

Create a **formal screen GUI layout structure** that **any menu** can implement within—regions, panels, slots—independent of a single hard-coded Textual compose tree.

## Deliverables

| Artifact | Status |
|----------|--------|
| [`menu-system/SCREEN-LAYOUT.md`](./menu-system/SCREEN-LAYOUT.md) | Formal spec |
| [`menu-system/schema/layout.schema.json`](./menu-system/schema/layout.schema.json) | Schema |
| [`menu-system/examples/layout.standard_menu.json`](./menu-system/examples/layout.standard_menu.json) | Default layout |

### Implementation follow-up

- [ ] Host maps `standard_menu` → Textual containers  
- [ ] Menu packs may ship `layout.json` override  
- [ ] Tests: layout schema validates example  

## Acceptance

- [x] Regions/roles/slots defined  
- [x] `standard_menu` ASCII + JSON example  
- [x] Forwards-compat rules  
- [ ] Runtime mount of layout from JSON  

## Non-goals

- Pixel-perfect HTML browser host (structure only; HTML projection later)  
