"""Test runner: python test_runner.py ../cases.tsv"""
import asyncio
import sys

from scatter_gather import Row, fetch_rows, sequential_cost


def run(text: str) -> str:
    rows = []
    for item in ([] if text == "-" else text.split(",")):
        key, ms, status, count = item.split(":")
        rows.append(Row(key, int(ms), status == "ok", int(count)))
    out = asyncio.run(fetch_rows(rows, "Failed to fetch shows"))
    if "error" in out:
        head = "ERROR:" + out["error"]
    else:
        head = ",".join(f"{k}={v}" for k, v in out["rows"].items()) or "none"
    return f"{head};elapsed={out['elapsed']};sequential={sequential_cost(rows)}"


def main(path: str) -> int:
    passed = total = 0
    for line in open(path, encoding="utf-8"):
        if not line.strip():
            continue
        cid, inp, expected = line.rstrip("\n").split("\t")
        got = run(inp)
        total += 1
        if got == expected:
            passed += 1
        else:
            print(f"FAIL {cid} expected={expected} got={got}")
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
