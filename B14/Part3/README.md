# Part 3: Strategy and Observer

This folder contains small examples of two patterns found in the original app:
Strategy for LLM provider streaming and Observer for auth state changes. These are
teaching examples, not copies of the Next.js app.

Govind wrote the Python and JavaScript examples. Soorya wrote the Java and C++
examples. The two sets currently use different inputs and expected outputs. Each
set has its own passing tests, but we have not yet proved that all four languages
behave the same way. The final report must say this until one shared test set is
used across all four languages.

## Python and JavaScript

Code and shared JSON cases:

- `llm_provider_streaming/`: Strategy specification, fixtures, Python and JavaScript.
- `auth_state_observer/`: Observer specification, fixtures, Python and JavaScript.

From `B14/`, run:

```powershell
python Part3/llm_provider_streaming/python/test_implementation.py
node --test Part3/llm_provider_streaming/javascript/test_implementation.mjs
python Part3/auth_state_observer/python/test_implementation.py
node --test Part3/auth_state_observer/javascript/test_implementation.mjs
python Part3/verify_cross_language.py
```

Strategy passed 11/11 cases in each language. Observer passed 15/15 in each
language. The Python and JavaScript process check passed 26/26 cases. Test logs
are in `evidence/tests/`. Their measured rows are in `../data/cross_language.csv`.
Code lines and complexity were measured with Lizard 1.24.1. One warm-up run and
five measured runs were used for each program. Timing includes process startup,
JSON input reading and output, but not tests or compilation. Raw values are in
`evidence/static_metrics.json` and `evidence/timings/process_timings.json`.

## Java and C++

Code and the separate CSV test specification:

- `strategy/java/` and `strategy/cpp/`: Strategy code and tests.
- `observer/java/` and `observer/cpp/`: Observer code and tests.
- `test-cases/common_test_cases.csv`: four cases per pattern for Java and C++.

From `B14/Part3/`, compile and run with a JDK and a C++17 compiler:

```sh
mkdir -p build/java/strategy build/java/observer build/cpp
javac -d build/java/strategy strategy/java/Strategy.java strategy/java/StrategyTest.java
java -cp build/java/strategy StrategyTest
javac -d build/java/observer observer/java/AuthObserver.java observer/java/ObserverTest.java
java -cp build/java/observer ObserverTest
g++ -std=c++17 -O2 -Wall -Wextra -pedantic strategy/cpp/test_strategy.cpp -o build/cpp/test_strategy
./build/cpp/test_strategy
g++ -std=c++17 -O2 -Wall -Wextra -pedantic observer/cpp/test_observer.cpp -o build/cpp/test_observer
./build/cpp/test_observer
```

The saved logs report 4/4 cases passed for each Java and C++ program. See
`evidence/test_results.txt`. Their measurements and notes are in
`cross_language.csv`, `evidence/timing_raw.csv` and
`evidence/complexity_audit.csv`. Soorya used a manual complexity audit. His
timings include process startup and the test runner. Those timings came from a
different machine and measurement setup, so do not rank them against Govind's
numbers.

## What the team still needs to do

1. Agree on one input, output and shared test set for all four languages.
2. Run that test set in all four languages and update the result logs.
3. Measure all four languages using the same timing boundary and machine.
4. Put the final verified rows in `../data/cross_language.csv`, then update the
   one team report and PDF.

The original handoff request is in `SOORYA_INTEGRATION.md`. Prompt records are
in `llm/part3_prompt.txt` for Soorya and `llm/govind_prompt.txt` for Govind.
`llm/verification.md` records what was checked for Govind's examples. The
partial `llm/llm.csv` row marks missing output and model details as
unavailable. The team can add them only if saved history supports them.
