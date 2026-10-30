# Read-Through Cache - My List Query Cache (Python)

- Production code: `my_list_cache.py`
- Test runner (kept separate): `test_runner.py`
- Shared fixture and specification: `../cases.tsv`, `../spec.md`
- Runtime / compiler: Python 3.12.10

## Run (working folder: this folder)
```
python -B test_runner.py ../cases.tsv
```
The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;
exit code 0 only when all cases pass. Raw output of the recorded run: `test_result.log`.

## Result recorded in Part3/llm/pattern_crosslanguage.csv
- test result: **9/9**, median process time 85.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 28; max function CC: 2

## Language notes
dict + callable loader; 'if key not in cache' miss test; functools.lru_cache would give read-through for pure functions but has no per-key invalidation. Max-CC function: fetch.
