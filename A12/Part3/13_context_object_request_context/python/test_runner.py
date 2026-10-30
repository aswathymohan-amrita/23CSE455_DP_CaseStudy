"""Test runner: python test_runner.py ../cases.tsv"""
import sys

from request_context import TRPCError, call, create_context, create_inner_context


def run(text: str) -> str:
    request, name = text.split("|")
    if request.startswith("inner:"):
        _, user, region = request.split(":")
        ctx = create_inner_context(None if user == "-" else user, None if region == "-" else region)
    else:
        headers = {} if request == "-" else dict(pair.split("=", 1) for pair in request.split(","))
        ctx = create_context(headers)
    try:
        return call(name, ctx)
    except TRPCError as e:
        return "ERROR:" + e.code


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
