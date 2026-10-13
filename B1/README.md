# Team B1 — 23CSE455 Design Patterns Case Study

**Course:** 23CSE455  
**Case Study Title:** Design Pattern Identification and Evolution in a React and Node.js-Based Restaurant Management Application  
**Team Identifier:** B1  
**Date:** October 11, 2026  

---

## 👥 Team Members & Contributions

| Roll Number | Student Name | Assigned Patterns | Pattern Type | Domain |
|:---|:---|:---|:---|:---|
| **AM.SC.U4AIE23032** | Surya Dingari | **Façade**, **Chain of Responsibility** | Structural, Behavioral | Service facade orchestration, Auth middleware |
| **AM.SC.U4AIE23110** | Vijay Reddy | **Observer**, **Strategy** | Behavioral, Behavioral | Real-time KDS dispatch, Payment engine |
| **AM.SC.U4AIE23057** | Srivarma | **Adapter**, **State** | Structural, Behavioral | Delivery payload normalizer, Table lifecycle |
| **AM.SC.U4AIE23039** | Bruhadesh | **Factory Method**, **Decorator** | Creational, Structural | Dynamic kitchen tickets, Menu item modifiers |
| **AM.SC.U4AIE23053** | Teja | **Command**, **Template Method** | Behavioral, Behavioral | POS cart actions with undo, Fulfillment pipeline |

---

## 📁 Submission Directory Structure

```text
submission/
└── B1/
    ├── README.md                      # This reproduction and navigation guide
    ├── corrections_and_limitations.md # Architectural fixes, bug solutions, and environment scope
    ├── B1_Report.tex                  # Comprehensive LaTeX source report
    ├── B1_Final_Report.pdf            # PDF report (compiled via pdfLaTeX/Overleaf)
    ├── submission_manifest.md         # Full manifest of copied files and origins
    ├── data/                          # 5 Canonical CSV datasets
    │   ├── patterns.csv               # Baseline & evolved pattern registry
    │   ├── pattern_counts.csv         # Pattern frequency counts (baseline vs evolved)
    │   ├── patterns_evolution.csv     # Evolution change ledger
    │   ├── cross_language.csv         # 40 cross-language benchmarks (LOC, CC, timing)
    │   └── llm.csv                    # 5-student LLM prompt and verification log
    ├── Part1/                         # Pattern Discovery
    │   ├── code/                      # Original pattern implementation snippets & demos
    │   ├── evidence/                  # Baseline patterns CSV and discovery report
    │   ├── pattern_architecture/      # Architecture overview
    │   └── llm/                       # Part 1 LLM prompts and human verification
    ├── Part2/                         # Evolution & Refactoring
    │   ├── code/                      # Evolved full-stack application (apps/backend, apps/frontend)
    │   ├── changes/
    │   │   ├── Change1/               # Online Ordering (requirement, acceptance criteria, demo)
    │   │   ├── Change2/               # Kitchen Station Workflow (routing algorithm, demo)
    │   │   └── Change3/               # Payment Strategy Pattern (strategy architecture, demo)
    │   ├── diagrams/                  # Sequence and class diagrams
    │   ├── evidence/                  # Evolution CSVs and report
    │   └── llm/                       # Evolution LLM logs
    └── Part3/                         # Cross-Language Evaluation (10 patterns × 4 languages)
        ├── adapter/                   # Java, Python, JavaScript, C++
        ├── command/                   # Java, Python, JavaScript, C++
        ├── cor/                       # Java, Python, JavaScript, C++
        ├── decorator/                 # Java, Python, JavaScript, C++
        ├── facade/                    # Java, Python, JavaScript, C++
        ├── factory/                   # Java, Python, JavaScript, C++
        ├── observer/                  # Java, Python, JavaScript, C++
        ├── state/                     # Java, Python, JavaScript, C++
        ├── strategy/                  # Java, Python, JavaScript, C++
        ├── template_method/           # Java, Python, JavaScript, C++
        ├── test-cases/                # Common test inputs and expected outputs
        ├── evidence/                  # Benchmark methodology and timing records
        └── llm/                       # Cross-language LLM prompts for all 5 students
```

---

## 🚀 Reproduction & Execution Instructions

### 1. Evolution Verification Test Suite (28/28 Passed)
```bash
cd apps/backend
npm run build
node dist/scripts/verify_evolutions.js
```
**Results:**
- Evolution 1 (Online Ordering): 3/3 passed (server-side pricing, tax calculations, validation)
- Evolution 2 (Kitchen Workflow): 9/9 passed (station routing across Cold, Hot, and Bar)
- Evolution 3 (Payment Strategy): 16/16 passed (Cash, CreditCard, MobilePay, GiftCard algorithms)
- **Total:** 28/28 assertions passed (100% success rate).

### 2. Full-Stack Application
```bash
# Terminal 1 - Backend API (Port 3000)
cd apps/backend
npm run dev

# Terminal 2 - Frontend UI (Port 5173)
cd apps/frontend
npm run dev
```

### 3. Cross-Language Pattern Implementations (40/40 Verified)
All 10 patterns are implemented in 4 languages:
- **Python (10/10):** `python Part3/<pattern>/python/<Pattern>Demo.py`
- **Node.js (10/10):** `node Part3/<pattern>/javascript/<Pattern>Demo.js`
- **Java (10/10):** `java -cp Part3/<pattern>/java <Pattern>Demo`
- **C++ (10/10):** Standard C++17 implementations under `Part3/<pattern>/cpp/<Pattern>Demo.cpp`

### 4. Compiling the LaTeX Report to PDF
`B1_Report.tex` uses standard LaTeX packages (`geometry`, `fontenc`, `hyperref`, `longtable`, `booktabs`, `enumitem`):
```bash
pdflatex B1_Report.tex
# Or upload directly to Overleaf and compile with pdfLaTeX
```

---

## 📊 Canonical Datasets Summary (`data/`)

1. **`patterns.csv`**: Contains verified baseline and evolved pattern collaborations, participant roles, and exact source code locations.
2. **`pattern_counts.csv`**: Statistical summary of pattern counts across baseline (4 types, 5 instances) vs evolved system (10 types, 13 instances).
3. **`patterns_evolution.csv`**: Evolution audit ledger documenting preservation, extension, modification, and newly introduced pattern instances.
4. **`cross_language.csv`**: Complete 40-row evaluation matrix containing physical LOC, maximum function cyclomatic complexity, runtime versions, test commands, and median process execution time.
5. **`llm.csv`**: Full LLM usage audit trail tracking prompts, model versions, dates, input context, generated code, and human verification notes for all 5 students.
