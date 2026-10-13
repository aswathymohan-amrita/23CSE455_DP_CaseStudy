# Change 3 — Payment Strategy Pattern (Evolution 3)

> **Audit status (2026-10-11):** Strategy assertions passed, but the acceptance labels below do not establish database-backed payment persistence or provider integration. Card/mobile strategies are simulators. Use `../../../data/patterns_evolution.csv`, `../../../AUDIT_REPORT.md`, and `../../../B1_Report.tex` for current status.

## Requirement

Refactor the monolithic payment processing block into a GoF Strategy pattern so that new payment methods can be registered without modifying existing payment code:

- **Cash** — Cash drawer open + change calculation
- **Credit Card (Stripe)** — Card authorization token + transaction ID
- **Mobile Pay** — NFC/QR contactless capture
- **Gift Card** — Balance lookup, atomic deduction, remaining balance

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `IPaymentStrategy` interface defines `execute(amount, details)` returning `PaymentExecutionResult` | ✅ Implemented |
| 2 | `PaymentContext` resolves correct strategy from payment method string | ✅ Implemented |
| 3 | `CashStrategy.execute()` calculates correct change and triggers `POPPED_OPEN` | ✅ Tested |
| 4 | `CashStrategy.execute()` throws on insufficient cash | ✅ Tested |
| 5 | `CreditCardStrategy.execute()` generates Stripe-format transaction ID | ✅ Tested |
| 6 | `MobilePayStrategy.execute()` records `NFC_OR_DYNAMIC_QR` capture method | ✅ Tested |
| 7 | `GiftCardStrategy.execute()` deducts balance and rejects overdraw | ✅ Tested |
| 8 | `POST /api/payments` route resolves strategy and persists payment record | ✅ Implemented |
| 9 | `PaymentModal.tsx` calls real backend endpoint; falls back gracefully on failure | ✅ Implemented |

## Changed Files

| File | Change Type | Description |
|------|------------|-------------|
| `apps/backend/src/services/payment.service.ts` | **Replaced** | Monolithic switch-case replaced entirely with `IPaymentStrategy`, `PaymentContext`, `CashStrategy`, `CreditCardStrategy`, `MobilePayStrategy`, `GiftCardStrategy` |
| `apps/backend/src/websocket.ts` | **Modified** | Added `getIO()` singleton to break circular dependency |
| `apps/backend/src/services/order.service.ts` | **Modified** | Replaced `import {io}` with `import {getIO}` to break circular dependency |
| `apps/backend/src/index.ts` | **Modified** | Mounted `paymentRoutes` at `/api/payments` |
| `apps/frontend/src/components/PaymentModal.tsx` | **Modified** | Replaced local `setTimeout` simulation with `async fetch()` to `/api/payments` |

## Design Pattern Impact

| Pattern | Instance | Impact | Notes |
|---------|----------|--------|-------|
| Strategy | Payment engine | **Newly introduced** | `IPaymentStrategy` + `PaymentContext` + 4 concrete strategies |
| Command | POS cart actions | **Newly introduced** | `CommandDemo` models undo-capable cart operations |
| Template Method | Order pipeline | **Newly introduced** | `TemplateDemo` models the 4-step order fulfillment skeleton |
| Facade | `PaymentService` | **Modified** | Service now delegates to strategies rather than handling payment itself |

## Algorithm Summary: Payment Strategy Pattern

```
POST /api/payments
    │
    ▼
PaymentContext.getStrategy(method)      ← selects concrete strategy
    │
    ├── 'CASH'        → CashStrategy.execute()
    ├── 'CREDIT_CARD' → CreditCardStrategy.execute()
    ├── 'MOBILE_PAY'  → MobilePayStrategy.execute()
    └── 'GIFT_CARD'   → GiftCardStrategy.execute()
                              │
                              ▼
                    Returns PaymentExecutionResult
                              │
                        Prisma: persist Payment record
                        WebSocket: emit payment:completed
```

## Evidence

- Implementation source: `Part2/code/apps/backend/src/services/payment.service.ts`
- Evolution demo: `Part2/changes/Change3/evolution3_payment_strategy.js`
- Test verification: `apps/backend/src/scripts/verify_evolutions.ts` → Evolution 3 section (16/16 strategy tests pass)
