#!/usr/bin/env python3
"""Count nonblank implementation lines for each supplied Part 2 stage.
Run from the A11 submission root: python3 Part2/evidence/measure_source_loc.py
Snapshots are reconstructed in a temporary directory from Part1/code and the ordered patches.
Scope: src/app/**/*.ts excluding *.spec.ts and elearning-backend/src/main/java/**/*.java;
counts physical nonblank lines (including comments), not parser-derived executable LOC.
"""
from pathlib import Path
import csv, shutil, subprocess, tempfile
root=Path(__file__).resolve().parents[2]
stages=[('Original',[]),('After Change1',['Change1']),('After Change2',['Change1','Change2']),('After Change3',['Change1','Change2','Change3'])]
with tempfile.TemporaryDirectory(prefix='a11-loc-') as td:
    rows=[]
    for idx,(stage,changes) in enumerate(stages):
        dst=Path(td)/str(idx)
        shutil.copytree(root/'Part1/code',dst,ignore=shutil.ignore_patterns('node_modules','target','dist','.angular','.git'))
        for change in changes:
            patch=root/'Part2/changes'/change/'diff.patch'
            subprocess.run(['patch','-p1','-i',str(patch)],cwd=dst,check=True,stdout=subprocess.DEVNULL)
        files=[]
        for rel,ext in [('src/app','.ts'),('elearning-backend/src/main/java','.java')]:
            folder=dst/rel
            if folder.exists(): files += [p for p in folder.rglob('*'+ext) if '.spec.' not in p.name]
        loc=sum(1 for p in files for line in p.read_text(errors='replace').splitlines() if line.strip())
        rows.append((stage,len(files),loc))
    out=root/'Part2/evidence/source_loc_by_stage.csv'
    with out.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['source_version','production_files_counted','nonblank_physical_lines']); w.writerows(rows)
    for row in rows: print(','.join(map(str,row)))
