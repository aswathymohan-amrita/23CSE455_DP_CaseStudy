"""Builds, tests, times and measures every Part 3 implementation.

Run from the team folder (A12/):  python data/test_result/part3/run_all.py [problem-prefix ...]
Writes Part3/llm/pattern_crosslanguage.csv, Part3/<problem>/<language>/test_result.log,
Part3/<problem>/<language>/README.md and data/test_result/part3/timings.csv.

Rules (also in README.md):
- Production files = everything in a language folder except the test runner (Runner.java,
  test_runner.py, testRunner.js, test_runner.cpp). Tests are kept separate and are not measured.
- source_loc = lizard NLOC of the production files (excludes blank lines and comments).
- max_function_cc = largest lizard cyclomatic complexity of any production function.
- Timing: compile first (not timed), 1 warm-up run, then 5 measured runs of the test command
  on the same machine; median wall-clock milliseconds of the whole process (runtime start-up,
  reading the shared cases.tsv and all cases). Raw times go to data/test_result/part3/timings.csv.
"""
import csv
import glob
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time

import lizard

HERE = os.path.dirname(os.path.abspath(__file__))
TEAM = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # data/test_result/part3 -> A12
PART3 = os.path.join(TEAM, "Part3")
EXE = ".exe" if os.name == "nt" else ""
LANGS = {
    "Java": dict(dir="java", runner="Runner.java", prod="*.java",
                 build=["javac", "-d", "build", "*.java"], cmd=["java", "-cp", "build", "Runner", "../cases.tsv"],
                 show_build="javac -d build *.java", show_cmd="java -cp build Runner ../cases.tsv"),
    "Python": dict(dir="python", runner="test_runner.py", prod="*.py",
                   build=None, cmd=[sys.executable, "-B", "test_runner.py", "../cases.tsv"],
                   show_build=None, show_cmd="python -B test_runner.py ../cases.tsv"),
    "JavaScript": dict(dir="javascript", runner="testRunner.js", prod="*.js",
                       build=None, cmd=["node", "testRunner.js", "../cases.tsv"],
                       show_build=None, show_cmd="node testRunner.js ../cases.tsv"),
    "C++": dict(dir="cpp", runner="test_runner.cpp", prod="*.hpp",
                build=["g++", "-std=c++17", "-O2", "-Wall", "-o", "build/test_runner" + EXE, "test_runner.cpp"],
                cmd=[os.path.join("build", "test_runner" + EXE), "../cases.tsv"],
                show_build="g++ -std=c++17 -O2 -Wall -o build/test_runner test_runner.cpp",
                show_cmd="./build/test_runner ../cases.tsv"),
}


def version(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True)
    text = (out.stdout + out.stderr).splitlines()
    return next(l for l in text if l and "JAVA_TOOL_OPTIONS" not in l).strip()


RUNTIMES = {
    "Java": version(["javac", "-version"]) + " / " + version(["java", "-version"]),
    "Python": version([sys.executable, "--version"]),
    "JavaScript": "Node.js " + version(["node", "--version"]),
    "C++": version(["g++", "--version"]) + " -std=c++17 -O2",
}
MACHINE = f"{platform.system()} {platform.release()} {platform.machine()}"


def measure(prod_files):
    nloc, maxcc, top = 0, 0, ""
    for f in prod_files:
        info = lizard.analyze_file(f)
        nloc += info.nloc
        for fn in info.function_list:
            if fn.cyclomatic_complexity > maxcc:
                maxcc, top = fn.cyclomatic_complexity, fn.name
    return nloc, maxcc, top


def rel(path):
    return os.path.relpath(path, TEAM).replace(os.sep, "/")


def write_readme(wd, lang, cfg, meta, prod, row):
    lines = [f"# {meta['pattern_name']} - {meta['instance_name']} ({lang})", "",
             f"- Production code: {', '.join('`' + os.path.basename(p) + '`' for p in prod)}",
             f"- Test runner (kept separate): `{cfg['runner']}`",
             "- Shared fixture and specification: `../cases.tsv`, `../spec.md`",
             f"- Runtime / compiler: {row['runtime_compiler']}", "",
             "## Run (working folder: this folder)", "```"]
    if cfg["show_build"]:
        lines.append(cfg["show_build"])
    lines += [cfg["show_cmd"], "```",
              "The runner prints `FAIL <case> expected=... got=...` for every mismatch, then `<passed>/<total> passed`;",
              "exit code 0 only when all cases pass. Raw output of the recorded run: `test_result.log`.", "",
              "## Result recorded in Part3/llm/pattern_crosslanguage.csv",
              f"- test result: **{row['test_result']}**, median process time {row['median_process_ms']} ms ({MACHINE})",
              f"- source LOC (lizard NLOC, production files only): {row['source_loc']}; "
              f"max function CC: {row['max_function_cc']}", "",
              "## Language notes", row["language_notes"], ""]
    open(os.path.join(wd, "README.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines))


def main(prefixes):
    problems = sorted(d for d in os.listdir(PART3) if d[:2].isdigit() and os.path.isdir(os.path.join(PART3, d)))
    if prefixes:
        problems = [p for p in problems if any(p.startswith(x) for x in prefixes)]
    rows, timings = [], []
    for prob in problems:
        meta = dict(csv.reader(open(os.path.join(PART3, prob, "meta.csv"), encoding="utf-8")))
        notes = {r[0]: r[1] for r in csv.reader(open(os.path.join(PART3, prob, "notes.csv"), encoding="utf-8"))}
        for lang, cfg in LANGS.items():
            wd = os.path.join(PART3, prob, cfg["dir"])
            prod = sorted(f for f in glob.glob(os.path.join(wd, cfg["prod"])) if os.path.basename(f) != cfg["runner"])
            result, median = "not_run", ""
            with open(os.path.join(wd, "test_result.log"), "w", encoding="utf-8", newline="\n") as lg:
                lg.write(f"# {prob} / {lang} - {time.strftime('%Y-%m-%d %H:%M:%S')} - {MACHINE}\n")
                lg.write(f"# runtime: {RUNTIMES[lang]}\n")
                if cfg["build"]:
                    os.makedirs(os.path.join(wd, "build"), exist_ok=True)
                    b = cfg["build"]
                    if "*.java" in b:
                        b = b[:-1] + sorted(os.path.basename(f) for f in glob.glob(os.path.join(wd, "*.java")))
                    r = subprocess.run(b, cwd=wd, capture_output=True, text=True)
                    lg.write(f"$ {cfg['show_build']}\n{r.stdout}{r.stderr}")
                    if r.returncode:
                        result = "failed (compile error)"
                if result == "not_run":
                    times, out = [], None
                    cmd = [os.path.join(wd, cfg["cmd"][0])] + cfg["cmd"][1:] if lang == "C++" else cfg["cmd"]
                    for i in range(6):
                        t0 = time.perf_counter()
                        out = subprocess.run(cmd, cwd=wd, capture_output=True, text=True)
                        dt = (time.perf_counter() - t0) * 1000
                        if i:
                            times.append(dt)
                        timings.append([prob, lang, "warmup" if i == 0 else f"run{i}", f"{dt:.2f}"])
                    lg.write(f"$ {cfg['show_cmd']}\n{out.stdout}{out.stderr}exit={out.returncode}\n")
                    last = (out.stdout.strip().splitlines() or ["?"])[-1]
                    result = last.replace(" passed", "") if out.returncode == 0 else f"failed {last}"
                    median = f"{statistics.median(times):.1f}"
            if cfg["build"]:
                shutil.rmtree(os.path.join(wd, "build"), ignore_errors=True)  # no compiled binaries in the repo
            nloc, maxcc, top = measure(prod)
            row = {
                "pattern_name": meta["pattern_name"], "instance_name": meta["instance_name"], "language": lang,
                "snippet_path": "; ".join(rel(f) for f in prod),
                "source_loc": nloc, "max_function_cc": maxcc, "runtime_compiler": RUNTIMES[lang],
                "test_command": f"cd {rel(wd)} && {cfg['show_cmd']}"
                                + (f"  (build: {cfg['show_build']})" if cfg["show_build"] else ""),
                "test_result": result, "median_process_ms": median,
                "language_notes": notes.get(lang, "") + (f" Max-CC function: {top}." if top else ""),
            }
            rows.append(row)
            write_readme(wd, lang, cfg, meta, prod, row)
            print(f"{prob:44} {lang:10} {result:8} {median:>8} ms  loc={nloc:<4} cc={maxcc}")
    out_csv = os.path.join(PART3, "llm", "pattern_crosslanguage.csv")
    keep = []
    if prefixes and os.path.exists(out_csv):  # partial run: keep other problems' rows
        names = {r["instance_name"] for r in rows}
        keep = [r for r in csv.DictReader(open(out_csv, encoding="utf-8")) if r["instance_name"] not in names]
    cols = ["pattern_name", "instance_name", "language", "snippet_path", "source_loc", "max_function_cc",
            "runtime_compiler", "test_command", "test_result", "median_process_ms", "language_notes"]
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(sorted(keep + rows, key=lambda r: (r["snippet_path"].split("/")[1], list(LANGS).index(r["language"]))))
    tpath = os.path.join(HERE, "timings.csv")
    old = []
    if prefixes and os.path.exists(tpath):
        done = {t[0] for t in timings}
        old = [r for r in csv.reader(open(tpath)) if r and r[0] not in done and r[0] != "problem"]
    with open(tpath, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["problem", "language", "run", "wall_ms"])
        w.writerows(sorted(old + timings))
    with open(os.path.join(HERE, "environment.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"machine: {MACHINE}\n")
        for k, v in RUNTIMES.items():
            fh.write(f"{k}: {v}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
