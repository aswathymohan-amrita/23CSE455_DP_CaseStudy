# Front Controller - tRPC API Front Controller (Java)

- Production code: `FrontController.java`
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
- test result: **14/14**, median process time 154.5 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 68; max function CC: 11

## Language notes
Registry is a Map<String, Procedure> of records holding BiFunction resolvers; checked TRPCError vs. unchecked RuntimeException mirrors the two error paths; context factory and error hook are injected functional interfaces. Max-CC function: Procedure::dispatch.
