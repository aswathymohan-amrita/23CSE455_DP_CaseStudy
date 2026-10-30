"""Test runner: python test_runner.py ../cases.tsv"""
import sys

from suspense_boundary import AsyncPage, Dependency, segment, stream


def run(text: str) -> str:
    loading, spec = text.split(" ")
    deps = []
    for item in ([] if spec == "-" else spec.split(",")):
        name, ms = item.split(":")
        deps.append(Dependency(name, int(ms.lstrip("!")), ms.startswith("!")))
    return " | ".join(stream(segment(AsyncPage(deps), loading == "yes"), deps))


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
