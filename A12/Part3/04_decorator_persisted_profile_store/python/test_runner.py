"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from profile_stores import BasicStore, DevtoolsDecorator, PersistDecorator


def run(text: str) -> str:
    decorators, ops = text.split(";")
    storage: dict = {}
    log: list = []
    try:
        store = BasicStore()
        for name in [] if decorators == "none" else decorators.split("+"):
            if name == "persist":
                store = PersistDecorator(store, storage)
            elif name == "devtools":
                store = DevtoolsDecorator(store, log)
            else:
                raise ValueError(f"unknown decorator {name}")
        for op in [] if ops == "-" else ops.split(","):
            if op == "clear":
                store.clear_storage()
            else:
                store.set(*op.split("="))
    except ValueError as e:
        return f"ERROR:{e}"
    return f"state={store.state()};storage={storage.get('test-store', '-')};log={','.join(log) or '-'}"


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
