# Java and C++ results summary

This file records Soorya's Java and C++ runs for Strategy and Observer.
The four Java/C++ test runners were compiled and executed in the recorded environment.
Govind's Python and JavaScript results are in `../README.md` and
`../../data/cross_language.csv`. The two language pairs use different inputs,
so this file does not establish a four-language comparison.

## Actual test results

- **Strategy / Java:** RESULT 4/4
- **Observer / Java:** RESULT 4/4
- **Strategy / C++:** RESULT 4/4
- **Observer / C++:** RESULT 4/4

## Measured summary

| Pattern | Language | Production LOC | Max function CC (manual McCabe audit) | Median process time (ms) |
|---|---:|---:|---:|---:|
| Strategy | Java | 33 | 4 | 36.116 |
| Observer | Java | 24 | 2 | 42.995 |
| Strategy | C++ | 35 | 4 | 1.115 |
| Observer | C++ | 30 | 2 | 1.070 |

Timing includes process startup and test harness and excludes compilation. Values are specific to this machine; see raw measurements in `timing_raw.csv`.
Cyclomatic complexity values are based on the documented function-by-function manual McCabe audit (`M = 1 + D`); see `complexity_audit.csv` and `complexity_audit.md`. This is not output from an external static-analysis package.

## Interpretation

- Java and C++ preserve the same test behaviour for the two selected examples.
- The Strategy examples use an interface/abstract class and concrete provider strategies. The provider implementations return deterministic chunks instead of calling real LLM services.
- The Observer examples demonstrate notification and unsubscribe behaviour. They do not connect to Supabase.
- Process-level timing for tiny programs is strongly affected by runtime/process startup and is not a general language-performance ranking.
- The original source has an implicit Strategy contract and uses an if-chain. The cross-language samples make the strategy roles explicit to compare the pattern clearly; this structural simplification must be acknowledged.
- This summary covers Java and C++ only. Python and JavaScript are also present in Part 3, with their own saved test evidence.
