"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from content_access import Show, Viewer, content_access_chain


def run(text: str) -> str:
    f = text.split(";")
    genres = frozenset() if f[3] == "-" else frozenset(int(g) for g in f[3].split(","))
    show = Show(int(f[0]), f[1] == "1", f[2] == "1", genres)
    viewer = Viewer(int(f[4]), f[5], f[6])
    try:
        return str(content_access_chain().check(show, viewer))
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
