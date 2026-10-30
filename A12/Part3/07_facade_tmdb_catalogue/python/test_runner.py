"""Test runner: python3 test_runner.py ../cases.tsv"""
import sys

from tmdb_catalogue import TmdbCatalogue


class FakeHttp:
    """Test double: request n answers [n]; fails when the URL contains the fragment."""

    def __init__(self, fail: str) -> None:
        self.fail = fail
        self.requests = 0

    def get(self, url: str):
        self.requests += 1
        return (self.fail == "-" or self.fail not in url), [self.requests]


def run(text: str) -> str:
    mode, fail = text.split(";", 1)
    http = FakeHttp(fail)
    facade = TmdbCatalogue(http, "k")
    try:
        rows = facade.get_new_and_popular() if mode == "newpopular" else facade.get_shows(mode)
    except (ValueError, RuntimeError) as e:
        return f"ERROR:{e};requests={http.requests}"
    parts = [f"{k}={v[0][0]}{'P' if v[0][1] else ''}" for k, v in rows.items()]
    return ",".join(parts) + f";requests={http.requests}"


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
