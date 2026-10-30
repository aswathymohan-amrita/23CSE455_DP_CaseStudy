# Front Controller - tRPC API Front Controller (JavaScript)

- Production code: `frontController.js`
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
- test result: **14/14**, median process time 59.7 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 58; max function CC: 10

## Language notes
Closest to tRPC: Map of procedure records, string path split for batching, instanceof TRPCError decides the code; closures count contexts/errors in the runner. Max-CC function: dispatch.
