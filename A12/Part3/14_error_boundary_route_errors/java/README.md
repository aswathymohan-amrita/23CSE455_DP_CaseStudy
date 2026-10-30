# Error Boundary - Shows Segment Error Boundary (Java)

- Production code: `ErrorBoundaryApp.java`
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
- test result: **10/10**, median process time 122.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 76; max function CC: 3

## Language notes
Component interface with lambdas as fallbacks (e -> () -> ...); unchecked RenderError; boundary state is a nullable field reset by the retry button. Max-CC function: ErrorBoundary::render.
