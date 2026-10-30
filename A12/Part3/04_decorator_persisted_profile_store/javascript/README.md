# Decorator - Persisted Profile Store (JavaScript)

- Production code: `profileStores.js`
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
- test result: **11/11**, median process time 53.3 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 34; max function CC: 2

## Language notes
Zustand-style functional decorators: each is a function store -> store that spreads the inner object and overrides set/clearStorage; no classes needed. Max-CC function: basicStore.
