# Part 2 — Change impact, pattern evolution and integration

This section analyzes three hypothetical changes against the **unchanged baseline** at `1e7420e431771e3f5eec470d8a005e8255fa5fe8`:

- **Change 1:** laboratory integration
- **Change 2:** billing provider
- **Change 3:** patient-data/FHIR integration

The `changes/Change1`, `Change2` and `Change3` directories contain the **original proposal-stage** requirements, descriptive diffs and historical test notes. They are not applied Git patches, and a historical “not run” statement refers to the original proposal stage.

`code/` contains the first standalone PHP prototypes. `eight_patterns/` contains eight **separate standalone** pattern collaborations and PHP contracts. `../laravel_integration/` is the later installable Laravel overlay with three additional protected endpoints, dependency-injection bindings and tests using Laravel HTTP fakes; it does **not** replace the original application's booking or patient controllers and does not contact live vendors.

**Pattern-count conventions:** `Pattern_count.csv` separates `original` (2 types, 5 observed instances), `standalone_eight_pattern_extension` (8 types, 8 teaching examples) and `laravel_overlay` (2 types, 3 new HTTP integration collaborations). These phases are **not additive**: the overlay is a separate implementation of some proposed roles, not three more independent baseline discoveries. `patterns_evolution.csv` distinguishes the historical proposal stage from the later tested overlay. The eight-pattern team allocation is proposed, not independently verified authorship.

`diagrams/` contains the architecture and class diagrams. See `../README.md` and the report for the complete evidence boundary and reproduction instructions.
