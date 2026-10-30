# Singleton - Shared Prisma Database Client (Java)

- Production code: `SharedDbClient.java`
- Test runner (kept separate): `Runner.java`
- Shared fixture and specification: `../cases.tsv`, `../spec.md`
- Runtime / compiler: javac 21.0.12.1 / openjdk version "21.0.12.1" 2026-08-18 LTS

## Run (working folder: this folder)
```
javac -d build *.java
java -cp build Runner ../cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass. Raw output of the recorded run: `test_result.log`.

## Result recorded in Part3/llm/pattern_crosslanguage.csv
- test result: **9/9**, median process time 92.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 28; max function CC: 4

## Language notes
Holder is an explicit ProcessGlobals object (Java has no globalThis); idiomatic Java would use a static holder / enum singleton, which cannot be reset per test case. Max-CC function: DbModule::DbModule.
