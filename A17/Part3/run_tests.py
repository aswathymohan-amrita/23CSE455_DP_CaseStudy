"""Compile first, check shared fixtures, then warm up and time five processes."""
import json
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

root = Path(__file__).resolve().parent
evidence = root / "evidence"
evidence.mkdir(exist_ok=True)
fixtures = json.loads((root / "test-cases/fixtures.json").read_text())
results = {}
with tempfile.TemporaryDirectory(prefix="a17-cross-") as build:
    subprocess.run(["javac", "-d", build, str(root / "diagram/java/DiagramSystem.java"), str(root / "diagram/java/Runner.java")], check=True)
    subprocess.run(["clang++", "-std=c++17", "-O2", "-Wall", "-Wextra", str(root / "diagram/cpp/runner.cpp"), "-o", build + "/runner"], check=True)
    commands = {
        "Java": ["java", "-cp", build, "Runner"],
        "Python": [sys.executable, str(root / "diagram/python/runner.py")],
        "JavaScript": ["node", str(root / "diagram/javascript/runner.mjs")],
        "C++": [build + "/runner"],
    }
    for language, command in commands.items():
        logs = []
        for case in fixtures:
            result = subprocess.run(command + [case["mode"]], input=case["input"], text=True, capture_output=True, check=True)
            actual = result.stdout.rstrip("\n")
            assert actual == case["expected"], (language, case["name"], actual, case["expected"])
            logs.append(f"PASS {case['name']}: {actual}")
        # Timing is a fresh process on the same three-line fixture, not the whole test suite.
        case = fixtures[2]
        samples = []
        for repeat in range(6):
            start = time.perf_counter_ns()
            result = subprocess.run(command + [case["mode"]], input=case["input"], text=True, capture_output=True, check=True)
            elapsed = (time.perf_counter_ns() - start) / 1e6
            assert result.stdout.strip() == case["expected"]
            if repeat:
                samples.append(elapsed)
        results[language] = {"passed": len(fixtures), "total": len(fixtures), "samples_ms": samples, "median_process_ms": statistics.median(samples)}
        logs.append(f"RESULT {len(fixtures)}/{len(fixtures)}")
        (evidence / (language.replace("+", "p") + ".log")).write_text("\n".join(logs) + "\n")
        print(language, results[language])
(evidence / "results.json").write_text(json.dumps(results, indent=2) + "\n")
