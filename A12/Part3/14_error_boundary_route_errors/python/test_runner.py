"""Test runner: python test_runner.py ../cases.tsv"""
import sys

from error_boundary import build_app, reset_nearest


def run(text: str) -> str:
    setup, *actions = text.split(";")
    fails = {} if setup == "none" else {k: int(v) for k, v in (p.split(":") for p in setup.split(","))}
    root, shows = build_app(fails)
    frames = [root.render()]
    for action in actions:
        if action == "reset" and reset_nearest(root, shows):
            frames.append(root.render())
    return " > ".join(frames)


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
