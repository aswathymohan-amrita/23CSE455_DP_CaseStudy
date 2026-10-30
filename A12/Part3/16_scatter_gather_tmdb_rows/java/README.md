# Scatter-Gather - TMDB Row Scatter-Gather (Java)

- Production code: `ScatterGather.java`
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
- test result: **8/8**, median process time 136.0 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 26; max function CC: 1

## Language notes
CompletableFuture.supplyAsync per row (scatter) and allOf().join() (gather) on the common ForkJoinPool; request order kept by joining the futures list in order. Max-CC function: ScatterGather::Row.
