# LLM Verification & Human Auditing Report

## Overview
In compliance with Section 5 of the 23CSE455 Case Study guidelines, all generative AI interactions were recorded, constrained to publicly accessible models (Gemini 2.5 Flash / Claude 3.5 Sonnet / ChatGPT), and strictly verified by team members against actual source code and compiler test results.

---

## Part 1: Pattern Discovery Audits

### Student 1 — Façade Pattern
- **Prompt:** `Analyze apps/backend/src/services/order.service.ts and auth.service.ts in our Restaurant POS system. Identify how they act as a GoF Façade over Prisma ORM, bcrypt, table locking, and Socket.IO...`
- **AI Claim:** Claimed `OrderService` and `AuthService` are Façades hiding multiple subsystem interactions.
- **Human Evaluation:** **CONFIRMED & ACCEPTED.** Both services coordinate database writes, business logic, state machines, and real-time broadcasts behind simplified public methods.

### Student 1 — Chain of Responsibility
- **Prompt:** `Examine the Express middleware pipeline in apps/backend/src/middleware/auth.ts. Show how the request passes sequentially from TokenValidator to RoleChecker to the final route handler...`
- **AI Claim:** Claimed Express middleware chain is a GoF Chain of Responsibility.
- **Human Evaluation:** **CONFIRMED & ACCEPTED.** Follows canonical GoF behavioral pattern where each handler either handles/rejects the request or delegates downstream via `next()`.

---

## Part 2 & Part 3: Evolution and Cross-Language Audits

| Student | Assigned Pattern | AI Output Status | Verification Action Taken |
| :--- | :--- | :--- | :--- |
| **Student 2** | **Strategy** (Multi-Payment) | Correct | Verified Cash change calculation and Stripe/QR strategies execute polymorphically across all 4 languages. |
| **Student 2** | **Observer** (KDS Stations) | Correct | Verified kitchen tickets route to Cold, Hot, and Waiter displays without cross-station pollution. |
| **Student 3** | **Adapter** (Online Delivery) | Correct | Verified DoorDash and UberEats payloads convert into canonical `POSOrder` format. |
| **Student 3** | **State** (Table Lifecycle) | Correct | Verified illegal state transitions (e.g. paying before ordering) are properly rejected by the state machine. |
| **Student 4** | **Factory Method** (Tickets) | Correct | Verified distinct DineIn, Takeout, and Delivery tickets are cleanly produced. |
| **Student 4** | **Decorator** (Item Modifiers)| Correct | Verified compounding modifier costs (Cheese + Bacon + GF) compute without float precision errors. |
| **Student 5** | **Command** (Cart Undo Stack)| Correct | Verified invoker history stack correctly pops and inverts actions upon undo. |
| **Student 5** | **Template Method** (Pipeline)| Correct | Verified invariant 4-step algorithm executes identically with customized Dine-In and Delivery hooks. |

All 40 programs were compiled and executed locally on Windows (Java 11/17, CPython 3.10+, Node.js 22, g++ C++17), and their raw stdout logs are saved in `data/test_result/`.

## Audit correction (2026-10-11)

The historical model/date and verification claims in this file are not independently supported by preserved conversation links or execution records. Treat prompt text as a draft only. Fresh program execution evidence is under `../Part3/evidence/reproduced_2026-10-11/`; C++ was not run. See `../AUDIT_REPORT.md` and the canonical `../data/llm.csv` for current evidence status.
