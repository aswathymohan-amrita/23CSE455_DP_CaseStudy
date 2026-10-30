# Observer - Active Profile Selection (Python)

- Production code: `profile_selection.py`
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
- test result: **11/11**, median process time 82.8 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 30; max function CC: 3

## Language notes
Protocol-free duck typing: any object with notify(); dict-as-ordered-set (dict.fromkeys) keeps order and uniqueness; observers are small classes. Max-CC function: set_state.
