"""Test runner: python test_runner.py ../cases.tsv"""
import sys

from front_controller import FrontController, app_router


def run(text: str) -> str:
    user, path = text.split(" ")
    counters = {"ctx": 0, "logged": 0}

    def create_context(u):
        counters["ctx"] += 1
        return {"user": u, "db": "prisma"}

    def on_error(_path, _code):
        counters["logged"] += 1

    controller = FrontController(app_router(), create_context, on_error)
    results = controller.handle(None if user == "-" else user, None if path == "-" else path)
    return f"{'|'.join(results)};ctx={counters['ctx']};logged={counters['logged']}"


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
