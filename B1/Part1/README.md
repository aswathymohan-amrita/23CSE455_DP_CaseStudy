# Part 1 — Baseline Pattern Discovery

**Course:** 23CSE455 Design Patterns  
**Team:** B1  
**Target Application:** Restaurant POS System (React + Node.js + TypeScript + Express + Socket.IO + Prisma)  

---

## Overview

Part 1 identifies and documents the baseline design patterns present in the original codebase prior to any feature evolution.

## Files & Artifacts

- `patterns.csv`: Canonical baseline pattern catalog with source file locations and participant symbols.
- `Pattern_count.csv`: Baseline pattern instance and type frequencies.
- `llm.csv`: LLM prompts used for pattern discovery and architectural inspection.
- `llm/verification.md`: Human verification evidence for baseline patterns.
- `pattern_architecture/`: Architecture diagrams and LaTeX source showing baseline component relationships.
- `code/`: Standalone baseline pattern demonstrations (`facade_demo.js`, `cor_demo.js`, `observer_demo.js`).

## Baseline Findings

1. **Façade Pattern (GoF Structural):**
   - `AuthService.login` (`apps/backend/src/services/auth.service.ts`): Orchestrates employee lookup, bcrypt password verification, and JWT creation.
   - `OrderService.createOrder` (`apps/backend/src/services/order.service.ts`): Coordinates order creation, table status update, and Socket.IO emission.
2. **Observer Pattern (GoF Behavioral / Framework Idiom):**
   - Socket.IO event system (`apps/backend/src/websocket.ts`): Server emits `order:new` events; connected kitchen display clients subscribe to rooms.
3. **Chain of Responsibility (GoF Behavioral / Candidate):**
   - Express authentication middleware (`apps/backend/src/middleware/auth.ts`): Sequentially validates JWT tokens and employee role permissions via `next()`.
