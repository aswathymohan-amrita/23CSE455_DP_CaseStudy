# Team B1 — Restaurant POS System Integration Overlay

This directory contains the full-stack integration overlay for the React and Node.js-based Restaurant Management Application, verifying the three architectural evolutions.

## Components & Structure

```text
restaurant_integration/
├── README.md               # This integration and execution guide
├── install.py              # Automated test runner and build verifier
├── routes/                 # Evolved Express HTTP route definitions
├── services/               # Core business services implementing GoF patterns
│   ├── order.service.ts    # Extended Façade with online order validation & pricing
│   ├── payment.service.ts  # Strategy Pattern engine (Cash, Card, Mobile, Gift)
│   └── websocket.ts        # Observer room dispatcher with course-to-station routing
└── tests/                  # Automated integration tests
    └── verify_evolutions.ts# 28-assertion test suite (100% passing)
```

## How to Verify
From the repository root or this directory, run:
```bash
python install.py
```
Or directly via Node.js in `apps/backend`:
```bash
cd apps/backend
node dist/scripts/verify_evolutions.js
```
