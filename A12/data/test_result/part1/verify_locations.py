"""Check every code/... location cited in a pattern CSV: file exists, lines in range.
Usage (from A12/): python data/test_result/part1/verify_locations.py Part1/patterns.csv"""
import csv, re, sys, os
bad = 0
for row in csv.DictReader(open(sys.argv[1], encoding="utf-8")):
    for m in re.finditer(r"((?:data/code|Part2/code)/[^:;]+?):([0-9,\-]+)", row["source_locations"]):
        path, spans = m.group(1), m.group(2)
        if not os.path.exists(path):
            print("MISSING", path); bad += 1; continue
        lines = open(path, encoding="utf-8").read().split("\n")
        for span in spans.split(","):
            if not span: continue
            a, _, b = span.partition("-"); a = int(a); b = int(b or a)
            if b > len(lines) or a > b:
                print("RANGE", path, span, len(lines)); bad += 1
            else:
                print(f"ok {row['instance_name'][:28]:28} {path}:{a} | {lines[a-1].strip()[:70]}")
print("problems:", bad)
