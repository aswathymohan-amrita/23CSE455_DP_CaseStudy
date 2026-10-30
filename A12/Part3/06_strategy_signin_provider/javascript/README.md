# Strategy - Sign-in Provider Strategy (JavaScript)

- Production code: `signIn.js`
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
- test result: **10/10**, median process time 59.3 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 31; max function CC: 3

## Language notes
Like next-auth: each provider is a factory returning a config object {id, authorize}; the context only needs the shape (duck typing). Max-CC function: signIn.
