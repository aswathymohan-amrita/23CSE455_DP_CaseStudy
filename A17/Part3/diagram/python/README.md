# Python miniature

Production: `diagram.py`. Runner: `runner.py`. Recorded runtime: Python 3.14.2.
The standard library supplies `abc` and `json`; no package install is required.

From `A17/`:

```bash
printf 'class A\nclass B\nlink A B\n' | python3 Part3/diagram/python/runner.py compact
python3 Part3/run_tests.py
```

Expected compact output: `A,B|A->B`. Other modes: `bracketed` and `json`.
Abstract base classes make the intended contracts explicit; method dispatch
is still dynamic.
