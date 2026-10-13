# Change 2 — Kitchen Station Workflow (Evolution 2)

> **Audit status (2026-10-11):** Status labels below are not evidence of a live Socket.IO/client integration test. Use `../../../data/patterns_evolution.csv`, `../../../AUDIT_REPORT.md`, and `../../../B1_Report.tex` for current status. The verification script tests course-to-station mapping only; station delivery and status persistence remain unverified.

## Requirement

Partition the kitchen display into three specialized stations so that each station only receives items relevant to their preparation area:

- **Cold Station** — Salads, starters, appetizers, soups
- **Hot Station** — Entrees, grills, mains, sides
- **Bar Station** — Beverages, cocktails, wines, desserts

Each item must be routed to exactly one station using a deterministic algorithm based on `CourseType` metadata.

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `kitchen:station:join` Socket.IO event subscribes client to a specific station room | ✅ Implemented |
| 2 | `mapCourseToStation()` maps `CourseType` enum and category name to `cold`, `hot`, or `bar` | ✅ Implemented |
| 3 | `emitKitchenStationItem()` broadcasts `kitchen:station:item:new` into the correct station room | ✅ Implemented |
| 4 | All 9 `CourseType` values route to the correct station | ✅ 9/9 assertions pass |
| 5 | Category-name fallback correctly routes cocktails/wine → bar; starters → cold | ✅ 2/2 assertions pass |
| 6 | `KitchenDisplay.tsx` re-joins station room when `stationFilter` changes | ✅ Implemented |
| 7 | `KitchenDisplay.tsx` deduplicates incoming items to prevent duplicate order tickets | ✅ Implemented |

## Changed Files

| File | Change Type | Description |
|------|------------|-------------|
| `apps/backend/src/websocket.ts` | **Modified** | Added `ioInstance`, `getIO()`, `mapCourseToStation()`, station join handler, `emitKitchenStationItem()` |
| `apps/backend/src/services/order.service.ts` | **Modified** | Station dispatch loop added after online order creation |
| `apps/frontend/src/components/KitchenDisplay.tsx` | **Modified** | Replaced `kitchen:join` with `kitchen:station:join`; added `kitchen:station:item:new` listener; deduplication |

## Design Pattern Impact

| Pattern | Instance | Impact | Notes |
|---------|----------|--------|-------|
| Observer | Kitchen events | **Extended** | Partitioned from one broadcast room into three station-specific rooms |
| State | Table lifecycle | **Newly introduced** | `StateDemo` models table state machine (Available → Occupied → Billed) |
| Decorator | Menu item modifiers | **Newly introduced** | `DecoratorDemo` models dynamic price/prep-note wrapping |
| Facade | `OrderService` | **Preserved** | No interface change; station dispatch is an internal detail |

## Evidence

- Implementation source: `Part2/code/apps/backend/src/websocket.ts` (lines 10–166)
- Evolution demo: `Part2/changes/Change2/evolution2_kitchen_workflow.js`
- Test verification: `apps/backend/src/scripts/verify_evolutions.ts` → Evolution 2 section (9/9 station routing tests pass)
