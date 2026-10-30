# Chain of Responsibility - Content Access Rule Chain (JavaScript)

- Production code: `contentAccess.js`
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
- test result: **16/16**, median process time 54.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 60; max function CC: 3

## Language notes
ES2022 class with private #next field and static tables; 'abstract' evaluate() can only throw at run time; decisions are plain object literals. Max-CC function: check.
