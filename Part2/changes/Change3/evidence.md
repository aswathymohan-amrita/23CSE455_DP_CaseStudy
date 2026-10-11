# CH03 Evidence - Different Cancellation Policies

Project: DaPlanStan (Rails 8.1.3)
Source version: `baseline` (frozen P01-P09 unchanged)
Working branch: `member3/evolution` at `cd306ec`
Scope: CH03 only. CH01 (personalized itinerary generation) and CH02 (multiple booking
providers) were completed earlier and are preserved.

This record is an AFTER note for an extension to existing booking behavior. It does not
modify or re-count the frozen P01-P09 baseline.

## 1. Requirement and observable behavior

Requirement (handoff): "Different cancellation policies" - new cancellation logic and any
affected trip, membership or controller responsibilities, with P03, P04 or P07 touched only
if actually affected. The handoff describes this only as an investigation entry point and
prescribes no design.

The source has no structured cancellation logic at all. Cancellation terms exist only as
free text inside `trip_items.notes` (the seeded stays carry "Free cancellation until
8 May 2026" at `db/seeds.rb:32` and `:40`, "28 April 2026" at `:43`, "13 April 2026" at
`:48`, and "9 May 2026" at `:56`). Nothing reads these
strings, and the app has no concept of whether a booking can still be cancelled or at what
cost. The concrete interpretation used here is therefore the smallest one supported by the
source: model a small set of cancellation policies on a trip item and answer, for a given
moment, whether cancelling is free and how much of the price is kept as a penalty.

Observable behavior after CH03:

- A trip item can record a cancellation policy (`trip_items.cancellation_policy`) and an
  optional free-cancellation deadline (`trip_items.free_cancellation_until`).
- Three policies are supported: `flexible` (free until the deadline, otherwise full
  penalty), `moderate` (free until the deadline, otherwise a half refund), and
  `non_refundable` (never free).
- Known spellings are normalized ("Non-refundable", "non refundable" become
  `non_refundable`); an unsupported value is rejected by validation rather than silently
  dropping the policy.
- `TripItem#cancellation_status(at:)` returns the eligibility/penalty for a moment in time
  (deadline inclusive), or `nil` when no policy is recorded.
- Manual items can pick a policy from the trip item form, and the detail page shows the
  policy, its free-until date and the current cancellation fee.

This feature only evaluates eligibility and penalty. It never cancels a booking and never
moves money; no refund is performed anywhere in the application.

## 2. Main files changed

New (CH03):

- `app/models/cancellation_policy.rb` - plain value module (no database table) holding the
  supported policies and the `evaluate` calculation.
- `db/migrate/20260511120000_add_cancellation_policy_to_trip_items.rb` - adds
  `cancellation_policy` (string) and `free_cancellation_until` (datetime) to `trip_items`.
- `test/models/cancellation_policy_test.rb` - policy calculation and boundary tests.
- `test/models/trip_item_test.rb` - model validation/normalization and `cancellation_status`
  tests.

Modified (CH03):

- `db/structure.sql` - `trip_items.cancellation_policy varchar` and
  `trip_items.free_cancellation_until datetime(6)` columns plus the matching
  `schema_migrations` version row.
- `app/models/trip_item.rb` - `cancellation_policy` inclusion validation (`:30`),
  `before_validation :normalize_cancellation_policy` (`:33`, definition `:81`), and
  `cancellation_status` (`:50`).
- `app/controllers/trip_items_controller.rb` - permits `:cancellation_policy` and
  `:free_cancellation_until` (`:133`). This is the only CH03 change in this file.
- `app/views/trip_items/_form.html.erb` - policy `select` plus a free-until `datetime_field`
  (`:118-132`).
- `app/views/trip_items/show.html.erb` - "Cancellation" block (`:135-156`).
- `test/controllers/trip_items_controller_test.rb` - three tests for policy create,
  rejection and detail rendering.

## 3. Relevant before/after implementation and design-pattern effect

Before:

- No cancellation model existed. `trip_items` had no policy or deadline column, and no code
  interpreted the free-text cancellation notes. `grep` for "cancel" in `app/` matched only
  unrelated UI text.

After:

- `app/models/cancellation_policy.rb:10` defines the policy set, `:34`
  (`CancellationPolicy.normalize`) canonicalizes input, and `:41`
  (`CancellationPolicy.evaluate`) computes `free`/`penalty_percent`/`refund_percent` at a
  given time, raising for an unsupported policy so a wrong rule can never be applied
  silently.
- `app/models/trip_item.rb:33` normalizes the policy before validation, `:30` rejects
  values outside the known set, and `:50` (`cancellation_status`) exposes the evaluation
  for the item at a given moment.
- `app/controllers/trip_items_controller.rb:133` lets the two new fields be set from the
  normal item form; `app/views/trip_items/show.html.erb:135` surfaces the policy and the
  current fee.

Why this is a small, defensible change: it adds one value module and two columns, changes
one model, one line of strong-params, and two view blocks. It reuses the existing pattern
already used for providers (a plain Ruby value module plus a normalized attribute) instead
of introducing a new table, service object, route or background job. It does not change
booking extraction, the AI boundary, trip/membership logic or controller responsibilities.

Design-pattern effect (baseline relation): no baseline pattern is affected. The feature is
trip-item-local data and a pure calculation; it does not touch P03 (trip responsibilities),
P04 (membership) or P07. The frozen P01-P09 counts are unchanged and no baseline pattern is
removed or reclassified. The policy calculation is a small plain module and is deliberately
not claimed as a GoF Strategy implementation.

## 4. Test commands and actual results

Toolchain: Ruby 3.4.2, Rails 8.1.3, Minitest. Run with mise. The test database is loaded
from `db/structure.sql`.

### Historical results (CH03 standalone, at time of CH03 completion)

Focused CH03 tests (2 new files plus the extended controller test):

    mise exec ruby@3.4.2 -- bin/rails test \
      test/models/cancellation_policy_test.rb \
      test/models/trip_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: **19 runs, 56 assertions, 0 failures, 0 errors, 0 skips.**

Full suite (at that time, CH01 + CH02 + CH03 = final combined):

    mise exec ruby@3.4.2 -- bin/rails test

Result: **65 runs, 204 assertions, 0 failures, 0 errors, 0 skips.** (Before CH03 the suite was
52 runs, 168 assertions; CH03 adds 13 tests.)

RuboCop on changed Ruby files:

    mise exec ruby@3.4.2 -- bin/rubocop --no-color \
      app/models/cancellation_policy.rb \
      app/models/trip_item.rb \
      app/controllers/trip_items_controller.rb \
      db/migrate/20260511120000_add_cancellation_policy_to_trip_items.rb \
      test/models/cancellation_policy_test.rb \
      test/models/trip_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: 7 files inspected, no offenses detected.

Whitespace check:

    git diff --check

Result: clean (no output, exit 0).

Migration consistency check:

    RAILS_ENV=test mise exec ruby@3.4.2 -- bin/rails db:migrate:status

Result: `up 20260511120000 Add cancellation policy to trip items` (the new migration is
present and up against the structure.sql-loaded schema).

New tests added:

- CancellationPolicy: flexible is free up to and including the deadline then fully
  penalised; moderate keeps a partial refund after the deadline; non_refundable is never
  free; a flexible policy with no deadline is not free; an unsupported policy raises;
  normalization and labels.
- TripItem: policy is normalized on save; an unsupported policy is rejected; a blank policy
  yields `nil` status; the recorded policy is evaluated at a given time and coexists with a
  CH02 provider.
- TripItemsController: create with a policy and deadline persists both; an unsupported
  policy is rejected (`unprocessable_entity`); the item page renders the policy.

### Combined-tree results (final)

The final combined test suite (all 10 test files) yields:

    mise exec ruby@3.4.2 -- bin/rails test

Result: **65 runs, 204 assertions, 0 failures, 0 errors, 0 skips.**

The CH03-focused subset in the combined tree (same 3 files) yields:

    mise exec ruby@3.4.2 -- bin/rails test \
      test/models/cancellation_policy_test.rb \
      test/models/trip_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: **19 runs, 56 assertions, 0 failures, 0 errors, 0 skips.**

This matches the historical CH03 result because CH03 was the last scenario implemented.
No further changes have been made to these test files.
