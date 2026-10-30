# Chain of Responsibility - Content Access Rule Chain (Python)

- Production code: `content_access.py`
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
- test result: **16/16**, median process time 100.7 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 68; max function CC: 5

## Language notes
ABC + @abstractmethod enforces evaluate(); frozen dataclasses; set intersection (show.genres & blocked) replaces the loop; links are checked only at run time. Max-CC function: evaluate.
