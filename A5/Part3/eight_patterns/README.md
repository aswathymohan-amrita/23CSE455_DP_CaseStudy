# A5 cross-language extension (8 patterns x 4 languages)

Each pattern has standalone demonstrations in Python, JavaScript, Java and C++ (32 source files). These are **portable reduced examples**, not Laravel code. They preserve the pattern roles and representative healthcare use cases but deliberately omit network services, framework routing, databases, authentication and clinical data.

## Running

From `A5/` run the per-language commands in `Part3/eight_patterns/cross_language.csv`. Run `python3 Part3/eight_patterns/benchmark.py` followed by `python3 Part3/eight_patterns/audit_faculty_dataset.py` from `A5/` after `python3 -m pip install lizard==1.21.0`. The repository workflow `.github/workflows/a5-validate.yml` has validated all 32 implementations and the PHP contracts. `cross_language.csv` records the verified run status and the corresponding measured median/LOC from `measured_results.csv`. `benchmark.py` regenerates process-level measurements; five raw times and medians are recorded in `measured_results.csv`. Cyclomatic complexity is measured using **lizard 1.21.0** as the maximum per-function CCN reported for each source file. CCN is the analyzer's branch-counting metric; source LOC excludes blank and standalone comment lines.

## Evaluation notes

All implementations use synthetic data and deterministic assertions. Cross-language timing must use a shared protocol: compile first, then time five process executions on the same CI machine, record raw times and median; startup costs are included, compilation is excluded, and these are not steady-state benchmarks. The faculty-schema audit also measures the eight original Adapter/Strategy programs after one warmup and five timed executions; see `../../data/cross_language.csv`. Keep the original Adapter and Strategy evidence separate from these newly added simplified variants.

## Pattern / domain mapping

- Facade: appointment booking + notification
- Repository: patient lookup persistence abstraction
- Adapter: laboratory order vendor payload translation
- Strategy: payment method selection
- Proxy: cached patient data lookup and invalidation
- Observer: clinical event subscriber notifications
- Factory Method: medical record JSON/CSV exporter creation
- Decorator: medical record access auditing

These 8 designs are **proposed extensions**; baseline counts must not be rewritten as if they existed in the original Laravel application.
