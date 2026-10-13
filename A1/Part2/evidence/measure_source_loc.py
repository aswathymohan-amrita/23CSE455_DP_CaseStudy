from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
VERSIONS = {
    "Baseline": ROOT / "A1/Part2/baseline",
    "Evolved (CH01-CH03)": ROOT / "A1/Part2/code",
}
SUBDIRS = ("app", "config", "db/migrate")

def measure(root):
    files = set()
    for subdir in SUBDIRS:
        folder = root / subdir
        if folder.exists():
            files.update(folder.rglob("*.rb"))

    physical = 0
    nonblank_non_hash_comment = 0
    for path in sorted(files):
        lines = path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        physical += len(lines)
        nonblank_non_hash_comment += sum(
            1 for line in lines
            if line.strip() and not line.lstrip().startswith("#")
        )
    return len(files), physical, nonblank_non_hash_comment

print("Scope: app/**/*.rb, config/**/*.rb, db/migrate/**/*.rb")
print("Excluded: tests, documentation, dependencies, generated files")
print("Physical lines include blanks and comments.")
print("Nonblank/non-#-comment lines exclude blank and # comment-only lines.")
print("Inline comments and other comment forms may still be counted.")
print(f"Python: {sys.version.split()[0]}\n")

results = {}
for name, root in VERSIONS.items():
    if not root.is_dir():
        raise SystemExit(f"ERROR: snapshot missing: {root}")
    results[name] = measure(root)
    files, physical, code_proxy = results[name]
    print(name)
    print(f"  Ruby files: {files}")
    print(f"  Physical lines: {physical}")
    print(f"  Nonblank/non-#-comment lines: {code_proxy}")

b = results["Baseline"]
e = results["Evolved (CH01-CH03)"]
print("\nEvolved minus baseline")
print(f"  Ruby files: {e[0] - b[0]:+}")
print(f"  Physical lines: {e[1] - b[1]:+}")
print(f"  Nonblank/non-#-comment lines: {e[2] - b[2]:+}")
