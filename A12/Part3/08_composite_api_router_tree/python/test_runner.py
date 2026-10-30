"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from router_tree import Procedure, app_router


def run(text: str) -> str:
    root = app_router()
    op, _, arg = text.partition(" ")
    if op == "depth":
        return str(root.depth())
    node = root.resolve(arg.split(".")) if arg else root
    if node is None:
        return "NOT_FOUND"
    if op == "count":
        return str(node.count())
    if op == "paths":
        return ",".join(node.paths(arg))
    return node.kind if isinstance(node, Procedure) else f"router({node.count()})"


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
