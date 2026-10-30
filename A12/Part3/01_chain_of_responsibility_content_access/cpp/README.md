# Chain of Responsibility - Content Access Rule Chain (C++)

- Production code: `content_access.hpp`
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
- test result: **16/16**, median process time 14.7 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 86; max function CC: 6

## Language notes
Ownership of the chain via std::unique_ptr (each link owns the next); std::optional<Decision> as 'pass on' signal; virtual dispatch; header-only. Max-CC function: access::MaturityRule::evaluate.
