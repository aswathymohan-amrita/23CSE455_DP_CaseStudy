# CH01 Evidence - Personalized Itinerary Generation

Project: DaPlanStan (Rails 8.1.3)
Source version: `baseline` (frozen P01-P09 unchanged)
Working branch: `member3/evolution` at `cd306ec`
Scope: CH01 only. CH02 (multiple booking providers) and CH03 (different cancellation
policies) were not started.

This record is an AFTER note for a genuinely new functionality. It does not modify or
re-count the frozen P01-P09 baseline.

## 1. Requirement and observable behavior

Requirement: give a trip owner/planner in-app, AI-assisted personalized itinerary
suggestions, reviewed by a human before anything is saved.

Observable behavior:

- From the trip panel, an owner or planner triggers "Generate". A background job asks
  Claude for suggestions; the page shows a generating state and updates in place when
  results arrive (Turbo Stream).
- The preview lists up to 12 validated suggestions (name, kind, optional address,
  dates, URL, notes). Suggestions that are blank, use an unknown kind, fall outside the
  trip dates, end before they start, duplicate an existing item, or exceed the limit
  are filtered out and reported.
- "Add these to itinerary" persists the reviewed suggestions as `idea` items only on
  explicit confirmation, using the same importer as the manual JSON import.
- Duplicate-generation prevention: repeated accidental submissions while a generation
  is already queued or running do not enqueue a second job, and therefore do not make a
  second AI call. Once a generation has finished, intentional regeneration
  ("Generate again" / "Try again") still works.

## 2. Main files changed

New (CH01):

- `app/services/itinerary_generator.rb` - AI boundary: builds the prompt, calls Claude
  via the `anthropic` gem, validates/normalizes output, never persists.
- `app/services/trip_items_bulk_import.rb` - shared persistence service extracted from
  the manual import so AI and manual imports use one path.
- `app/jobs/generate_itinerary_job.rb` - background generation, caches the preview,
  broadcasts the result, clears the in-progress marker.
- `app/controllers/itinerary_generations_controller.rb` - create/show/confirm.
- `app/controllers/concerns/editable_trip_scoped.rb` - shared owner/planner authz
  extracted from `TripsController`.
- `app/views/itinerary_generations/show.html.erb`,
  `app/views/itinerary_generations/_result.html.erb` - preview UI.
- `test/services/itinerary_generator_test.rb`,
  `test/services/trip_items_bulk_import_test.rb`,
  `test/controllers/itinerary_generations_controller_test.rb`,
  `test/jobs/generate_itinerary_job_test.rb`.

Modified (CH01):

- `config/routes.rb` - `resource :itinerary_generation, only: [:create, :show]` with
  `post :confirm` (`config/routes.rb:41`).
- `app/controllers/trips_controller.rb`, `app/controllers/trip_items_controller.rb` -
  use the extracted concern/service.
- `app/views/trips/_trip_panel.html.erb` - "Generate" entry point.
- `config/application.rb`, `config/environments/test.rb` - test infrastructure.

Final increment (duplicate-generation prevention) touched exactly:

- `app/jobs/generate_itinerary_job.rb`
- `app/controllers/itinerary_generations_controller.rb`
- `test/controllers/itinerary_generations_controller_test.rb`
- `test/jobs/generate_itinerary_job_test.rb`

## 3. Relevant before/after implementation and design-pattern effect

Before (final increment): `ItineraryGenerationsController#create` unconditionally
called `GenerateItineraryJob.perform_later(@trip.id, current_user.id)`. A double-click,
a repeated submit, or a re-open while a generation was running enqueued a second job
and made a second Claude call.

After (final increment):

- `app/jobs/generate_itinerary_job.rb:20` adds
  `GenerateItineraryJob.enqueue_unless_running(trip:, user:)`. It reads an in-progress
  cache marker (`GenerateItineraryJob.in_progress_key`, `app/jobs/generate_itinerary_job.rb:29`),
  returns `false` if one exists, otherwise writes the marker (TTL
  `IN_PROGRESS_TTL = 5.minutes`) and enqueues exactly one job.
- `app/jobs/generate_itinerary_job.rb:48` releases the marker in an `ensure` block, so
  it is cleared on success and on failure; regeneration after a result is never blocked.
- `app/controllers/itinerary_generations_controller.rb:12` now calls
  `enqueue_unless_running` instead of `perform_later`.

Why this is the smallest reasonable change: it adds one idempotency guard around the
existing enqueue point. It does not change the AI service, the model, the persistence
path, routes, authorization, or any view. Intentional regeneration keeps working
because the marker is released the moment the job finishes, and the "Generate again"
button is only shown for a finished ("ready") result.

Design-pattern effect: an idempotency/guard responsibility is added to the existing
background-work coordination, complementing the new Controller (GRASP) coordination
introduced by CH01. The single shared persistence path is preserved: both AI and manual
imports still flow through `TripItemsBulkImport`, which itself continues to enforce the
`TripItem` model validations (duplicates skipped, unknown kinds coerced, invalid raw
URLs skipped). No baseline pattern (P01-P09) responsibility is removed or reclassified.

## 4. Test commands and actual results

Toolchain: Ruby 3.4.2, Rails 8.1.3, Minitest. Run with mise.

Focused CH01 suite (6 files):

    mise exec ruby@3.4.2 -- bin/rails test \
      test/services/itinerary_generator_test.rb \
      test/services/trip_items_bulk_import_test.rb \
      test/controllers/itinerary_generations_controller_test.rb \
      test/jobs/generate_itinerary_job_test.rb \
      test/controllers/trip_items_controller_test.rb \
      test/controllers/trips_controller_test.rb

Result: 41 runs, 139 assertions, 0 failures, 0 errors, 0 skips.

Full suite:

    mise exec ruby@3.4.2 -- bin/rails test

Result: 41 runs, 139 assertions, 0 failures, 0 errors, 0 skips. The repository test
directory contains exactly the six files above, so the full-suite total equals the
focused total.

Changed-file incremental result (this task's four files, controller + job tests):

    mise exec ruby@3.4.2 -- bin/rails test \
      test/controllers/itinerary_generations_controller_test.rb \
      test/jobs/generate_itinerary_job_test.rb

Result: 18 runs, 58 assertions, 0 failures, 0 errors, 0 skips (14 before the four new
regression tests).

RuboCop on changed Ruby files:

    mise exec ruby@3.4.2 -- bin/rubocop --no-color \
      app/jobs/generate_itinerary_job.rb \
      app/controllers/itinerary_generations_controller.rb \
      test/controllers/itinerary_generations_controller_test.rb \
      test/jobs/generate_itinerary_job_test.rb \
      app/services/itinerary_generator.rb

Result: 5 files inspected, no offenses detected.

Whitespace check:

    git diff --check

Result: clean (no output).

New regression tests added for this increment:

- Controller: repeated submissions while a generation is running do not enqueue a
  second job (`assert_enqueued_jobs 1`).
- Controller: regeneration is allowed once a generation has finished (job run clears
  the marker, then a new submit enqueues again).
- Job: `enqueue_unless_running` returns `true` once and `false` thereafter for the same
  trip/user.
- Job: `perform` clears the in-progress marker when it finishes.

Pre-existing (previous CH01 increment) focused baseline for context: 4 CH01 files were
33 runs, 113 assertions before these four tests were added.

## 5. Required metrics

No faculty metrics, thresholds, or CSV columns were specified in the materials
available in the repository, so none are claimed. Only genuinely measured/asserted
quantities are reported:

- Test totals: 41 runs, 139 assertions, 0 failures (focused and full suite).
- Existing job tests assert that a single generation results in exactly one Anthropic
  call (`fake.messages.create_calls.size == 1`), and the new controller/job tests assert
  that a repeated submission adds zero further jobs. This is the measurable basis for
  "no redundant AI work".
- Performance, token count, and cost were not measured.

## 6. Limitations

- Live AI API not tested. All tests use a fake Anthropic client (`test/support/fake_anthropic.rb`);
  no real Claude API request was made. Runtime behavior of the real `anthropic` gem call
  is unverified here.
- Verification method is static source review plus Rails unit, controller, and job
  tests. No browser/end-to-end integration test and no independent human sign-off.
- The duplicate-generation guard is a best-effort cache marker, not an atomic
  database-level lock. Within one process the marker prevents redundant enqueues; two
  truly concurrent requests in separate processes could still race before the marker is
  written. The marker TTL (5 minutes) is only a safety net if a job never runs.
- CH02 and CH03 were not started; frozen P01-P09 baseline artifacts were not modified.

## 7. Combined-tree reconciliation (Member 3 final)

Added during final packaging. This file records CH01 at its own completion time. The
statements above that CH02/CH03 were "not started" and that the test directory held
exactly six files were true when CH01 was verified and are superseded as follows:

- CH02 and CH03 are now implemented and have their own evidence files
  (`CH02_Multiple_Booking_Providers.md`, `CH03_Different_Cancellation_Policies.md`).
- The test directory now contains ten `*_test.rb` files. The full combined suite is
  65 runs / 204 assertions, 0 failures, 0 errors, 0 skips (see the final verification
  record in `Member3_Evolution_Report.md`).
- No CH01 source, test or evidence claim above was altered by CH02/CH03; the CH01 anchors
  remain correct in the combined tree.
