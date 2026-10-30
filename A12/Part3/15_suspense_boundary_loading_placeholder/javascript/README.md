# Suspense Boundary - Shows Loading Placeholder (JavaScript)

- Production code: `suspenseBoundary.js`
- Test runner (kept separate): `testRunner.js`
- Shared fixture and specification: `../cases.tsv`, `../spec.md`
- Runtime / compiler: Node.js v26.13.0

## Run (working folder: this folder)
```
node testRunner.js ../cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass. Raw output of the recorded run: `test_result.log`.

## Result recorded in Part3/llm/pattern_crosslanguage.csv
- test result: **10/10**, median process time 60.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 51; max function CC: 7

## Language notes
Throwing a sentinel (Pending) mirrors how React Suspense really works (thrown thenable); Set + sort for event times. Max-CC function: stream.
