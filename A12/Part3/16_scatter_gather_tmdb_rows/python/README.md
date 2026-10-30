# Scatter-Gather - TMDB Row Scatter-Gather (Python)

- Production code: `scatter_gather.py`
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
- test result: **8/8**, median process time 267.9 ms (Windows 11 AMD64)
- source LOC (lizard NLOC, production files only): 15; max function CC: 6

## Language notes
asyncio.gather is the direct analogue of Promise.all and preserves argument order; the latency is simulated so the result is deterministic. Max-CC function: fetch_rows.
