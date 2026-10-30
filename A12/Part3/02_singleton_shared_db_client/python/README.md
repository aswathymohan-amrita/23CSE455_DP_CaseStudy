# Singleton - Shared Prisma Database Client (Python)

- Production code: `shared_db_client.py`
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
- test result: **9/9**, median process time 39.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 15; max function CC: 4

## Language notes
Module-level objects are already singletons via the import cache; the holder mirrors globalThis with a plain object; 'or' expresses ??. Max-CC function: __init__.
