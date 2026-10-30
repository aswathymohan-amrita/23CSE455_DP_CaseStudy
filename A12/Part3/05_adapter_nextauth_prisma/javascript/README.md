# Adapter - NextAuth Prisma Persistence Adapter (JavaScript)

- Production code: `authAdapters.js`
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
- test result: **9/9**, median process time 58.0 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 31; max function CC: 2

## Language notes
Like the real @next-auth/prisma-adapter: a factory returns an object literal whose methods translate to orm.user.create({data}) etc.; no class or interface. Max-CC function: create.
