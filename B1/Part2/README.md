# Part 2 — Software Evolution and Refactoring

**Course:** 23CSE455 Design Patterns  
**Team:** B1  
**Project:** Restaurant Management System Evolution  

---

## Evolution Summary

Part 2 implements and verifies the three required software evolutions across the full-stack architecture:

1. **Evolution 1 (Online Ordering):**
   - Public menu (`GET /api/menu/public`) and online order creation (`POST /api/orders/online`).
   - Server-side pricing enforcement against Prisma database, 8% tax calculation, and delivery fee calculation.
   - React frontend integration in `OnlineOrdering.tsx`.
   - Pattern impact: Extends `OrderService` Facade, extends Observer Socket.IO dispatch.

2. **Evolution 2 (Kitchen Workflow):**
   - Partitioning of prep items across station-specific Socket.IO rooms (`cold`, `hot`, `bar`).
   - Deterministic course-to-station routing via `mapCourseToStation()`.
   - Real-time station tab switching and item deduplication in `KitchenDisplay.tsx`.
   - Pattern impact: Extends Observer event publication and subscription.

3. **Evolution 3 (Payment Strategy):**
   - GoF Strategy Pattern refactoring in `payment.service.ts`: `IPaymentStrategy`, `PaymentContext`, and 4 concrete strategies (`CashStrategy`, `CreditCardStrategy`, `MobilePayStrategy`, `GiftCardStrategy`).
   - Tender validation and change calculation for cash; simulated Stripe auth tokens; contactless NFC/QR capture; process-local gift card balance management.
   - Pattern impact: Introduces Strategy Pattern into the application codebase.

## Directory Structure

- `changes/`: Requirement specifications, code diffs, and test results for `Change1`, `Change2`, `Change3`, and `EVOLUTION_VALIDATION.md`.
- `code/`: Evolved source files (`order.service.ts`, `websocket.ts`, `payment.service.ts`, `OnlineOrdering.tsx`, `KitchenDisplay.tsx`, `PaymentModal.tsx`).
- `diagrams/`: UML diagrams in LaTeX TikZ format (`strategy_uml.tex`, `evolved_architecture.tex`).
- `tests/`: Automated test suite (`verify_evolutions.ts`) verifying 28/28 assertions (100% pass rate).
- `patterns_evolution.csv`: Change-by-change pattern audit ledger.
- `pattern_evalution.csv`: Pattern evolution tracking and student responsibility matrix.
- `Pattern_count.csv`: Statistical summary of evolved pattern instances.
- `llm.csv`: LLM prompt history for all evolution tasks.
