# Scatter-Gather - TMDB Row Scatter-Gather (C++)

- Production code: `scatter_gather.hpp`
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
- test result: **8/8**, median process time 18.4 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 45; max function CC: 6

## Language notes
std::async(std::launch::async) starts one thread per row; futures are collected in request order with get(); real OS threads make this the heaviest variant at run time. Max-CC function: sg::fetchRows.
