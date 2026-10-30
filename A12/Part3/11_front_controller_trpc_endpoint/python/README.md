# Front Controller - tRPC API Front Controller (Python)

- Production code: `front_controller.py`
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
- test result: **14/14**, median process time 48.3 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 49; max function CC: 9

## Language notes
Registry is a plain dict of Procedure objects with lambdas; one try/except separates expected TRPCError from unexpected exceptions; context factory and onError are just callables. Max-CC function: _dispatch.
