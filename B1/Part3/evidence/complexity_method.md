# Cyclomatic-complexity measurement status

## Selected method

Use Lizard's function-level cyclomatic-complexity metric with one pinned tool version across all Java, Python, JavaScript, and C++ examples. Record the Lizard version and configuration with the measurements. Take the maximum function-level CC in each source file; do not mix this with maintainability index, cognitive complexity, or hand-counted token totals. A Lizard report must be retained as raw evidence before populating `data/cross_language.csv`.

## Current status

No reliable values are available yet. Lizard is not installed in the inspected environment; `lizard`, `radon`, `tree_sitter`, and `javalang` are unavailable. The relevant C++ compilers are also absent. No package was installed. All `max_function_cc` cells remain blank rather than filling them with an unvalidated regex or visual estimate.

The `source_loc` column currently means physical source-file lines counted with PowerShell `Get-Content | Measure-Object -Line`; it includes blank lines and comments and must not be described as logical SLOC.

The intended language-specific rules are those of the same Lizard version's Java, Python, JavaScript, and C++ parsers. Those parser rules cannot be asserted more specifically until the tool/version is present and its report can be inspected. Keep the values unavailable until then.

No language-specific counting rule has been applied in the current package. In particular, there are no hand-counted adjustments for switch/case branches, Python boolean/comprehension constructs, JavaScript conditional expressions, or C++ preprocessor constructs. A single verified parser/version must establish those rules before publishing comparable values.

## Commands for a suitable environment

After the team authorizes/chooses a Python environment and installs a pinned Lizard version, run the tool on every source file under `Part3/*/{java,python,javascript,cpp}/` and save its complete report. Confirm that all 40 sources are recognized as functions, record the tool version, and update each language/pattern row only from that report. Do not substitute default `radon` (Python-only) for cross-language measurement.
