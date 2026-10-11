#!/usr/bin/env python3
"""Reproducible process-level benchmarks. Compilation excluded; startup included."""
from pathlib import Path
import csv
import platform
import statistics
import subprocess
import sys
import time
import lizard

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Part3" / "eight_patterns"
PATTERNS = ("facade", "repository", "adapter", "strategy", "proxy", "observer", "factory_method", "decorator")
LANGUAGES = ("python", "javascript", "java", "cpp")
REPEATS = 5

def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{cmd}: exit {result.returncode}: {result.stdout}\n{result.stderr}")
    return result

def measure(cmd, cwd=None):
    run(cmd, cwd)  # warmup
    samples = []
    for _ in range(REPEATS):
        start = time.perf_counter_ns()
        run(cmd, cwd)
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    return samples

rows = []
for pattern in PATTERNS:
    for language in LANGUAGES:
        folder = BASE / pattern / language
        filename = "Demo.java" if language == "java" else f"{pattern}." + {"python": "py", "javascript": "js", "cpp": "cpp"}[language]
        source = folder / filename
        if language == "java":
            run(["javac", "Demo.java"], cwd=folder)
            command = ["java", "Demo"]
        elif language == "cpp":
            binary = Path("/tmp") / f"a5_benchmark_{pattern}"
            run(["g++", "-std=c++17", "-O2", filename, "-o", str(binary)], cwd=folder)
            command = [str(binary)]
        elif language == "python":
            command = [sys.executable, filename]
        else:
            command = ["node", filename]
        samples = measure(command, cwd=folder)
        loc = sum(bool(line.strip()) and not line.lstrip().startswith(("//", "#", "/*", "*")) for line in source.read_text().splitlines())
        analysis = lizard.analyze_file(str(source))
        max_cc = max((function.cyclomatic_complexity for function in analysis.function_list), default=1)
        rows.append({
            "pattern_name": pattern, "language": language,
            "source_path": str(source.relative_to(ROOT)), "source_loc": loc,
            "median_process_ms": round(statistics.median(samples), 4),
            "raw_process_ms": ";".join(f"{n:.4f}" for n in samples),
            "runtime_host": platform.platform(), "test_result": "PASS",
            "timing_scope": "process_startup_plus_test_compilation_excluded",
            "max_function_cc": max_cc, "complexity_status": "measured_lizard_max_function_cc",
        })
        print(f"{pattern}/{language}: PASS, median {rows[-1]['median_process_ms']} ms")

output = BASE / "measured_results.csv"
with output.open("w", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {output} ({len(rows)} rows)")
