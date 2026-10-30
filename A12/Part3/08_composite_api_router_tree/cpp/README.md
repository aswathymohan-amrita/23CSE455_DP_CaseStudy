# Composite - API Router Tree (C++)

- Production code: `router_tree.hpp`
- Test runner (kept separate): `test_runner.cpp`
- Shared fixture and specification: `../cases.tsv`, `../spec.md`
- Runtime / compiler: g++ (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r3) 16.2.0 -std=c++17 -O2

## Run (working folder: this folder)
```
g++ -std=c++17 -O2 -Wall -o build/test_runner test_runner.cpp
./build/test_runner ../cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass. Raw output of the recorded run: `test_result.log`.

## Result recorded in Part3/llm/pattern_crosslanguage.csv
- test result: **12/12**, median process time 14.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 70; max function CC: 4

## Language notes
Abstract base Node; Router owns children via std::unique_ptr in a vector of pairs (ordered); recursion through virtual calls. Max-CC function: routers::Router::resolve.
