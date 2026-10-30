# Builder - tRPC Procedure Builder (Python)

- Production code: `procedure_builder.py`
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
- test result: **14/14**, median process time 48.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 66; max function CC: 5

## Language notes
Tuples make the middleware list immutable; each method returns a new ProcedureBuilder; duck typing lets build() tell builder from product with isinstance. Max-CC function: build.
