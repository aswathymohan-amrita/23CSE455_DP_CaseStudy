# Context Object - tRPC Request Context (JavaScript)

- Production code: `requestContext.js`
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
- test result: **14/14**, median process time 67.2 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 50; max function CC: 4

## Language notes
Plain object spread {...ctx, planTier} mirrors tRPC next({ctx}); reduce chains the middlewares; Object.keys().sort() lists keys. Max-CC function: attachSubscription.
