# Scatter-Gather - TMDB Row Scatter-Gather (JavaScript)

- Production code: `scatterGather.js`
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
- test result: **8/8**, median process time 66.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 10; max function CC: 2

## Language notes
Promise.all over async recipients is exactly the source code idiom (lib/fetchers.ts); Object.fromEntries rebuilds the keyed result. Max-CC function: fetchRows.
