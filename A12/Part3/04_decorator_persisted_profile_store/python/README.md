# Decorator - Persisted Profile Store (Python)

- Production code: `profile_stores.py`
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
- test result: **11/11**, median process time 44.6 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 37; max function CC: 2

## Language notes
Forwarding base class; decorators override only what they add; could also use __getattr__ delegation, kept explicit for parity. Max-CC function: set.
