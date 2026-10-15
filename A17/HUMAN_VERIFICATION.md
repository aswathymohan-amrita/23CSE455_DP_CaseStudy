# Team A17: technical contribution record

This is the division of substantive work for the two students. The package was
prepared with AI assistance, so neither student should claim its source edits,
tests or analysis as personally performed solely because their name appears on
the report. Mark an item complete only after doing it, and cite the evidence or
correction in `data/human_verification.csv`. Keep this file with the report.

## Sathvik Pasuvula — AM.SC.U4CSE23064, CSE A

1. Trace the class input in `Part1/evidence/baseline.puml` from
   `ClassDiagramFactory` command registration through `CommandCreateClass`,
   `CommandLinkClass`, `Entity`, `Link` and SVG export. Check the Command,
   Factory Method and Composite participant rows and source ranges in
   `data/patterns.csv`. Correct any unsupported role in both the dataset and
   report.
2. Inspect `Part2/changes/Change1/change.patch` for CH01. Reconstruct the
   source with `Part2/reconstruct.sh` or examine its saved cumulative source.
   Run `Part2/run_evolution.py` with the specified baseline release JAR;
   confirm the CH01 11/11 result and inspect `Part2/evidence/CH01/review.png`.
3. Run `Part3/run_tests.py`; inspect the Java and Python pattern participants
   and fixture outputs. Explain any language-specific difference in the report.

Evidence to enter: review date, exact source paths and lines, command output or
log path, corrections made, and commit hash if committing changes. Status: **not
yet signed off**.

## P Sai Satvik Chowdary — AM.SC.U4CSE23142, CSE A

1. Verify the class layout Strategy selection in `net.atmp.CucaDiagram` and the
   VizJs Adapter contract in `GraphvizJs` against source. Check the corresponding
   `data/patterns.csv` rows, including branches not executed by the tests.
2. Inspect CH02 and CH03 patches and saved Java source. Reproduce or inspect
   the 15/15 and 20/20 results. Check that explicit class fill overrides the
   review palette; inspect `Part2/evidence/CH03/metadata.svg` and
   `PortableSvgDocument` to confirm `data-review-status` is serialized only
   when enabled.
3. Run `Part3/run_tests.py`; inspect JavaScript and C++ fixture outputs. Audit
   `data/cross_language.csv` against the recorded timings and compare CSV rows
   with `data/A17_Dataset.xlsx`.

Evidence to enter: review date, exact source paths and lines, command output or
log path, corrections made, and commit hash if committing changes. Status: **not
yet signed off**.

Both students should independently read the final report before submission and
sign the corresponding claims in `data/human_verification.csv`. Faculty approval,
the LLM access-tier requirement and the course PR merge must be confirmed from
real records. These are administrative submission checks, not substitutes for
the technical contributions above.
