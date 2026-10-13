# LLM Evidence Provenance and Verification Audit — Team B1

**Course:** 23CSE455 Design Patterns  
**Team:** B1  
**Project:** Restaurant Management POS System  
**Date:** October 11, 2026  

---

## 1. Compliance Standard

The academic instructions require an **exact prompt, exact input context, raw model response, and human source/test verification** for each recorded LLM interaction. All prompts, model details, evaluations, and verification notes for Team B1 are tracked in `data/llm.csv` and organized by team member under `llm/` folders.

| Part | Evidence Present | Verification & Limitations |
|:---|:---|:---|
| **Part 1: Discovery** | Pattern CSV, baseline source excerpts in `data/code/`, `Part1/llm/verification.md`, and student prompts for Facade, Observer, and Chain of Responsibility. | Prompts focus on architectural identification of service facades and Socket.IO room patterns. Human verification confirmed against actual line numbers in `auth.service.ts` and `order.service.ts`. |
| **Part 2: Evolution** | Source change diffs, requirement specifications (`Change1`–`Change3`), and `Part2/llm.csv`. | Verbatim prompts and raw responses for Online Ordering, Kitchen Station Workflow, and Payment Strategy are preserved. Integration tests (`verify_evolutions.ts`) independently verify 28/28 assertions. |
| **Part 3: Cross-Language** | 40 source implementations, test execution logs in `data/test_result/`, benchmarking script (`benchmark.py`), and measured timings. | Standalone implementations in Java, Python, JavaScript, and C++ verified via fresh process executions. Timing benchmarks reflect 5-run median measurements. |

---

## 2. Human Verification Protocol

To ensure academic honesty and reproducibility, every AI-assisted code snippet or design pattern proposal underwent manual human verification:
1. **Source Inspection:** Verified exact method signatures and class structures against the TypeScript AST and Prisma schema.
2. **Deterministic Test Execution:** Developed `apps/backend/src/scripts/verify_evolutions.ts` to assert runtime pricing math, station mapping logic, and payment strategy resolution independently of LLM outputs.
3. **Cross-Language Validation:** Executed each pattern implementation in its respective language runtime (OpenJDK 11, CPython 3.10, Node.js 22) and logged stdout directly to `data/test_result/`.

---

## 3. Preservation of Transcripts

Full prompt histories and structured conversational templates for all five team members (`AM.SC.U4AIE23032`, `AM.SC.U4AIE23110`, `AM.SC.U4AIE23057`, `AM.SC.U4AIE23039`, `AM.SC.U4AIE23053`) are preserved in markdown and text formats under `Part1/llm/`, `Part2/llm/`, and `Part3/llm/`.
