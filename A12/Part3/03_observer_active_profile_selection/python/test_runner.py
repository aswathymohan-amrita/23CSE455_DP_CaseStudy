"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from profile_selection import Hero, PinForm, ProfileStore, ShowsContainer, State


def run(text: str) -> str:
    store = ProfileStore()
    views = {"Hero": Hero(), "ShowsContainer": ShowsContainer(), "PinForm": PinForm()}
    out: list[str] = []
    for cmd in text.split(";"):
        op, _, arg = cmd.partition(" ")
        if op in ("sub", "unsub"):
            if arg not in views:
                return "ERROR:unknown observer"
            (store.subscribe if op == "sub" else store.unsubscribe)(views[arg])
        elif op == "select":
            s = arg.split(":")
            store.set_state(State(s[0], s[1], len(s) > 2), out)
        else:
            store.set_state(State(), out)
    return "|".join(out) or "-"


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
