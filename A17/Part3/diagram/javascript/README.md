# JavaScript miniature

Production: `diagram.mjs`. Runner: `runner.mjs`. Recorded runtime: Node.js
22.19.0. This is a standard ECMAScript module and has no external packages.

From `A17/`:

```bash
printf 'class A\nclass B\nlink A B\n' | node Part3/diagram/javascript/runner.mjs compact
python3 Part3/run_tests.py
```

Expected compact output: `A,B|A->B`. Other modes: `bracketed` and `json`.
The base classes state the intended contracts by throwing when an operation
is not overridden. `Map` holds the command registry.
