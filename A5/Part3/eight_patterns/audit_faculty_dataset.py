#!/usr/bin/env python3
"""Rebuild the faculty-schema cross-language dataset using executed source files.

Requires: pip install lizard. Compile before timing; one warmup; five process runs.
This script does not fabricate missing results. Exits nonzero on failed tests.
"""
import csv
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path
import lizard

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data"/"cross_language.csv"
MATRIX=ROOT/"Part3"/"eight_patterns"/"cross_language.csv"
MEASURED=ROOT/"Part3"/"eight_patterns"/"measured_results.csv"
PATTERNS={
 "Adapter":("EHR Patient Record","adapter"),
 "Strategy":("Diagnostic Booking Payment","strategy"),
}
SOURCES={
 "Adapter":{"Java":"AdapterDemo.java","Python":"adapter_demo.py","JavaScript":"adapterDemo.js","C++":"adapter_demo.cpp"},
 "Strategy":{"Java":"StrategyDemo.java","Python":"strategy_demo.py","JavaScript":"strategyDemo.js","C++":"strategy_demo.cpp"},
}
EXT={"Python":"python","Java":"java","JavaScript":"javascript","C++":"cpp"}
FIELDS=["pattern_name","instance_name","language","snippet_path","source_loc","max_function_cc","runtime_compiler","test_command","test_result","median_process_ms","language_notes"]
def call(cmd,cwd=None):
    r=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    if r.returncode:
        raise RuntimeError(f"{cmd} returned {r.returncode}: {r.stdout} {r.stderr}")
    return r
def measure(cmd,cwd):
    call(cmd,cwd)
    results=[]
    for _ in range(5):
        start=time.perf_counter_ns()
        call(cmd,cwd)
        results.append((time.perf_counter_ns()-start)/1e6)
    return results
def loc(path):
    return sum(bool(line.strip()) and not line.lstrip().startswith(("#","//","/*","*")) for line in path.read_text().splitlines())
def cc(path):
    analysis=lizard.analyze_file(str(path))
    return max((f.cyclomatic_complexity for f in analysis.function_list),default=1)
def version(language):
    cmd={"Python":[sys.executable,"--version"],"Java":["java","-version"],"JavaScript":["node","--version"],"C++":["g++","--version"]}[language]
    r=call(cmd)
    return (r.stdout or r.stderr).splitlines()[0].strip()
rows=[]
with DATA.open(newline="") as f:
    existing={(r["pattern_name"],r["language"]):r for r in csv.DictReader(f)}
for pattern,(instance,folder_name) in PATTERNS.items():
    for language,subdir in EXT.items():
        folder=ROOT/"Part3"/folder_name/subdir
        source=folder/SOURCES[pattern][language]
        if language=="Java":
            call(["javac",source.name],folder)
            cmd=["java",source.stem]
            display=f"cd Part3/{folder_name}/{subdir} && javac {source.name} && java {source.stem}"
        elif language=="C++":
            binary=Path("/tmp")/f"a5_original_{folder_name}"
            call(["g++","-std=c++17","-O2",source.name,"-o",str(binary)],folder)
            cmd=[str(binary)]
            display=f"cd Part3/{folder_name}/{subdir} && g++ -std=c++17 -O2 {source.name} -o /tmp/a5_original_{folder_name} && /tmp/a5_original_{folder_name}"
        elif language=="Python":
            cmd=[sys.executable,source.name]
            display=f"cd Part3/{folder_name}/{subdir} && python3 {source.name}"
        else:
            cmd=["node",source.name]
            display=f"cd Part3/{folder_name}/{subdir} && node {source.name}"
        raw=measure(cmd,folder)
        original=existing.get((pattern,language),{})
        rows.append(dict(pattern_name=pattern,instance_name=instance,language=language,
            snippet_path=str(source.relative_to(ROOT)),source_loc=loc(source),
            max_function_cc=cc(source),runtime_compiler=version(language),
            test_command=display,test_result="PASS (1/1 process assertion)",
            median_process_ms=f"{statistics.median(raw):.4f}",
            language_notes=(original.get("language_notes","")+"; measured on "+platform.platform()+
                "; five raw process times ms: "+";".join(f"{x:.4f}" for x in raw))))
with MEASURED.open(newline="") as f:
    measurements={(r["pattern_name"],r["language"]):r for r in csv.DictReader(f)}
with MATRIX.open(newline="") as f:
    matrix=list(csv.DictReader(f))
assert len(matrix)==32
for r in matrix:
    m=measurements[(r["pattern_name"],r["language"])]
    if m["test_result"]!="PASS":
        raise RuntimeError("Nonpassing measurement "+str(r))
    r["test_status"]="passed"
    r["median_process_ms"]=m["median_process_ms"]
    r["source_loc"]=m["source_loc"]
    r["max_function_cc"]=m["max_function_cc"]
    r["measurement_status"]="runtime_loc_cc_measured_lizard_1_21_0"
    path=ROOT/m["source_path"]
    language={"python":"Python","javascript":"JavaScript","java":"Java","cpp":"C++"}[r["language"]]
    rows.append(dict(pattern_name=r["pattern_name"].replace("_"," ").title(),
        instance_name=r["pattern_name"].replace("_"," ").title()+" healthcare extension",
        language=language,snippet_path=m["source_path"],source_loc=m["source_loc"],
        max_function_cc=m["max_function_cc"],runtime_compiler=version(language),
        test_command=r["test_command"],test_result="PASS (1/1 process assertion)",
        median_process_ms=m["median_process_ms"],
        language_notes="Reduced standalone example, not original baseline collaboration; "+
            m["timing_scope"]+"; raw timings in Part3/eight_patterns/measured_results.csv"))
with MATRIX.open("w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(matrix[0].keys()))
    writer.writeheader()
    writer.writerows(matrix)
assert len(rows)==40
with DATA.open("w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
print("Validated and wrote 40 faculty-schema rows to",DATA)
