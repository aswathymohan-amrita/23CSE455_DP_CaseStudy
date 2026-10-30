# Adapter - NextAuth Prisma Persistence Adapter (Python)

- Production code: `auth_adapters.py`
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
- test result: **9/9**, median process time 46.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 37; max function CC: 3

## Language notes
Object adapter with plain dicts as the ORM's data/where arguments; returning None for 'no user'; duck typing means the Target is only a convention (could add typing.Protocol). Max-CC function: find_unique.
