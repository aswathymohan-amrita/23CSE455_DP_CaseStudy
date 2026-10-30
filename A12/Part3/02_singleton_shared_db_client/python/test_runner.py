"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from shared_db_client import DbModule, ProcessGlobals


def run(text: str) -> str:
    env, ops = text.split(";")
    process = ProcessGlobals()
    seen = set()
    try:
        module = DbModule(process, env)
        for op in [] if ops == "-" else ops.split(","):
            if op == "reload":
                module = DbModule(process, env)
            else:
                seen.add(id(module.prisma))
    except ValueError as e:
        return f"ERROR:{e}"
    return f"constructed={process.constructed};distinct={len(seen)}"


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
