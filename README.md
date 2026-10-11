# Team B7 — Design Patterns Case Study (23CSE455)

**Design Pattern Identification and Evolution in a Spring MVC-Based Warehouse Management Application**

We studied **OpenWMS**, an open-source warehouse management system written in Java and Spring. We found the GoF design patterns it uses, added three new features, and implemented two of the patterns in four programming languages so we could compare them.

| Roll number | Name | Batch |
|---|---|---|
| AM.SC.U4CSE23215 | D Aditya Kiran | CSE C |
| AM.SC.U4CSE23235 | Mithun Krishna | CSE C |
| AM.SC.U4CSE23248 | Sai Kishen K M | CSE C |
| AM.SC.U4CSE23359 | Sivadev Smijith | CSE D |

---

## Start here

If you only have a few minutes, open these in order:

1. **[`report/main.pdf`](report/main.pdf)** — the full case study report (all three parts in one document).
2. **[`report/part1_findings.pdf`](report/part1_findings.pdf)** — Part 1 in detail: which patterns we found and the evidence for each.
3. **[`report/part2_findings.pdf`](report/part2_findings.pdf)** — Part 2 in detail: the three new features and their tests.
4. **[`report/part3_findings.pdf`](report/part3_findings.pdf)** — Part 3 in detail: the four-language comparison and its metrics.

Everything else in this repository is **supporting evidence** (source code, tests, data and diagrams) behind the claims in those PDFs.

---

## Results at a glance

| Part | What we did | Result |
|---|---|---|
| **Part 1: Pattern discovery** | Inspected the OpenWMS core source code at commit `9d263bf` | **2 GoF patterns confirmed:** Observer (event subscription and dispatch) and Composite (`TreeNode` tree). We also recorded the rejected candidates and the reason for rejecting each one. |
| **Part 2: Evolution** | Added three new features | **CH01** Multiple-warehouse support (18 new tests) · **CH02** Barcode-based picking (14/14 tests pass) · **CH03** Automatic stock reordering (19/19 tests pass) |
| **Part 3: Cross-language** | Implemented Observer and Composite in Java, Python, JavaScript and C++ | **28/28 tests pass** across all 8 implementations. We also measured lines of code, cyclomatic complexity and runtime. |

---

## Repository map

```text
Team_B9_DP/
├── README.md                     ← you are here
│
├── report/                       ← THE REPORTS (start here)
│   ├── main.pdf                  ← full case study report
│   ├── part1_findings.pdf        ← Part 1 detailed findings
│   ├── part2_findings.pdf        ← Part 2 detailed findings
│   ├── part3_findings.pdf        ← Part 3 detailed findings
│   ├── *.tex                     ← LaTeX sources for the PDFs above
│   └── figures/                  ← diagrams used in the report
│
└── Team_B7_Findings/              ← ALL SUPPORTING EVIDENCE
    ├── Part1_Findings/           ← Part 1: pattern discovery
    ├── Part2/                    ← Part 2: the three new features
    │   ├── CH01-multiple-warehouses/
    │   ├── CH02-barcode-picking/
    │   └── CH03-stock-reorder/
    ├── Part3-cross-language/     ← Part 3: four-language implementations
    ├── LLM_RECORDS/              ← record of AI-assisted work and how we verified it
    └── COPY_MANIFEST.md          ← where each file in this folder came from
```

---

## Where to find each thing

### Part 1: Pattern discovery → `Team_B7_Findings/Part1_Findings/`

| File | What it shows |
|---|---|
| [`Part1_Findings.md`](Team_B7_Findings/Part1_Findings/Part1_Findings.md) | Written findings: each pattern, its participating classes, and why it qualifies |
| [`data/patterns.csv`](Team_B7_Findings/Part1_Findings/data/patterns.csv) | Table of the confirmed patterns |
| [`data/llm.csv`](Team_B7_Findings/Part1_Findings/data/llm.csv) | LLM chat links of each member |
| [`data/rejected_candidates.csv`](Team_B7_Findings/Part1_Findings/data/rejected_candidates.csv) | Patterns we considered and rejected, with the reason for each |
| [`data/pattern_counts.csv`](Team_B7_Findings/Part1_Findings/data/pattern_counts.csv) | Summary counts |
| [`diagrams/`](Team_B7_Findings/Part1_Findings/diagrams/) | UML diagrams for Observer and Composite, plus an architecture diagram (`.png` images, `.puml` sources) |
| [`evidence/verification_notes.md`](Team_B7_Findings/Part1_Findings/evidence/verification_notes.md) | How each finding was checked against the real source |

### Part 2: Evolution (new features) → `Team_B7_Findings/Part2/`

Each feature folder has a single evidence file. **Read that file first**, because it explains the requirement, the before/after design and the tests.

| Feature | Read this first | Code |
|---|---|---|
| **CH01: Multiple warehouses** | [`PROVENANCE.md`](Team_B7_Findings/Part2/CH01-multiple-warehouses/PROVENANCE.md) | Changes to two real OpenWMS modules. The `*.complete-source/` folders contain the full source; the other two folders contain only the changed files. |
| **CH02: Barcode-based picking** | [`CH02_EVIDENCE.md`](Team_B7_Findings/Part2/CH02-barcode-picking/CH02_EVIDENCE.md) | `src/main/java/…` (code) and `src/test/java/…` (tests) |
| **CH03: Automatic stock reordering** | [`CH03_EVIDENCE.md`](Team_B7_Findings/Part2/CH03-stock-reorder/CH03_EVIDENCE.md) | `src/main/java/…`, `src/test/java/…`, and a class diagram in [`CH03-class-diagram.puml`](Team_B7_Findings/Part2/CH03-stock-reorder/CH03-class-diagram.puml) |

### Part 3: Cross-language comparison → `Team_B7_Findings/Part3-cross-language/`

| File / folder | What it shows |
|---|---|
| [`PART3_EVIDENCE.md`](Team_B7_Findings/Part3-cross-language/PART3_EVIDENCE.md) | The common specification, how each language implements it, test commands and the comparison |
| `observer/{java,python,javascript,cpp}/` | Observer pattern implementation and test in each language |
| `composite/{java,python,javascript,cpp}/` | Composite pattern implementation and test in each language |
| [`metrics/cross_language.csv`](Team_B7_Findings/Part3-cross-language/metrics/cross_language.csv) | Lines of code, cyclomatic complexity, runtime and test results per language |
| [`metrics/pattern_metrics.csv`](Team_B7_Findings/Part3-cross-language/metrics/pattern_metrics.csv) | Structural metrics: classes, interfaces, inheritance depth and dependencies |

### AI usage record → `Team_B7_Findings/LLM_RECORDS/`

[`LLM_RECORDS.md`](Team_B7_Findings/LLM_RECORDS/LLM_RECORDS.md) lists the parts of the work that used an AI assistant. For each one it shows the evidence we used to check it independently and labels the result **CONFIRMED**, **PARTIALLY VERIFIED** or **NOT RECOVERABLE**.

---

## Running the code (optional)

**Part 2: CH02 and CH03** (requires Java and Maven). Run this from inside the feature folder:

```bash
cd Team_B7_Findings/Part2/CH02-barcode-picking   # or CH03-stock-reorder
mvn -DforkCount=0 verify
```

Expected result: CH02 reports 14 tests passing and CH03 reports 19.

**Part 3** — run this from inside a pattern/language folder, for example `Team_B7_Findings/Part3-cross-language/observer/python/`:

| Language | Command |
|---|---|
| Java | `javac *.java && java ObserverPatternTest` (use `CompositePatternTest` for the Composite folder) |
| Python | `python -m unittest -v` |
| JavaScript | `node observer.test.mjs` (or `composite.test.mjs`) |
| C++ | `g++ -std=c++20 observer_test.cpp -o test && ./test` (or `composite_test.cpp`) |

[`PART3_EVIDENCE.md`](Team_B7_Findings/Part3-cross-language/PART3_EVIDENCE.md) has the exact commands and the toolchain versions we recorded.

---

## Notes on scope

- **The original OpenWMS project:** <https://github.com/openwms/org.openwms>, baseline commit `9d263bf`. The Part 1 findings cover only code that actually exists in that repository.
- **CH02 and CH03** are standalone reference implementations that we built ourselves, because the OpenWMS Picking and Inventory services were not publicly available. They are *not* modifications of those services.
- **CH01** modifies real OpenWMS modules. It does not include a production data migration; [`PROVENANCE.md`](Team_B7_Findings/Part2/CH01-multiple-warehouses/PROVENANCE.md) explains this limitation.
- Each findings PDF ends with a **"Corrections made in the re-audit"** section listing what changed after we cross-checked all the findings against upstream OpenWMS.
