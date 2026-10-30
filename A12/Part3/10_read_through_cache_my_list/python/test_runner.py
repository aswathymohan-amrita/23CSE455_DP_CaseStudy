"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from my_list_cache import MyListStore, QueryCache


def run(text: str) -> str:
    cache, store, out = QueryCache(), MyListStore(), []
    for cmd in text.split(";"):
        p = cmd.split(" ")
        try:
            if p[0] == "get":
                ids = cache.fetch(p[1], lambda: store.get_all(p[1]))
                out.append(f"{p[1]}=[{','.join(map(str, ids))}]")
            elif p[0] == "add":
                store.add(p[1], int(p[2]))
            elif p[0] == "remove":
                store.remove(p[1], int(p[2]))
            else:
                cache.invalidate(p[1])
        except LookupError as e:
            out.append(f"ERROR:{e.args[0]}")
    out.append(f"loads={store.loads}")
    return "|".join(out)


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
