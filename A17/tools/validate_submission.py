"""Check the self-contained A17 evidence package before it is uploaded."""

import csv
import json
import re
from pathlib import Path

import openpyxl


team = Path(__file__).resolve().parents[1]
data = team / "data"
expected = {
    "patterns.csv": ("Patterns", 5),
    "pattern_counts.csv": ("Counts", 28),
    "patterns_evolution.csv": ("Evolution", 22),
    "evolution_metrics.csv": ("Metrics", 4),
    "cross_language.csv": ("Cross language", 20),
    "llm.csv": ("LLM record", 3),
    "human_verification.csv": ("Human review", 3),
}
workbook = openpyxl.load_workbook(data / "A17_Dataset.xlsx", read_only=True, data_only=True)
assert workbook.sheetnames == ["Overview", *(name for name, _ in expected.values())]
for filename, (sheetname, count) in expected.items():
    with (data / filename).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream))
    assert len(rows) == count + 1, filename
    sheet_rows = list(workbook[sheetname].values)
    assert len(sheet_rows) == len(rows), filename
    for csv_row, excel_row in zip(rows, sheet_rows):
        values = tuple("" if value is None else str(value) for value in excel_row[: len(csv_row)])
        assert tuple(csv_row) == values, filename
    print(f"PASS {filename}: {count} records, workbook matches")

locations = 0
for filename in ("patterns.csv", "patterns_evolution.csv"):
    with (data / filename).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            for field in row["source_locations"].split("; "):
                location = field.split(" = ", 1)[-1]
                match = re.fullmatch(r"(.+):(\d+)-(\d+)", location)
                assert match, location
                source = team / match[1]
                assert source.is_file(), source
                end = len(source.read_text(encoding="utf-8", errors="replace").splitlines())
                assert 1 <= int(match[2]) <= int(match[3]) <= end, location
                locations += 1
print(f"PASS {locations} participant source locations exist and have valid line ranges")

with (data / "llm.csv").open(newline="", encoding="utf-8") as stream:
    for row in csv.DictReader(stream):
        for field in ("prompt_file", "input_file", "output_file", "verification_file"):
            assert (team / row[field]).is_file(), row[field]
print("PASS LLM paths resolve")

snapshots = json.loads((team / "Part2/evidence/snapshots.json").read_text())
assert [stage["result"] for stage in snapshots] == ["RESULT 3/3", "RESULT 11/11", "RESULT 15/15", "RESULT 20/20"]
upstream = json.loads((team / "Part2/evidence/upstream/summary.json").read_text())
assert len(upstream) == 2 and upstream[0]["failure_names"] == upstream[1]["failure_names"]
assert all((run["tests"], run["passed"], run["failures"], run["skipped"]) == (3191, 3177, 2, 12) for run in upstream)
language = json.loads((team / "Part3/evidence/results.json").read_text())
assert set(language) == {"Java", "Python", "JavaScript", "C++"}
for name, result in language.items():
    assert result["passed"] == 16 and result["total"] == 16, name
print("PASS saved integration, upstream and four-language test summaries")

for item in ("A17_Report.pdf", "A17_Report.tex", "Part3/A17_slide.pdf", "README.md", "HUMAN_VERIFICATION.md"):
    assert (team / item).is_file(), item
assert (team / "A17_Report.pdf").read_bytes().startswith(b"%PDF")
assert (team / "Part3/A17_slide.pdf").read_bytes().startswith(b"%PDF")
print("PASS report, slide deck and editable sources exist")

for path in team.rglob("*"):
    assert not path.is_symlink(), path
    assert path.suffix not in {".jar", ".class", ".pyc"}, path
print("PASS no local symlinks, JARs, class files or Python bytecode")
