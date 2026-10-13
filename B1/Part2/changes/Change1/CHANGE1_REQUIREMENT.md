# Change 1 — Online Ordering (Evolution 1)

> **Audit status (2026-10-11):** The acceptance labels and test summary below are historical claims, not verified end-to-end results. Use `../../../data/patterns_evolution.csv`, `../../../AUDIT_REPORT.md`, and `../../../B1_Report.tex` for current status. The backend verification script does not call the HTTP endpoint or database, and the UI has a local-only fallback.

## Requirement

Allow customers to place orders directly from a public web portal without requiring a restaurant staff login. The system must:
1. Accept itemized orders from external customers via a REST endpoint.
2. Apply server-side validated pricing — never trusting client-supplied prices.
3. Persist the order in the database linked to a virtual "Online Table".
4. Automatically route each ordered item to the correct kitchen station (Cold / Hot / Bar).

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `POST /api/orders/online` is publicly accessible (no JWT required) | ✅ Implemented |
| 2 | `GET /api/menu/public` returns available menu items without authentication | ✅ Implemented |
| 3 | Prices are looked up server-side from `MenuItem` table — client-supplied prices are ignored | ✅ Implemented |
| 4 | Missing or invalid `menuItemId` returns HTTP 400 with a descriptive error | ✅ Implemented |
| 5 | Successful order returns HTTP 201 with the persisted order object | ✅ Implemented |
| 6 | Items are routed to kitchen stations via WebSocket after creation | ✅ Implemented |
| 7 | Frontend `OnlineOrdering.tsx` calls the real endpoint, falls back gracefully if server unavailable | ✅ Implemented |

## Changed Files

| File | Change Type | Description |
|------|------------|-------------|
| `apps/backend/src/services/order.service.ts` | **Modified** | Added `createOnlineOrder()` with Prisma lookup, server-side pricing, and station dispatch |
| `apps/backend/src/routes/order.routes.ts` | **Modified** | Exposed public `POST /online` route bypassing auth middleware |
| `apps/backend/src/index.ts` | **Modified** | Mounted public `/api/orders/online` and `/api/menu/public` routes before auth middleware |
| `apps/frontend/src/components/OnlineOrdering.tsx` | **Modified** | Replaced local state simulation with async `fetch()` call to backend API |

## Design Pattern Impact

| Pattern | Instance | Impact | Notes |
|---------|----------|--------|-------|
| Facade | `OrderService` | **Extended** | `createOnlineOrder()` added as a new public operation on the existing facade |
| Chain of Responsibility | Auth middleware | **Preserved** | Online endpoint bypasses the chain intentionally (public route) |
| Observer | Socket.IO KDS | **Extended** | Station dispatch now triggered on every online order item |
| Adapter | Delivery normalizer | **Newly introduced** | `AdapterDemo` models the pattern for normalizing 3rd-party payloads |
| Factory Method | Ticket generator | **Newly introduced** | `FactoryDemo` models ticket generation for Delivery vs DineIn |

## Evidence

- Implementation source: `Part2/code/apps/backend/src/services/order.service.ts` (lines 326–467)
- Evolution demo: `Part2/changes/Change1/evolution1_online_ordering.js`
- Test verification: `apps/backend/src/scripts/verify_evolutions.ts` → Evolution 1 section (3/3 tests passing)
