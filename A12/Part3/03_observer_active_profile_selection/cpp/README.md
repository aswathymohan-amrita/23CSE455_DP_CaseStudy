# Observer - Active Profile Selection (C++)

- Production code: `profile_selection.hpp`
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
- test result: **11/11**, median process time 13.7 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 50; max function CC: 3

## Language notes
Observers are non-owning pointers to an abstract base; registration order kept in a std::vector with a duplicate check; lifetime must outlive the subject. Max-CC function: profiles::ProfileStore::setState.
