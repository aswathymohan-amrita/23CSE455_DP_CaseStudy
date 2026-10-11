#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
(cd "$ROOT/java" && javac Patterns.java TestMain.java && java TestMain)
(cd "$ROOT/python" && python3 test_main.py)
(cd "$ROOT/javascript" && node test_main.js)
(cd "$ROOT/cpp" && g++ -std=c++20 -O2 test_main.cpp -o /tmp/design-pattern-case-study-cpp-test && /tmp/design-pattern-case-study-cpp-test)
