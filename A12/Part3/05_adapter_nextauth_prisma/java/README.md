# Adapter - NextAuth Prisma Persistence Adapter (Java)

- Production code: `AuthAdapters.java`
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
- test result: **9/9**, median process time 124.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 50; max function CC: 2

## Language notes
Object adapter: class implements the Target interface and holds the adaptee; the ORM's map-based arguments (Map.of(...)) must be built explicitly; Optional for 'no user'. Max-CC function: OrmClient::userCreate.
