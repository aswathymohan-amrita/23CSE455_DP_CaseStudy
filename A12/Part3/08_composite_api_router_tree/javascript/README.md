# Composite - API Router Tree (JavaScript)

- Production code: `routerTree.js`
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
- test result: **12/12**, median process time 53.4 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 36; max function CC: 3

## Language notes
Nodes are plain objects with the same methods, like tRPC's router records (procedures and routers mixed in one record); Map keeps order. Max-CC function: resolve.
