"""Run the same cases through Python and JavaScript programs."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


BASE = Path(__file__).resolve().parent
NODE = shutil.which("node")
if NODE is None:
    raise SystemExit("node executable not found")


def invoke(executable: str, source: Path, input_file: Path) -> dict:
    completed = subprocess.run(
        [executable, str(source), str(input_file)],
        cwd=source.parent,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    passed = 0
    total = 0
    with tempfile.TemporaryDirectory(prefix="b14-part3-") as temporary:
        input_file = Path(temporary) / "input.json"
        for pattern in ("llm_provider_streaming", "auth_state_observer"):
            pattern_dir = BASE / pattern
            cases = json.loads((pattern_dir / "fixtures.json").read_text(encoding="utf-8"))
            python_source = pattern_dir / "python" / "implementation.py"
            javascript_source = pattern_dir / "javascript" / "implementation.mjs"
            for case in cases:
                total += 1
                input_file.write_text(json.dumps(case["input"]), encoding="utf-8")
                python_output = invoke(sys.executable, python_source, input_file)
                javascript_output = invoke(NODE, javascript_source, input_file)
                if python_output == javascript_output == case["expected"]:
                    passed += 1
                    print(f"PASS {pattern}/{case['name']}")
                else:
                    print(
                        f"FAIL {pattern}/{case['name']}: expected={case['expected']!r} "
                        f"python={python_output!r} javascript={javascript_output!r}"
                    )
    print(f"{passed}/{total} cross-language process cases passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
