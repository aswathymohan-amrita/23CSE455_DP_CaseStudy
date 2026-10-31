"""Time each example program once for warm-up and five more times."""

from __future__ import annotations

import json
import platform
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path


BASE = Path(__file__).resolve().parent
NODE = shutil.which("node")
if NODE is None:
    raise SystemExit("node executable not found")


def measure(pattern: str, language: str, executable: str, file_name: str) -> dict:
    workdir = BASE / pattern / language
    input_file = BASE / pattern / "benchmark_input.json"
    command = [executable, str(workdir / file_name), str(input_file)]
    observations: list[float] = []
    outputs: list[dict] = []
    for run_index in range(6):
        start = time.perf_counter_ns()
        result = subprocess.run(command, cwd=workdir, capture_output=True, text=True, check=True)
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        outputs.append(json.loads(result.stdout))
        if run_index > 0:
            observations.append(round(elapsed_ms, 3))
    if any(output != outputs[0] for output in outputs):
        raise RuntimeError(f"outputs changed between runs: {pattern}/{language}")
    return {
        "pattern": pattern,
        "language": language,
        "command": command,
        "input_file": str(input_file.relative_to(BASE)),
        "boundary": "whole process, including startup and JSON input reading; excludes compilation",
        "warmup_count": 1,
        "measured_ms": observations,
        "median_process_ms": round(statistics.median(observations), 3),
        "output": outputs[0],
    }


def main() -> None:
    measurements = [
        measure("llm_provider_streaming", "python", sys.executable, "implementation.py"),
        measure("llm_provider_streaming", "javascript", NODE, "implementation.mjs"),
        measure("auth_state_observer", "python", sys.executable, "implementation.py"),
        measure("auth_state_observer", "javascript", NODE, "implementation.mjs"),
    ]
    record = {
        "machine": platform.platform(),
        "python": platform.python_version(),
        "node": subprocess.run([NODE, "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "measurements": measurements,
    }
    target = BASE / "evidence" / "timings" / "process_timings.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    for item in measurements:
        print(f"{item['pattern']} {item['language']}: {item['median_process_ms']:.3f} ms")


if __name__ == "__main__":
    main()
