import hashlib
import json
from pathlib import Path
import sys

root = Path.cwd()
manifest_path = root / "A1/Part2/evidence/snapshots/source_snapshot_manifest.json"

if not manifest_path.is_file():
    raise SystemExit("FAIL: snapshot manifest not found.")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
errors = []

for name, snapshot in manifest["snapshots"].items():
    folder = root / snapshot["folder"]
    entries = snapshot["files"]
    print(f"{name}: checking {len(entries)} files")

    if not folder.is_dir():
        errors.append(f"{name}: snapshot directory missing")
        continue

    for entry in entries:
        path = folder / entry["path"]

        if not path.is_file():
            errors.append(f"{name}: missing {entry['path']}")
            continue

        data = path.read_bytes()
        if len(data) != entry["size_bytes"]:
            errors.append(f"{name}: size mismatch {entry['path']}")
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            errors.append(f"{name}: SHA-256 mismatch {entry['path']}")

if errors:
    print("FAIL: snapshot verification found problems:")
    print("\n".join(errors[:30]))
    sys.exit(1)

print("PASS: all manifest-listed files match their recorded sizes and SHA-256 hashes.")

patch = root / "A1/Part2/evidence/snapshots/baseline_to_final_source.patch"
provenance = root / "A1/Part2/evidence/snapshots/source_provenance.txt"

if not patch.is_file() or patch.stat().st_size == 0:
    raise SystemExit("FAIL: baseline-to-final patch missing or empty.")
if not provenance.is_file():
    raise SystemExit("FAIL: source provenance note missing.")

print(f"PASS: baseline-to-final patch exists ({patch.stat().st_size} bytes).")
print("PASS: source provenance note exists.")
print("LIMITATION: this does not establish intermediate CH01/CH02 source states.")
