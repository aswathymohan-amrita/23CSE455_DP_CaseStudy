# Error Boundary - Shows Segment Error Boundary (Python)

- Production code: `error_boundary.py`
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
- test result: **10/10**, median process time 58.1 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 41; max function CC: 3

## Language notes
Boundary catches RenderError only, so errors from its own fallback propagate naturally; components are small classes with a render() method. Max-CC function: render.
