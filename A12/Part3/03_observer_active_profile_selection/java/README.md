# Observer - Active Profile Selection (Java)

- Production code: `ProfileSelection.java`
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
- test result: **11/11**, median process time 94.0 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 44; max function CC: 3

## Language notes
Observer interface + LinkedHashSet keeps subscription order and set semantics; Consumer-style callbacks would also work; observers need explicit classes or lambdas. Max-CC function: ProfileStore::setState.
