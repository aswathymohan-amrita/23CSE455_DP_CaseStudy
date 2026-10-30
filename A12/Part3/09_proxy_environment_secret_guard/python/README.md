# Proxy - Environment Secret Guard (Python)

- Production code: `env_guard.py`
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
- test result: **10/10**, median process time 41.8 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 11; max function CC: 4

## Language notes
__getattr__ on a wrapper class intercepts attribute reads (env.STRIPE_API_KEY), the closest analogue of a property trap; object.__getattribute__ reaches the real data. Max-CC function: __getattr__.
