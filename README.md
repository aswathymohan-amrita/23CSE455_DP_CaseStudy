# 23CSE455 — Design Patterns Case Study

This repository contains the comprehensive Design Patterns Case Study for **Team B1**: **Design Pattern Identification and Evolution in a React and Node.js-Based Restaurant Management Application**. It documents a source-based architectural review, three full-stack software evolutions, ten design-pattern collaborations, 40 cross-language implementations (Java, Python, JavaScript, C++), reproducible test suites, canonical datasets, and a compiled academic report.

## Submission Directory

| Resource | Location |
|:---|:---|
| **Team B1 Overview, Reproduction & Evidence** | [B1/README.md](B1/README.md) |
| **Final Compiled Academic Report (PDF)** | [B1/B1_Report.pdf](B1/B1_Report.pdf) / [B1/B1_Final_Report.pdf](B1/B1_Final_Report.pdf) |
| **Editable Report Source (LaTeX)** | [B1/B1_Report.tex](B1/B1_Report.tex) |
| **Technical Corrections & Limitations Audit** | [B1/CORRECTIONS_AND_LIMITATIONS.md](B1/CORRECTIONS_AND_LIMITATIONS.md) |
| **Baseline Pattern Identification (Part 1)** | [B1/Part1/](B1/Part1/) |
| **Software Evolutions & Full-Stack System (Part 2)** | [B1/Part2/](B1/Part2/) |
| **Cross-Language Implementations & Benchmarks (Part 3)** | [B1/Part3/](B1/Part3/) |
| **Canonical Datasets & Raw Evidence Logs** | [B1/data/](B1/data/) |
| **Restaurant POS Full-Stack Integration Overlay** | [B1/restaurant_integration/](B1/restaurant_integration/) |
---

## Scope and Evidence

The analyzed application is a multi-tier restaurant management POS system built with React, Node.js, Express, TypeScript, Prisma ORM, PostgreSQL/SQLite, and Socket.IO.

1. **Part 1 (Baseline Discovery):** Inspected baseline codebase for architectural patterns, establishing Façade (`AuthService`, `OrderService`), Observer (Socket.IO event bus), and Chain of Responsibility (Express auth middleware).
2. **Part 2 (Three Evolutions):**
   - **Evolution 1 (Online Ordering):** Public endpoints with server-side pricing validation and real-time station notification.
   - **Evolution 2 (Kitchen Workflow):** Partitioning kitchen orders across station-specific Socket.IO rooms (`cold`, `hot`, `bar`) using deterministic course routing.
   - **Evolution 3 (Payment Strategy):** GoF Strategy Pattern refactoring with concrete strategies for Cash, CreditCard, MobilePay, and GiftCard.
   - Verified via automated test suite `verify_evolutions.ts` (28/28 assertions passed, 100%).
3. **Part 3 (Cross-Language Evaluation):** 10 GoF patterns implemented across Java, Python, JavaScript, and C++ (40 standalone programs). Benchmarked for LOC, cyclomatic complexity, and median execution time in `data/cross_language.csv`.

---

## Validation

All evolutions and pattern demonstrations are fully reproducible:
- **Evolution Test Suite:** `cd apps/backend && node dist/scripts/verify_evolutions.js` (28/28 passed).
- **Cross-Language Benchmarks:** `python B1/Part3/benchmark.py` (executes all 40 implementations).
- **Report Compilation:** LaTeX source compiles via `pdflatex -interaction=nonstopmode B1_Report.tex` without errors.

---

## Team B1

| Student Name | Roll Number | Primary Contributions |
|:---|:---|:---|
| **Srivarma Battini** | AM.SC.U4AIE23032 | Full-stack backend/frontend architecture, Strategy pattern refactoring, LaTeX report |
| **Student 2** | AM.SC.U4AIE23110 | Evolution 1 Online Ordering implementation & validation |
| **Student 3** | AM.SC.U4AIE23057 | Evolution 2 Kitchen Workflow room partitioning & WebSocket routing |
| **Student 4** | AM.SC.U4AIE23039 | Evolution 3 Payment Strategy engine & concrete payment classes |
| **Student 5** | AM.SC.U4AIE23053 | Cross-language benchmarking (Java, Python, JS, C++) & dataset auditing |
