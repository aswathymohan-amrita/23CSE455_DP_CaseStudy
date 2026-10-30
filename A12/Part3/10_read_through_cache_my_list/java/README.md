# Read-Through Cache - My List Query Cache (Java)

- Production code: `MyListCache.java`
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
- test result: **9/9**, median process time 108.8 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 37; max function CC: 2

## Language notes
Generic QueryCache<K,V> with Supplier<V> loader; HashMap.computeIfAbsent is a built-in read-through primitive; lists copied with List.copyOf to keep cached values immutable. Max-CC function: MyListStore::add.
