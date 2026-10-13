# Team B1 — Canonical Data Repository

This directory contains the canonical CSV datasets, baseline source code excerpts, raw test execution logs, and LLM provenance documentation for Team B1.

## Directory Structure

```text
data/
├── README.md                      # This overview and schema guide
├── LLM_PROVENANCE_AUDIT.md        # Provenance audit and human verification methodology
├── patterns.csv                   # Baseline and evolved GoF design patterns registry
├── pattern_counts.csv             # Statistical frequency of patterns across baseline & evolved
├── patterns_evolution.csv         # Change-by-change pattern evolution ledger
├── cross_language.csv             # 40-row evaluation matrix (LOC, CC, runtime, median ms)
├── llm.csv                        # Prompt and interaction history for all 5 team members
├── code/                          # Baseline application source code excerpts
│   ├── auth.service.ts            # Baseline authentication service facade
│   ├── order.service.ts           # Baseline order creation facade
│   ├── websocket.ts               # Baseline Socket.IO publisher/subscriber setup
│   ├── auth.ts                    # Baseline Express authentication middleware chain
│   └── schema.prisma              # Relational data models
└── test_result/                   # Raw console outputs from reproducible runs
    ├── <pattern>_<language>.txt   # Output logs for all 40 cross-language implementations
    └── verify_evolutions.txt      # 28/28 assertions output log
```

## Dataset Descriptions

1. **`patterns.csv`**: Contains verified baseline and evolved pattern collaborations, participant roles, and exact source code locations.
2. **`pattern_counts.csv`**: Statistical summary of pattern counts across baseline (4 types, 5 instances) vs evolved system (10 types, 13 instances).
3. **`patterns_evolution.csv`**: Evolution audit ledger documenting preservation, extension, modification, and newly introduced pattern instances.
4. **`cross_language.csv`**: Complete 40-row evaluation matrix containing physical LOC, maximum function cyclomatic complexity, runtime versions, test commands, and median process execution time.
5. **`llm.csv`**: Full LLM usage audit trail tracking prompts, model versions, dates, input context, generated code, and human verification notes for all 5 students.
