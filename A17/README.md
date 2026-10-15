# A17 - PlantUML Diagram Generation System

**Case study:** Design Pattern Analysis and Evolution in the PlantUML Diagram Generation System (23CSE455 Design Patterns). The selected family is class diagrams.

## Team

| Roll number | Student | Batch | Technical area assigned for personal review |
| --- | --- | --- | --- |
| AM.SC.U4CSE23064 | Sathvik Pasuvula | CSE A | Baseline parsing/model trace; Command, Factory Method and Composite mappings; CH01; Java and Python examples |
| AM.SC.U4CSE23142 | P Sai Satvik Chowdary | CSE A | Layout Strategy and VizJs Adapter mappings; CH02 and CH03; JavaScript and C++ examples; dataset audit |

These are **assigned areas, not completed-contribution claims**. Neither student's independent review was confirmed when this package was prepared. The steps and sign-off fields are in [HUMAN_VERIFICATION.md](HUMAN_VERIFICATION.md) and [data/human_verification.csv](data/human_verification.csv). The analysis, source edits, tests and document preparation performed with AI assistance are disclosed in the LLM records.

## Selected application

- Application: [PlantUML](https://github.com/plantuml/plantuml), a text-to-diagram generator.
- Baseline tag: `v1.2026.8`; peeled commit: `149874a1bb2b64c42889d7178cb89f6647ac14bc`; annotated tag object: `b531f7b00ebf733d9079a7b0a0180c64ded21ef0`.
- Source access date: 2026-10-11. The inspected Java files carry GPL-3.0-or-later notices; upstream `LICENSE`, `COPYING` and `LICENSES.md` are saved in `Part1/code/`.
- Stack on the selected path: Java (production code compiled for release 11), Gradle, Graphviz/Smetana/ELK/TeaVM layout options, and SVG/PNG export. No database is used by the inspected path.
- Faculty approval was not supplied and is not claimed.

`Part1/code/` contains the exact upstream baseline files inspected for the pattern trace, with original paths and license files. It is a **source subset**, not a claim that the whole PlantUML repository is copied here. `Part2/code/` contains the nine changed Java files after CH03; the three patches and exact commits reconstruct the full modified application source.

## Source versions

| Snapshot | Commit | Change and evidence |
| --- | --- | --- |
| Baseline | `149874a1bb2b64c42889d7178cb89f6647ac14bc` | Official `v1.2026.8`; `Part1/code/`; 3/3 focused checks |
| After CH01 | `8e9f313b8f589012115d631df4aad2a369a22f53` | Review status on class declarations; `Part2/changes/Change1/`; 11/11 |
| After CH02 | `0d170a89f61fc811f729f236a28634c697f985a6` | Configurable review palette; `Part2/changes/Change2/`; 15/15 |
| After CH03 | `dd5c91b457c13fb1a20ae51a62fa73c3b8485847` | Optional SVG review metadata; `Part2/changes/Change3/`; 20/20 |

The `change.patch` files apply sequentially to the baseline. `Part2/evidence/reconstruction.txt` records a byte-for-byte comparison of their reconstructed diff with the final local source commit. Saved cumulative Java snapshots are in each `ChangeN/source/` directory.

## Inspected modules and pattern results

The trace follows `ClassDiagramFactory` and `PSystemCommandFactory` command registration and selection; `CommandCreateClass` and `CommandLinkClass`; `Entity` and `Link`; `CucaDiagram` layout selection; the class-header `TextBlock` tree; `GraphvizJs`; and SVG/PNG output through `EntityImageClass` and `PortableSvgDocument`. Other diagram families, the web server, optional VizJs execution, and full TeaVM/ELK runtime behavior are outside the observed path.

| Snapshot | Confirmed types | Confirmed instances | Change in the scoped inventory |
| --- | ---: | ---: | --- |
| Baseline | 5 | 5 | Command, Factory Method, Strategy, Composite, Adapter |
| After CH01 | 5 | 5 | Existing Command collaboration modified |
| After CH02 | 5 | 6 | New review-fill Strategy collaboration |
| After CH03 | 5 | 6 | Existing collaborations preserved or modified; SVG serializer extended |

The inventory covers these five source-checked pattern types in the selected class-diagram path, not every pattern in PlantUML. Two candidates were rejected and one remains uncertain; see `Part1/evidence/candidate_review.md`. Participant roles, line ranges and version-specific status are in `data/patterns.csv`, `data/patterns_evolution.csv` and `data/pattern_counts.csv`.

## Tests and environment

| Check | Actual result | Evidence |
| --- | --- | --- |
| Focused baseline and evolution checks | 3/3, 11/11, 15/15, 20/20 | `Part2/evidence/snapshots.json`, per-change logs |
| Final full-built JAR checks | 20/20 | `Part2/evidence/full-build/tests.log` |
| Full upstream tests, baseline and final | Same two `PicowebTest` failures in both trees | `Part2/evidence/upstream/` |
| Four-language shared fixtures | 16/16 each in Java, Python, JavaScript and C++ | `Part3/evidence/results.json` |

The Gradle console reports **3,189 total: 3,177 passed, 2 failed, 10 skipped**. Generated JUnit XML/HTML counts **3,191 entries: 3,177 passed, 2 failed, 12 skipped**. The two extra skipped entries appear in both trees. The Picoweb failures expected HTTP 200 and received 503; a clean full suite is not claimed.

| Tool | Recorded version |
| --- | --- |
| OS | macOS 27.0.1 arm64 |
| Java / Gradle | OpenJDK 25.0.2 / Gradle 9.3.1 |
| Graphviz | 16.1.0 |
| Python / Node.js | 3.14.2 / 22.19.0 |
| C++ compiler | Apple clang 21.0.0 |
| Metrics | Lizard 1.24.1 |

The PlantUML version catalog pins JUnit 6.1.3, ELK 0.12.0, TeaVM 0.14.1, JLaTeXMath 1.0.7 and OpenPDF 3.0.5.

## Run and test commands

From this `A17/` directory, reconstruct the final application in a **new absolute-path directory**:

```bash
bash Part2/reconstruct.sh /absolute/output/plantuml-a17
cd /absolute/output/plantuml-a17
GPL_ONLY=1 bash gradlew jar test -Pfast --console=plain
```

To rerun focused snapshot checks, obtain the official PlantUML `v1.2026.8` release JAR first. The runner compiles the saved changed Java files against it and exercises the real parser, model and SVG/PNG exporter:

```bash
python3 Part2/run_evolution.py /absolute/path/plantuml-1.2026.8.jar /absolute/output/snapshot-builds
```

For the four-language comparison:

```bash
python3 Part3/run_tests.py
```

This runner compiles Java and C++ in a temporary directory. The language READMEs in `Part3/diagram/{java,python,javascript,cpp}/` give individual commands. To audit the packaged CSV paths, workbook parity and saved results, run `python3 tools/validate_submission.py` with `openpyxl` available. The saved result is `data/test_result/validation.txt`.

## Measurement rules and cross-language comparison

`data/evolution_metrics.csv` measures the same nine production Java paths listed in `Part2/evidence/measurement_scope.txt` at every snapshot; a newly introduced file contributes zero before it exists. `data/cross_language.csv` measures production code only, excluding runners and tests. Source LOC is Lizard nonblank, noncomment NLOC. Maximum function CC is the highest Lizard per-function cyclomatic complexity for that language.

Part 3 uses one small diagram model that demonstrates all five verified pattern types in each of four languages with the same 16 fixtures. Compile first; run one warm-up and five measured fresh processes; report the median. Timing includes process startup, standard input, execution and captured output, but excludes compilation and the 16-case correctness loop. Raw samples and per-function CC are in `Part3/evidence/`. The same program metrics appear on five pattern rows per language and must not be added together.

## LLM records and limitations

`data/llm.csv` links the three course parts to the **actual** prompt, supplied-context manifest, public output and correction notes in `prompts/`. The runtime record identifies the model as `gpt-6-astra`; its displayed UI label and access tier were not independently confirmed. Human review of pattern roles, source changes and language behavior remains pending. No student is credited with work performed only by the AI assistant.

Other limits: the inspection covers one diagram family and a representative source path; VizJs, ELK and TeaVM branches are source-verified but not all executed; review syntax is single-line; new metadata is SVG-only; and the two upstream Picoweb failures remain unresolved. Faculty approval is unconfirmed.

## Folder map and submission status

```text
A17/
  README.md  HUMAN_VERIFICATION.md  A17_Report.tex  A17_Report.pdf
  data/      patterns.csv  pattern_counts.csv  patterns_evolution.csv
             cross_language.csv  llm.csv  evolution_metrics.csv
             human_verification.csv  A17_Dataset.xlsx  test_result/
  Part1/     code/ (baseline subset)  diagrams/  evidence/
  Part2/     code/ (evolved subset)  changes/Change1..Change3/
             diagrams/  tests/  evidence/
  Part3/     diagram/{java,python,javascript,cpp}/  test-cases/
             evidence/  A17_slide.pdf
  prompts/   exact prompts, inputs, public outputs, verification
  tools/     submission validator
```

The folder is proposed at the course repository root in [PR #16, “A17: Final Submission”](https://github.com/aswathymohan-amrita/23CSE455_DP_CaseStudy/pull/16). The PR is open, not merged. A screenshot of the **merged** `A17/` directory must be captured after merge; none is fabricated here. Student sign-offs, faculty approval and LLM-tier confirmation must be recorded from real evidence before final submission.

## References

- [PlantUML source, tag `v1.2026.8`](https://github.com/plantuml/plantuml/tree/v1.2026.8) and [class-diagram documentation](https://plantuml.com/class-diagram).
- E. Gamma, R. Helm, R. Johnson and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994.
- [Oracle Java abstract classes](https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html), [Python `abc`](https://docs.python.org/3/library/abc.html), [MDN JavaScript classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), and [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
