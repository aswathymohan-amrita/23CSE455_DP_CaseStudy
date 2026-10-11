# Copy manifest

This folder is a local copy for `Team_B9_DP`; source files and worktrees under the
parent `DP` workspace were left untouched. The copied case-study bundle contains
500 files before this manifest was added.

| Destination | Source material and purpose |
| --- | --- |
| `README.md` | The audited case-study overview from `team-b9/Aditya/README.md`. |
| `Part1_Findings/` | Findings, CSV data, verification notes, and diagrams from `Part1_Findings/`. The selected OpenWMS source excerpts come from `Part1_Findings/repo/org.openwms/`; the larger embedded repository snapshot is not duplicated here. |
| `Part2/CH01-multiple-warehouses/` | Evidence and filtered complete-source snapshots from the `org.openwms.common.service.lib/` and `org.openwms.common.service/` worktrees. `PROVENANCE.md` records their origins and limitations. The copies do not include Git metadata and are not claimed as runnable Maven workspaces. |
| `Part2/CH02-barcode-picking/` | The complete project files, tests, resources, evidence, and Maven build file from `CH02-barcode-picking/`. |
| `Part2/CH03-stock-reorder/` | The complete project files, tests, resources, evidence, class diagram, and Maven build file from `CH03-stock-reorder/`. |
| `Part3-cross-language/` | Language implementations, tests, metrics, and evidence from `Part3-cross-language/`. |
| `LLM_RECORDS/LLM_RECORDS.md` | A publication copy of `LLM_RECORDS.md`; machine-specific paths and reviewer identity are redacted. |
| `report/casestudy.tex` | Listed in the original copy plan but **not present** in the published repository; superseded by the repository-level `report/` folder. |
| `screenshots/` | Listed in the original copy plan but **not present** (it was empty, and Git does not track empty folders). |

The audited staging copy was sourced from `team-b9/Aditya/`, whose source map is
in `team-b9/INVENTORY_REPORT.md`. No `.git` directories or Maven `target`
directories were copied. The stale `DP_Csestudy.pdf`, ZIP archives, and
unrelated workspace files were also excluded. The CH02 and CH03 source projects
do not contain standalone `LICENSE` files; none was invented or added.
The Part 1 verification notes omit the verifier's identity, and Part 3 uses a
generic Python command rather than retaining a machine-specific executable path.

CH02 and CH03 are independent reference implementations, not changes to the
canonical OpenWMS Picking or Inventory services. CH01 changes remain
uncommitted in the original worktrees. Do not commit or publish these local
copies without the attribution and licensing review described in the README.
