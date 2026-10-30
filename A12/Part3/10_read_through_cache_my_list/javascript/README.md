# Read-Through Cache - My List Query Cache (JavaScript)

- Production code: `myListCache.js`
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
- test result: **9/9**, median process time 65.0 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 33; max function CC: 3

## Language notes
Map-based cache with loader closures, the same shape as React Query's fetchQuery(key, fn); arrays copied with spread so the backend cannot mutate cached data. Max-CC function: add.
