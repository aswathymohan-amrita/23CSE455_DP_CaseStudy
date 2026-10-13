# Refactoring and Functional-Change Evidence — Member 3 / Part 2

## Measurement and evidence basis

The companion `refactoring_source_diffs.patch` contains source comparisons between
`Part2/baseline/` and `Part2/code/` for the relevant controllers and extracted
collaborators. The LOC procedure and its actual output are in
`measure_source_loc.py` and `LOC_Metrics_2026-10-11.txt`.

## Refactoring candidate 1 — Extract bulk-import persistence

**Technique:** Extract Service / Move Method.

**Source:** `Part2/baseline/app/controllers/trip_items_controller.rb`,
`Part2/code/app/controllers/trip_items_controller.rb`, and
`Part2/code/app/services/trip_items_bulk_import.rb`.

The batch-persistence responsibility was moved into `TripItemsBulkImport`.
The pre-existing manual import flow is intended to retain its behavior; the new
itinerary-generation confirmation flow also uses the extracted service. That reuse
is a feature of CH01, whereas the extraction itself is the refactoring.

**Behavior-preservation evidence:** inspect the final-tree tests in
`Part2/code/test/services/trip_items_bulk_import_test.rb` and
`Part2/code/test/controllers/trip_items_controller_test.rb`. The recorded final
suite is 65 runs, 204 assertions, zero failures, zero errors, zero skips, but this
file does not contain a raw test log. These are reported historical results, not
a baseline-versus-after equivalence proof. Re-run and save output before claiming
independently reproducible verification.

## Refactoring candidate 2 — Extract shared trip edit authorization

**Technique:** Extract Concern / consolidate shared authorization behavior.

**Source:** `Part2/code/app/controllers/concerns/editable_trip_scoped.rb`,
`Part2/code/app/controllers/trips_controller.rb`, and
`Part2/code/app/controllers/itinerary_generations_controller.rb`.

The concern centralizes owner/planner authorization for the existing trip editing
flow and the new itinerary-generation flow. Treat preservation of the existing
trip authorization behavior as the refactoring claim; the new generation endpoint
itself is functional behavior, not a behavior-preserving change.

**Evidence to review:** inspect `Part2/code/test/controllers/trips_controller_test.rb`
and `Part2/code/test/controllers/itinerary_generations_controller_test.rb` alongside
the source diff. A final-tree test passing alone does not prove complete equivalence
with the original implementation.

## Functional changes — not refactorings

- **CH01:** Personalized itinerary generation, background processing, preview, and
  confirmation are new functionality. Do not classify the entire scenario as a
  behavior-preserving refactoring.
- **CH02:** Provider normalization, provider persistence, and a provider/type/location
  matching name intentionally change booking behavior to prevent same-provider
  bookings from collapsing. This is a functional change to P01, not a
  behavior-preserving refactoring.
- **CH03:** Cancellation policy fields, normalization, eligibility/penalty calculation,
  and display are new functionality. The evidence does not claim a GoF Strategy
  implementation.

## Limitation

There is no saved baseline test-run log establishing an identical before/after test
comparison. The recorded final-tree tests support regression confidence but do not
prove that every behavior is unchanged. Do not claim a refactoring was proven
behavior-preserving beyond the cases actually tested.
