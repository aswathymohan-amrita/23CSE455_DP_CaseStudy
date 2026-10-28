"""Measure code lines and complexity in the four example programs."""

from __future__ import annotations

import json
from pathlib import Path

import lizard


BASE = Path(__file__).resolve().parent
FILES = [
    "llm_provider_streaming/python/implementation.py",
    "llm_provider_streaming/javascript/implementation.mjs",
    "auth_state_observer/python/implementation.py",
    "auth_state_observer/javascript/implementation.mjs",
]


def main() -> None:
    results = []
    for name in FILES:
        analysis = lizard.analyze_file(str(BASE / name))
        results.append({
            "file": name,
            "source_loc": analysis.nloc,
            "max_function_cc": max(item.cyclomatic_complexity for item in analysis.function_list),
            "functions": [
                {"name": item.name, "cc": item.cyclomatic_complexity}
                for item in analysis.function_list
            ],
        })
    target = BASE / "evidence" / "static_metrics.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for result in results:
        print(f"{result['file']}: LOC {result['source_loc']}, max CC {result['max_function_cc']}")


if __name__ == "__main__":
    main()
