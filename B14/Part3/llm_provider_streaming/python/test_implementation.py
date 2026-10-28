"""Check the saved Strategy examples."""

import json
import sys
from pathlib import Path

from implementation import run


def main() -> int:
    fixtures = Path(__file__).resolve().parents[1] / "fixtures.json"
    cases = json.loads(fixtures.read_text(encoding="utf-8"))
    passed = 0
    for case in cases:
        before = json.dumps(case["input"])
        actual = run(case["input"])
        if actual == case["expected"] and json.dumps(case["input"]) == before:
            passed += 1
            print(f"PASS {case['name']}")
        else:
            print(f"FAIL {case['name']}: expected {case['expected']!r}; got {actual!r}")
    print(f"{passed}/{len(cases)} cases passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
