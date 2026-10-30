# Singleton - Shared Prisma Database Client (JavaScript)

- Production code: `sharedDbClient.js`
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
- test result: **9/9**, median process time 51.5 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 17; max function CC: 4

## Language notes
Closest to the source: ?? for reuse-or-create and an object standing in for globalThis; module cache gives the singleton in real code. Max-CC function: loadDbModule.
