"""Run each recorded source snapshot against the official baseline runtime."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("baseline_jar", type=Path)
parser.add_argument("build_dir", type=Path)
args = parser.parse_args()
team = Path(__file__).resolve().parents[1]
jar = args.baseline_jar.resolve()
build = args.build_dir.resolve()
revisions = json.loads((team / "Part2/evidence/snapshots.json").read_text())
manifest = []
for stage, snapshot in enumerate(revisions):
    commit = snapshot["commit"]
    dest = build / str(stage)
    dest.mkdir(parents=True, exist_ok=True)
    evidence = team / "Part2" / "evidence" / ("baseline" if stage == 0 else f"CH0{stage}")
    evidence.mkdir(parents=True, exist_ok=True)
    saved = team / f"Part2/changes/Change{stage}/source"
    files = [p.relative_to(saved) for p in saved.rglob('*.java')] if stage else []
    extracted = []
    for file in files:
        extracted.append(str(saved / file))
    classes = dest / "classes"
    classes.mkdir(exist_ok=True)
    with (evidence / "compile.log").open("w") as log:
        if extracted:
            subprocess.run(["javac", "--release", "11", "-cp", str(jar), "-d", str(classes), *extracted], stdout=log, stderr=subprocess.STDOUT, check=True)
    manifest.append({"stage": stage, "commit": commit, "changed_java_files": len(files)})

# Compile the test once using the final API; execute against each snapshot.
testclasses = build / "tests"
testclasses.mkdir(exist_ok=True)
subprocess.run(["javac", "-cp", f"{build / '3/classes'}:{jar}", "-d", str(testclasses), str(team / "Part2/tests/EvolutionTest.java")], check=True)
for row in manifest:
    stage = row["stage"]
    evidence = team / "Part2/evidence" / ("baseline" if stage == 0 else f"CH0{stage}")
    command = ["java", "-Djava.awt.headless=true", "-cp", f"{testclasses}:{build / str(stage) / 'classes'}:{jar}", "EvolutionTest", str(stage), str(evidence)]
    result = subprocess.run(command, text=True, capture_output=True)
    (evidence / "tests.log").write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"Stage {stage} failed; see {evidence}")
    row["result"] = result.stdout.strip().splitlines()[-1]
    print(stage, row["result"])
(team / "Part2/evidence/snapshots.json").write_text(json.dumps(manifest, indent=2))
