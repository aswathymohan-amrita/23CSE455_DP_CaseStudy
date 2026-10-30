"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from auth_adapters import OrmClient, OrmError, PrismaAdapter


def run(text: str) -> str:
    adapter = PrismaAdapter(OrmClient())
    out = []
    for cmd in text.split(";"):
        p = cmd.split(" ")
        try:
            if p[0] == "create":
                out.append(adapter.create_user(p[1], p[2])["id"])
            elif p[0] == "get":
                u = adapter.get_user_by_email(p[1])
                out.append(f"{u['id']}:{u['name']}" if u else "null")
            elif p[0] == "link":
                a = adapter.link_account(p[1], p[2])
                out.append(f"{a['id']}:{a['userId']}:{a['provider']}")
            else:
                out.append("ERROR:unknown operation")
        except OrmError as e:
            out.append(f"ERROR:{e}")
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
