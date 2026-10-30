"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from env_guard import EnvGuard

VARS = {
    "DATABASE_URL": "mysql://db",
    "STRIPE_API_KEY": "sk_test_123",
    "NEXT_PUBLIC_TMDB_API_KEY": "tmdb_abc",
    "NEXT_PUBLIC_APP_URL": "http://localhost:3000",
}


def run(text: str) -> str:
    side, name = text.split(";")
    env = EnvGuard(VARS, side == "server", side == "client-prod")
    try:
        value = getattr(env, name)
    except PermissionError as e:
        return f"ERROR:{e}"
    return "undefined" if value is None else value


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
