"""Test runner: python test_runner.py ../cases.tsv"""
import sys

from procedure_builder import TRPCError, build, no_op, protected_procedure, public_procedure


def run(text: str) -> str:
    chain, user, raw = text.split(";")
    if chain == "immutable":
        subscribed = protected_procedure.use("plan", no_op)
        return (f"base={len(public_procedure.middlewares)};protected={len(protected_procedure.middlewares)};"
                f"subscribed={len(subscribed.middlewares)}")
    try:
        proc = build(chain.split(","))
    except TRPCError as e:
        return "ERROR:" + e.code
    try:
        result, trace = proc.call(None if user == "-" else user, None if raw == "-" else raw)
    except TRPCError as e:
        return f"ERROR:{e.code};trace={'>'.join(e.trace)}"
    return f"{result};trace={'>'.join(trace) or 'none'}"


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
