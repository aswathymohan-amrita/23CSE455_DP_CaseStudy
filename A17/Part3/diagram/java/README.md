# Java miniature

Production: `DiagramSystem.java`. Runner: `Runner.java`. Requires Java 17 or
newer for the runner's switch expression; the PlantUML source changes compile
with release 11. In this run the Java runtime was OpenJDK 25.0.2.

From `A17/`:

```bash
mkdir -p /tmp/a17-java
javac -d /tmp/a17-java Part3/diagram/java/DiagramSystem.java Part3/diagram/java/Runner.java
printf 'class A\nclass B\nlink A B\n' | java -cp /tmp/a17-java Runner compact
python3 Part3/run_tests.py
```

Expected compact output: `A,B|A->B`. Other modes: `bracketed` and `json`.
Contracts use interfaces and one abstract Parser creation hook. The parser owns
the command map; the exporter owns a Renderer interface reference.
