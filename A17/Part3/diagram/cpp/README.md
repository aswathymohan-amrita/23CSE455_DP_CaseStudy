# C++ miniature

Production: `diagram.hpp`. Runner: `runner.cpp`. Recorded compiler: Apple
clang 21.0.0. Requires C++17 and the standard library only.

From `A17/`:

```bash
clang++ -std=c++17 -O2 -Wall -Wextra Part3/diagram/cpp/runner.cpp -o /tmp/a17-cpp
printf 'class A\nclass B\nlink A B\n' | /tmp/a17-cpp compact
python3 Part3/run_tests.py
```

Expected compact output: `A,B|A->B`. Other modes: `bracketed` and `json`.
Groups own their children with `unique_ptr`; the parser's group stack holds
non-owning pointers into that owned tree. The exporter keeps a non-owning
reference to a Renderer that outlives the export call.
