# Case-study artifacts

This directory contains the collected Part 1 findings, Part 2 change evidence and code snapshots, Part 3 cross-language examples, LLM records, and the current report draft.

## Report

- The report sources and compiled PDFs are in the repository-level `report/` folder: `main.tex` (full case-study report) and `part1_findings.tex`, `part2_findings.tex`, `part3_findings.tex` (per-part findings), each with its PDF.
- The `report/casestudy.tex` draft and `screenshots/` folder listed in `COPY_MANIFEST.md` were not included when this folder was published.

## Part 1

The audited findings confirm exactly two GoF patterns and two instances: Observer and Composite. `TreeNode<T>`/`TreeNodeImpl<T>` is a generic utility finding; no concrete application/domain client use was found in the accessible OpenWMS repository. The findings, CSVs, source excerpts, verification notes, and editable PlantUML sources are retained under `Part1_Findings/`.

## Part 2

- `Part2/CH01-multiple-warehouses/` preserves the changed-file evidence snapshots in `org.openwms.common.service.lib/` and `org.openwms.common.service/`. Separate `org.openwms.common.service.lib.complete-source/` and `org.openwms.common.service.complete-source/` directories contain the complete eligible Java source/test sets and supporting build/source files from each original repository. `PROVENANCE.md` records upstream URLs, baseline HEADs, exact CH01 changed-file lists, and the files excluded for credentials.
- Neither copied form includes Git metadata. The complete-source snapshots also omit credential-bearing configuration/workflow files, so they are source-complete for the copied Java trees but are not guaranteed standalone Maven workspaces. No build or test is claimed for those copies. The CH01 files remain uncommitted in the original worktrees; production mapping/backfill is not evidenced.
- `Part2/CH02-barcode-picking/` is an independent Spring Boot reference implementation because the canonical Picking repository was inaccessible.
- `Part2/CH03-stock-reorder/` is an independent Spring Boot reference implementation because the canonical Inventory repository was inaccessible.

CH02 and CH03 must not be described as merged into canonical OpenWMS services or deployed. Their evidence files describe behavior, tests, metrics, and limitations. Their BEFORE/AFTER commit IDs refer to the original local project histories, which are not included in this repository. CH03 state is in memory with single-process synchronization and does not claim a new GoF pattern.

## Part 3 and LLM records

`Part3-cross-language/` includes eight pattern implementations, their tests, CSV metrics, and evidence. The recorded 28/28 checks passed; timing includes process startup and is not a language-performance claim. `LLM_RECORDS/LLM_RECORDS.md` preserves historical statuses and addenda while redacting machine-specific profile paths and reviewer identity in this publication copy.

## Reproduction

- CH02: from its directory, run `mvn.cmd -DforkCount=0 verify`.
- CH03: from its directory, run `mvn.cmd -DforkCount=0 verify`.
- Part 3: use the language-specific commands and tool versions in `Part3-cross-language/PART3_EVIDENCE.md`.
- CH01: use the untouched original repositories for full build/test verification. Aggregate changed-file snapshots are evidence copies; complete-source snapshots omit `.git/` and credential-bearing configurations and have not been compiled or tested.

All reported Maven runs using `forkCount=0` retain the caveat that test accuracy may be reduced. See `COPY_MANIFEST.md` for the source-to-destination map and copy exclusions.
