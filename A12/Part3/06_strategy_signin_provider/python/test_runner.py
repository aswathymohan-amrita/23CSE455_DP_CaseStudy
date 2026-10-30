"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from sign_in import NextAuth


def run(text: str) -> str:
    providers, pid, credential = text.split(";")
    try:
        return NextAuth(providers.split(",")).sign_in(pid, credential)
    except ValueError as e:
        return f"ERROR:{e}"


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
