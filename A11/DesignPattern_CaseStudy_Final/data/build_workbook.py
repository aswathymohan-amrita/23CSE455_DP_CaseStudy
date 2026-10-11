#!/usr/bin/env python3
"""Build a flat-XML workbook source from canonical CSVs and preserved references.
Run this script, then convert the emitted FODS with LibreOffice as documented in data/README.md.
"""
from pathlib import Path
import csv
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "A11_Dataset.xlsx"
OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
ET.register_namespace("office", OFFICE)
ET.register_namespace("table", TABLE)
ET.register_namespace("text", TEXT)

def read_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))

def read_xlsx_sheets(name, prefix):
    """Read each original sheet as displayed values, retaining all populated cells."""
    path = ROOT / name
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    office_rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package_rel = "http://schemas.openxmlformats.org/package/2006/relationships"
    ns = {"m": main, "p": package_rel}
    with zipfile.ZipFile(path) as z:
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        relationships = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in relationships.findall("p:Relationship", ns)}
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            strings = ["".join(t.text or "" for t in si.findall(".//m:t", ns)) for si in root.findall("m:si", ns)]
        result = []
        for sheet in workbook.findall(".//m:sheet", ns):
            target = targets[sheet.attrib[f"{{{office_rel}}}id"]]
            sheet_path = target.lstrip("/") if target.startswith("/") else "xl/" + target
            root = ET.fromstring(z.read(sheet_path))
            rows = []
            for row_el in root.findall(".//m:sheetData/m:row", ns):
                cells = {}
                for cell in row_el.findall("m:c", ns):
                    ref = cell.attrib.get("r", "A1")
                    letters = "".join(ch for ch in ref if ch.isalpha())
                    col = 0
                    for ch in letters.upper():
                        col = col * 26 + ord(ch) - 64
                    val = cell.find("m:v", ns)
                    inline = cell.find("m:is", ns)
                    value = ""
                    if val is not None:
                        value = val.text or ""
                        if cell.attrib.get("t") == "s":
                            value = strings[int(value)]
                    elif inline is not None:
                        value = "".join(t.text or "" for t in inline.findall(".//m:t", ns))
                    cells[col] = value
                if cells:
                    line = [""] * max(cells)
                    for col, value in cells.items():
                        line[col - 1] = value
                    rows.append(line)
            source_name = sheet.attrib["name"]
            if not prefix:
                source_name = {
                    "Member_Contributions": "Dataset_Index",
                    "M1_A8_Member_Stats": "A8_Report_Statistics",
                    "M1_Source_Manifest": "A8_Source_Manifest",
                    "M2_Evidence": "B12_Source_Evidence",
                    "M2_Verdicts": "B12_Source_Verdicts",
                    "M4_Evidence": "LMS_FIU_Source_Evidence",
                    "M4_Verdicts": "LMS_FIU_Source_Verdicts",
                }.get(source_name, re.sub(r"^M1_A8_", "A8_Source_", source_name))
            tab = prefix + re.sub(r"[^A-Za-z0-9_]", "_", source_name)
            result.append((tab[:31], rows))
        return result

data = [
    ("Summary", [
        ["A11 Design Pattern Case Study — consolidated dataset"],
        ["Baseline source", "https://github.com/dinhbachnguyen/E-Learning-App"],
        ["Baseline inventory", "One confirmed Authentication State Updates Observer collaboration"],
        ["After Change 1", "One Observer collaboration"],
        ["After Change 2", "One Observer and one Strategy collaboration"],
        ["After Change 3", "Two Observer collaborations and one Strategy collaboration"],
        ["Contributor materials", "Separate LMS analyses are grouped in contribution folders by data type; see Dataset_Index for coverage and attribution."],
        ["Contributor CSV format", "Records are grouped by generic data heading and carry source metadata where it is available."],
        ["Independent project findings", "A8, LMS-FIU and unattributed B12 results are separate from A11 E-Learning-App totals."],
        ["Source boundary", "Other-project analyses are not counted as evidence or pattern instances in the A11 source inventory"],
        ["Prompt boundary", "Prompts are verbatim only where explicit source text is supplied; see Prompt_Register"],
        ["Workbook generation", "Generated from canonical CSVs by data/build_workbook.py"],
    ]),
    ("A11_Patterns", read_csv("patterns.csv")),
    ("Pattern_Counts", read_csv("pattern_counts.csv")),
    ("Pattern_Evolution", read_csv("pattern_evolution.csv")),
    ("Cross_Language", read_csv("cross_language.csv")),
    ("LLM_Records", read_csv("llm.csv")),
    ("Prompt_Register", read_csv("prompt_register.csv")),
    ("Dataset_Index", read_csv("contributions/Dataset Index/index.csv")),
    ("Contributor_Patterns", read_csv("contributions/Pattern Inventory/patterns.csv")),
    ("Contributor_Counts", read_csv("contributions/Pattern Counts/counts.csv")),
    ("Contributor_Statistics", read_csv("contributions/Pattern Statistics/statistics.csv")),
    ("Contributor_Evolution", read_csv("contributions/Pattern Evolution/evolution.csv")),
    ("Contributor_Cross_Language", read_csv("contributions/Cross Language Results/results.csv")),
    ("Contributor_LLM", read_csv("contributions/LLM Records/records.csv")),
    ("Contributor_Evidence", read_csv("contributions/Evidence Register/records.csv")),
    ("Contributor_Verdicts", read_csv("contributions/Pattern Verdicts/verdicts.csv")),
]
manifest = ROOT / "contributions/Source Manifests/manifest.csv"
if manifest.exists():
    data.append(("Contributor_Manifest", read_csv("contributions/Source Manifests/manifest.csv")))

# Retain every original workbook data sheet while replacing current A11 and generic
# contributor tabs with the reorganized CSV datasets. Other imported study sheets
# remain as source records and are relabelled by project rather than member number.
current_names = {name for name, _ in data}
archived = read_xlsx_sheets("A11_Dataset.xlsx", "")
data.extend((name, rows) for name, rows in archived if name not in current_names)

document = ET.Element(f"{{{OFFICE}}}document", {f"{{{OFFICE}}}mimetype": "application/vnd.oasis.opendocument.spreadsheet", f"{{{OFFICE}}}version": "1.3"})
spreadsheet = ET.SubElement(ET.SubElement(document, f"{{{OFFICE}}}body"), f"{{{OFFICE}}}spreadsheet")
for sheet_name, rows in data:
    table = ET.SubElement(spreadsheet, f"{{{TABLE}}}table", {f"{{{TABLE}}}name": sheet_name})
    for row in rows:
        row_el = ET.SubElement(table, f"{{{TABLE}}}table-row")
        for value in row:
            cell = ET.SubElement(row_el, f"{{{TABLE}}}table-cell", {f"{{{OFFICE}}}value-type": "string"})
            ET.SubElement(cell, f"{{{TEXT}}}p").text = str(value)

# Emit the full ODS-compatible flat XML document; conversion is invoked separately so
# LibreOffice failures are visible and the existing workbook is preserved until replacement.
OUTDIR = Path("/tmp/a11-workbook-fods")
OUTDIR.mkdir(parents=True, exist_ok=True)
ods = OUTDIR / "A11_Dataset.fods"
ods.write_bytes(ET.tostring(document, encoding="utf-8", xml_declaration=True))
print(ods)
