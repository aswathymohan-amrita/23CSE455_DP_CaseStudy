# Builder - tRPC Procedure Builder (JavaScript)

- Production code: `procedureBuilder.js`
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
- test result: **14/14**, median process time 59.6 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 81; max function CC: 6

## Language notes
Object.freeze on middleware arrays and on the Procedure; spread creates the next builder, exactly like tRPC createNewBuilder; product and builder told apart with instanceof. Max-CC function: build.
