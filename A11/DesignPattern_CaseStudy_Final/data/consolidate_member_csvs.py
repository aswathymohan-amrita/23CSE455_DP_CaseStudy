#!/usr/bin/env python3
"""Normalize structured member CSV evidence into submission-wide, type-based datasets.

Raw member CSVs in member_inputs/ are preserved unchanged. The normalized outputs add
member/project provenance and share stable headings. External project findings remain
separate from A11's own baseline datasets.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "member_inputs"
if not RAW.is_dir():
    raise SystemExit("Source member_inputs/ directory is absent; refusing to overwrite normalized contribution datasets.")

META = {
    "member1": ("S N Chandran", "AM.EN.U4EAC23046", "EAC", "hoangsonww/Learning-Management-System-Fullstack (A8)"),
    "member2": ("Navaneeth Aneesh", "AM.EN.U4EAC23039", "EAC", "nchinling/learning_management_system (EduQuest)"),
    "member3": ("Harikrishnan S", "AM.EN.U4EAC23029", "EAC", "dinhbachnguyen/E-Learning-App (A11 baseline)"),
    "member4": ("Niveditha S", "AM.EN.U4EAC23063", "EAC", "pantharev/lms-fiu-fb-client"),
    "member5": ("Abhinav M Nair", "AM.EN.U4EAC23003", "EAC", "dinhbachnguyen/E-Learning-App (A11 baseline)"),
}
BASE = ["contributor_name", "roll_number", "batch", "source_project"]

def read_rows(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def unattributed_meta(project):
    return dict(zip(BASE, ["Not supplied", "Not supplied", "Not supplied", project]))

def write_rows(name, fields, rows):
    destinations = {
        "member_patterns.csv": "Pattern Inventory/patterns.csv",
        "member_pattern_counts.csv": "Pattern Counts/counts.csv",
        "member_pattern_summary.csv": "Pattern Statistics/statistics.csv",
        "member_pattern_evolution.csv": "Pattern Evolution/evolution.csv",
        "member_cross_language.csv": "Cross Language Results/results.csv",
        "member_llm.csv": "LLM Records/records.csv",
        "member_evidence_register.csv": "Evidence Register/records.csv",
        "member_pattern_verdicts.csv": "Pattern Verdicts/verdicts.csv",
        "member_source_manifest.csv": "Source Manifests/manifest.csv",
        "member_csv_index.csv": "Dataset Index/index.csv",
    }
    path = ROOT / "contributions" / destinations.get(name, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    if "source_file" in fields:
        fields = ["source_dataset" if field == "source_file" else field for field in fields]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            values = {}
            for field in fields:
                value = Path(row.get("source_file", "")).name if field == "source_dataset" else row.get(field, "")
                if isinstance(value, str):
                    value = value.replace("member_inputs/member1/patterns.csv and pattern_counts.csv", "the submitted pattern inventory and pattern-count CSVs")
                values[field] = value
            w.writerow(values)

def meta(member):
    name, roll, batch, project = META[member]
    return dict(zip(BASE, [name, roll, batch, project]))

# The available member2 evidence CSV describes B12, not the EduQuest repository
# named in Navaneeth's prompt. Keep those rows separate until attribution is verified.
B12_META = unattributed_meta("anshdev02/lms-microservices (B12)")

# Confirmed/candidate pattern records contributed in member source data.
fields = BASE + ["source_version", "pattern_name", "pattern_type", "instance_name", "participant_roles", "source_locations", "intent_and_evidence", "record_status", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "patterns.csv"):
        rows.append({**meta(member), **item, "record_status": "Member source inventory; not reverified as A11 source", "source_file": f"member_inputs/{member}/patterns.csv"})
write_rows("member_patterns.csv", fields, rows)

# Pattern type counts and aggregate totals share one explicit numeric value field.
fields = BASE + ["source_version", "summary", "pattern_name", "count", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "pattern_counts.csv"):
        rows.append({**meta(member), **item, "source_file": f"member_inputs/{member}/pattern_counts.csv"})
write_rows("member_pattern_counts.csv", fields, rows)

# Detailed totals that don't fit per-pattern count rows (e.g. role appearances and unique symbols).
fields = BASE + ["source_version", "measure", "value", "counting_rule", "source_location", "verification_note", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "pattern_summary.csv"):
        rows.append({**meta(member), **item, "source_file": f"member_inputs/{member}/pattern_summary.csv"})
write_rows("member_pattern_summary.csv", fields, rows)

# Upstream or team evolution records; source provenance stays explicit.
fields = BASE + ["source_version", "pattern_name", "pattern_type", "instance_name", "participant_roles", "source_locations", "intent_and_evidence", "status_after_change", "change_description", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "pattern_evolution.csv"):
        rows.append({**meta(member), **item, "source_file": f"member_inputs/{member}/pattern_evolution.csv"})
write_rows("member_pattern_evolution.csv", fields, rows)

fields = BASE + ["pattern_name", "instance_name", "language", "snippet_path", "source_loc", "max_function_cc", "runtime_compiler", "test_command", "test_result", "median_process_ms", "language_notes", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "cross_language.csv"):
        rows.append({**meta(member), **item, "source_file": f"member_inputs/{member}/cross_language.csv"})
write_rows("member_cross_language.csv", fields, rows)

fields = BASE + ["part", "model_and_date", "prompt_file", "input_file", "output_file", "evaluation", "verification_file", "source_file"]
rows = []
for member in META:
    for item in read_rows(RAW / member / "llm.csv"):
        rows.append({**meta(member), **item, "source_file": f"member_inputs/{member}/llm.csv"})
write_rows("member_llm.csv", fields, rows)

# Different source schemas for evidence registers are mapped to one common schema.
fields = BASE + ["record_id", "claim", "evidence_description", "evidence_type", "status_or_confidence", "source_locator", "limitation", "source_file"]
rows = []
for item in read_rows(RAW / "member2" / "evidence_register.csv"):
    rows.append({**B12_META, "record_id": item.get("ID", ""), "claim": item.get("Claim", ""), "evidence_description": item.get("Evidence summary", ""), "evidence_type": item.get("README section", ""), "status_or_confidence": item.get("Status", ""), "source_locator": item.get("Locator", ""), "limitation": item.get("Limitation", ""), "source_file": "evidence_register.csv"})
for item in read_rows(RAW / "member4" / "evidence_register.csv"):
    rows.append({**meta("member4"), "record_id": item.get("id", ""), "claim": item.get("claim", ""), "evidence_description": item.get("source", ""), "evidence_type": item.get("type", ""), "status_or_confidence": item.get("confidence", ""), "source_locator": item.get("location", ""), "limitation": "", "source_file": "member_inputs/member4/evidence_register.csv"})
write_rows("member_evidence_register.csv", fields, rows)

fields = BASE + ["pattern_name", "area", "verdict", "evidence", "rationale_or_caveat", "source_file"]
rows = []
for item in read_rows(RAW / "member2" / "pattern_verdicts.csv"):
    rows.append({**B12_META, "pattern_name": item.get("Pattern", ""), "area": "", "verdict": item.get("Verdict", ""), "evidence": item.get("Evidence", ""), "rationale_or_caveat": item.get("Caveat", ""), "source_file": "pattern_verdicts.csv"})
for item in read_rows(RAW / "member4" / "pattern_verdicts.csv"):
    rows.append({**meta("member4"), "pattern_name": item.get("pattern", ""), "area": item.get("area", ""), "verdict": item.get("verdict", ""), "evidence": item.get("evidence_ids", ""), "rationale_or_caveat": item.get("reason", ""), "source_file": "member_inputs/member4/pattern_verdicts.csv"})
write_rows("member_pattern_verdicts.csv", fields, rows)

fields = BASE + ["source_path", "commit", "sha256", "source_file"]
rows = []
for item in read_rows(RAW / "member1" / "source_manifest.csv"):
    rows.append({**meta("member1"), **item, "source_file": "member_inputs/member1/source_manifest.csv"})
write_rows("member_source_manifest.csv", fields, rows)

# Inventory what is and is not available instead of synthesizing missing member data.
fields = ["contributor_name", "roll_number", "batch", "source_project", "available_structured_csvs", "normalization_status", "notes"]
rows = [
    {**meta("member1"), "available_structured_csvs": "patterns; pattern_counts; pattern_summary; pattern_evolution; cross_language; llm; source_manifest", "normalization_status": "Included in normalized datasets", "notes": "Identity and statistics transcribed from supplied A8 report; separate from A11 counts."},
    {**meta("member2"), "available_structured_csvs": "None", "normalization_status": "No pattern data synthesized", "notes": "EduQuest prompt is supplied, but no completed source inventory/count CSV or verification report is present."},
    {**meta("member3"), "available_structured_csvs": "None (shared A11 analysis is in Part1/Part2)", "normalization_status": "Shared project findings; no individual CSV attribution", "notes": "Prompt targets the A11 baseline; shared A11 findings are not assigned exclusively to this student."},
    {**meta("member4"), "available_structured_csvs": "evidence_register; pattern_verdicts", "normalization_status": "Included in normalized datasets", "notes": "LMS-FIU records are based on documentation/configuration; no code-level pattern is confirmed."},
    {**meta("member5"), "available_structured_csvs": "None (shared A11 analysis is in Part1/Part2)", "normalization_status": "Shared project findings; no individual CSV attribution", "notes": "Prompt/chat archive targets A11; shared A11 implementation authorship is not recorded."},
    {**B12_META, "available_structured_csvs": "evidence_register; pattern_verdicts", "normalization_status": "Included as unattributed external records", "notes": "B12 repository conflicts with the EduQuest project named in Member 2's prompt; attribution is withheld."},
]
write_rows("member_csv_index.csv", fields, rows)
print("Normalized member datasets written to", ROOT)
