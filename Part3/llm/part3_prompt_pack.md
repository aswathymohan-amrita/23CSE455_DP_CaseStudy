# B14 Design Patterns Case Study — Part 3 Prompt Pack
## Java and C++ implementation, testing, measurement, and reporting

**Purpose:** A reusable set of prompts for implementing and verifying Part 3.

**Scope:** Exactly two patterns—**Strategy (LLM Provider Streaming)** and **Observer (Authentication State)**—implemented in **Java and C++ only** for this working phase. Use Part 1 for confirmed pattern evidence and review Part 2 changes so the report does not claim that a baseline file contains changes that are not present.

**Provenance note:** These are proposed/reconstructed prompts prepared as a reusable prompt pack. Do not present them as verbatim historical prompts actually submitted to an AI tool unless they match the saved conversation or actual prompt logs. For the final `llm.csv`, record only real AI interactions, actual outputs, dates, model labels, and verification evidence.

---

## Prompt 1 — Inspect evidence and establish scope

> I am working on Part 3 (Cross-Language Comparison) of the B14 23CSE455 Design Patterns case study.
>
> Inspect the supplied B14 project files, especially the Part 1 pattern inventory, original source code, Part 2 change records, and current Part 3 directory.
>
> For this working comparison, use exactly two patterns: (1) Strategy — LLM Provider Streaming; and (2) Observer — Authentication State. Use Java and C++ only in this working phase. Do not implement Python or JavaScript.
>
> Verify the original source evidence and map the actual participant roles. Distinguish production implementation from simplified cross-language examples. Review Part 2 change records and determine whether changed source files are actually present in the supplied snapshot. Do not assume a change is merged merely because a report describes it.
>
> Produce a scope statement, source-to-pattern mapping table, selection rationale, list of missing/inconsistent evidence, and outstanding requirements. Do not invent source paths, class names, commits, test results, or measurements.

## Prompt 2 — Define language-independent specifications

> For Strategy and Observer, create a language-independent specification before writing code.
>
> Strategy: deterministic selection among Claude, OpenAI, and Gemini provider strategies; define response-chunk format and unsupported-provider error.
>
> Observer: authentication event source with subscribe, publish, and unsubscribe; cover sign-in, sign-out, unsubscribe, and multiple observers.
>
> For each, specify purpose, participant roles, inputs/outputs, rules, normal/boundary/error cases, exact expected outputs, assumptions, and exclusions. These are deterministic educational examples, not real LLM or Supabase calls. Do not write implementation code yet.

## Prompt 3 — Create common test cases

> Create `Part3/test-cases/common_test_cases.csv` from the approved specifications. Use one row per case and columns for pattern name, test ID, inputs, expected result, and description. Use S01–S04 for Strategy (Claude, OpenAI, Gemini, unsupported provider) and O01–O04 for Observer (sign-in, sign-out, no notification after unsubscribe, two active observers).
>
> Expected results must be precise enough to implement identically in Java and C++. Quote CSV cells containing commas and use UTF-8. This prompt defines tests only; do not claim they passed.

## Prompt 4 — Implement Strategy in Java

> Implement the Strategy example in Java using the approved specification and common test cases. Use a common strategy contract, concrete provider strategies, and a context/selector. Preserve chunk order and exact error behaviour. Keep production code and tests separate, avoid network calls and external dependencies, and include a test runner for S01–S04. Provide exact `javac`/`java` commands and a README.
>
> Explain how the small example relates to the verified original Strategy instance and identify structural differences from the TypeScript source. Do not invent test output; provide commands so it can be run.

## Prompt 5 — Implement Strategy in C++

> Implement the same Strategy specification in C++17. Use an abstract strategy contract and concrete provider implementations. Preserve exactly the Java version's inputs, output chunks, and unsupported-provider error. Keep production code and tests separate, avoid external dependencies, test S01–S04, and provide exact `g++ -std=c++17` compile/run commands.
>
> Compare participant mapping to Java. Do not alter behaviour merely to make the C++ version more idiomatic. Do not claim tests passed until the program is compiled and run.

## Prompt 6 — Implement Observer in Java

> Implement the authentication Observer example in Java. Define an observer/listener contract and an event source supporting subscribe, publish, and unsubscribe. Add a recording listener for tests. Notify every active observer and ensure an unsubscribed observer receives no later events.
>
> Keep production code and tests separate. Implement O01–O04 with assertions and a clear pass/fail summary. Provide compile/run commands. Explain how the educational example maps to the original Supabase subscription in React, without claiming the Java example is production code or connects to Supabase.

## Prompt 7 — Implement Observer in C++

> Implement the same authentication Observer specification in C++17. Define an observer interface and event source with subscribe, publish, unsubscribe, and multiple-observer support. Preserve the Java version's event names, payloads, and expected outcomes. Keep production code and tests separate, implement O01–O04, and provide exact compile/run commands.
>
> Explain pointer/reference lifetime assumptions and avoid dangling observers in the tests. Do not add unrelated dependencies or claim success until the code has been run.

## Prompt 8 — Verify cross-language equivalence

> Review both patterns in Java and C++ against `common_test_cases.csv`. For every test ID, create a table showing expected behaviour, Java assertion/result, C++ assertion/result, pass/fail status, and whether any differences are syntactic or behavioural.
>
> Compile and run both implementations. Save actual commands, compiler/runtime versions, stdout, stderr, and exit status. Fix failures and rerun. Do not silently change the common specification to accommodate a bug. Never fabricate results for code that was not run.

## Prompt 9 — Measure production LOC

> Measure production source LOC for Strategy/Java, Strategy/C++, Observer/Java, and Observer/C++. Apply one consistent rule: count nonblank production-code lines, excluding comments, test code, and the agreed preprocessor/guard lines. Document the rule and list the exact files counted.
>
> Update `source_loc` in `Part3/cross_language.csv`. Keep tests and README files excluded. Provide a reproducible calculation or script. Do not reuse earlier numbers without checking the current source files.

## Prompt 10 — Audit cyclomatic complexity

> Audit cyclomatic complexity for all functions/methods in the four production implementations. State the exact counting convention, including treatment of `if`/`else if`, loops, switch cases, exception handlers, short-circuit conditions, and logical operators.
>
> Prefer an available static-analysis tool accepted by the course. Record tool/version, command, and output. If the result is manual, label it as a manual audit—not tool-generated.
>
> Create `Part3/evidence/complexity_audit.csv` with one row per function/method: source path, function name, decision points, calculated CC, counting rule, and tool/manual method. Update `max_function_cc` in `cross_language.csv`. Do not invent tool output or claim independent verification if no tool was run.

## Prompt 11 — Measure process execution time

> Measure elapsed process time for each Java and C++ test runner on the same machine. Compile first, run one warm-up, then five measured process launches. Record every measurement in milliseconds and calculate the median. State whether timing includes process startup, runtime initialization, test harness, and input reading. Record OS and compiler/runtime versions and relevant flags.
>
> Save raw data in `Part3/evidence/timing_raw.csv` and update `median_process_ms` in `cross_language.csv`. Do not estimate missing values or compare measurements from different conditions without explaining the limitation.

## Prompt 12 — Build the comparison CSV

> Create/update `Part3/cross_language.csv` with these exact columns:
>
> `pattern_name,instance_name,language,snippet_path,source_loc,max_function_cc,runtime_compiler,test_command,test_result,median_process_ms,language_notes`
>
> For the current reduced scope, create one row per pattern per implemented language: Strategy/Java, Strategy/C++, Observer/Java, Observer/C++. Bind fields to current source, actual test output, recorded toolchain versions, LOC measurements, complexity audit, and timing evidence. Use paths relative to the B14 team folder and quote CSV cells containing commas.
>
> Use `not_run` with a reason when a measurement was not performed. Do not fabricate or estimate values. State that the official handout requires four languages and this CSV covers only the Java/C++ working scope.

## Prompt 13 — Write comparison and interpretation

> Write the Part 3 comparison using only evidence in the current project. Discuss how Strategy contracts/concrete strategies are represented in Java and C++; how Observer subscription, notification, and unsubscribe are represented; LOC and maximum function complexity; actual tests; median timing and its scope; language-specific abstraction, inheritance, composition, and ownership/lifetime considerations; and limitations compared with the original TypeScript/React/Supabase application.
>
> Do not claim lower LOC or faster timing proves a language is generally superior. Do not call the examples production ports. Separate measured facts from interpretation and limitations.

## Prompt 14 — Record genuine AI use and human verification

> Prepare `Part3/llm/llm.csv` using the required columns:
>
> `part,model_and_date,prompt_file,input_file,output_file,evaluation,verification_file`
>
> Record only AI interactions that actually occurred. Preserve the exact prompt, supplied input/context, raw output, displayed model name, and actual date. Evaluate important claims as correct, partially correct, incorrect, or cannot confirm, with evidence.
>
> Do not manufacture historical prompts, outputs, model names, dates, or verification results. If a field is unknown, leave it blank or mark it unavailable according to the project convention. Keep proposed prompts in a separate prompt pack rather than misrepresenting them as past interactions.

## Prompt 15 — Final compliance audit

> Audit the current B14 Part 3 directory against the assignment and the team's reduced Java/C++ scope.
>
> Check that both patterns are confirmed in Part 1; Part 2 changes and source snapshot are described accurately; shared cases match both runners; all four Java/C++ test runners compile and run; logs contain actual commands/output/exit status; LOC rules are reproducible; complexity values trace to the declared method/tool; five raw timing runs and medians exist; CSV headers and paths match the prescribed schema; AI records contain only genuine interactions; README commands work; limitations and missing Python/JavaScript are explicit; and no placeholder or invented result is presented as verified.
>
> Produce a checklist with `met`, `partially met`, `not met`, or `cannot verify`, citing exact paths. Do not mark the assignment complete if any mandatory requirement remains unmet.

---

## Suggested evidence directory

```text
B14/
└── Part3/
    ├── README.md
    ├── test-cases/
    │   └── common_test_cases.csv
    ├── strategy/
    │   ├── java/
    │   └── cpp/
    ├── observer/
    │   ├── java/
    │   └── cpp/
    ├── evidence/
    │   ├── test_results.txt
    │   ├── environment.txt
    │   ├── timing_raw.csv
    │   ├── complexity_audit.csv
    │   └── complexity_audit.md
    ├── cross_language.csv
    └── llm/
        ├── part3_prompt_pack.md
        └── llm.csv
```

## Submission note

This pack contains reusable prompts and a recommended workflow. It is not proof that every prompt was historically submitted or that every requested action was performed. For an honest AI-use record, retain the prompts and outputs from the interactions actually used; use this pack as supporting methodology or for remaining work.
