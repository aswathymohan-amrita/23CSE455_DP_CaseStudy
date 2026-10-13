# Member 3 - Software Evolution / Refactoring Report (Faculty Part 2)

Project: DaPlanStan (Rails 8.1.3)
Frozen BEFORE source version: `baseline` (Member 2 Part 2 package, P01-P09)
Working branch: `member3/part2-submission`, HEAD `d190cf7e3c11321039f24c264462f14224564132` (current local repository state)
Scope: Member 3 / Faculty Part 2 only. CH01, CH02 and CH03 are implemented and audited.
All changes are uncommitted.

## 1. Purpose and method

This report records the AFTER state of the three evolution scenarios against the unchanged
BEFORE inventory. It does not re-open or re-count the frozen baseline.

Method: read the actual source, tests, migrations and the three scenario evidence files;
compare each baseline collaboration against the evolved tree by file and line; run the
full and focused test suites, RuboCop, `git diff --check`, `db:migrate:status`, Brakeman,
bundler-audit and importmap audit. Every status below is supported by a source location in
`patterns_evolution.csv`.

Authoritative inputs actually available:

- `handoff/Part2_to_Software_Evolution_Handoff.md` (from the Member 2 package) - names the
  three scenarios, the five baseline statuses ("preserved, modified, extended, replaced or
  removed"), requires new patterns to be recorded separately, and names
  `patterns_evolution.csv`.
- `patterns.csv` and `pattern_counts.csv` - the frozen baseline schema and counts.
- The frozen baseline counts: 9 instances, 3 distinct types (Controller 6, Information
  Expert 1, Observer 2).

Requirements and submission format are governed by the supplied faculty instructions
and report template. This report documents the three evolution scenarios, pattern effects,
tests, metrics, refactoring evidence and provenance. The source-version count dataset and
its per-snapshot summary must remain consistent with the faculty's requirements for
pattern types, instances, concrete participant classes and rejected/uncertain observations.
The final team integration must also follow the required team-folder hierarchy.

## 2. Evolution status inventory

`FR` = frozen baseline instance. `NEW` = introduced by Member 3.

| ID | Baseline instance | Type | Status | Main AFTER evidence |
|---|---|---|---|---|
| P01 | Parsed Email to Trip Record Linking | Information Expert (GRASP) | modified | `app/models/inbox_item.rb:90,169-189,198-206` |
| P02 | Inbound Travel Email Intake Coordination | Controller (GRASP) | preserved | `app/mailboxes/trip_mailbox.rb` (unchanged) |
| P03 | Trip Creation Coordination | Controller (GRASP) | preserved | `app/controllers/trips_controller.rb:2,110-119` |
| P04 | Trip Membership Management Coordination | Controller (GRASP) | preserved | `app/controllers/trip_members_controller.rb` (unchanged) |
| P05 | Bulk Itinerary Import Coordination | Controller (GRASP) | modified | `app/controllers/trip_items_controller.rb:31-34`; `app/services/trip_items_bulk_import.rb:15-69` |
| P06 | OAuth Sign-in and Identity Linking Coordination | Controller (GRASP) | preserved | `app/controllers/sessions_controller.rb` (unchanged) |
| P07 | Account Traveler Enrollment Coordination | Controller (GRASP) | preserved | `app/controllers/travelers_controller.rb` (unchanged) |
| P08 | Outbound Mail Delivery Logging | Observer (GoF) | preserved | `config/initializers/mail_logger.rb` (unchanged) |
| P09 | Trip-Scoped Turbo Refresh Notifications | Observer (GoF) | extended | `app/jobs/generate_itinerary_job.rb:76-87`; `app/views/itinerary_generations/show.html.erb:4` |
| NEW-01 | Personalized Itinerary Generation Coordination | Controller (GRASP) | introduced | `app/controllers/itinerary_generations_controller.rb:5-43`; `config/routes.rb:41-43` |

Frozen baseline counts are unchanged: 9 instances, 3 distinct types. NEW-01 is counted
separately and is not added to the frozen baseline total.

### Why the statuses are what they are

- **P01 modified.** CH02 changed the existing booking branch of `InboxItem`: the provider is
  normalized and the derived item name now folds in provider + booking type + location
  (`app/models/inbox_item.rb:171-173,198-206`), so two same-provider bookings no longer
  collapse onto one item. A missing provider is backfilled on an already-linked item
  (`:90`). The collaboration still interprets the parsed email and matches/creates/links
  records, but its matching key changed, so this is a modification, not a pure extension.
- **P05 modified.** CH01 moved the batch persistence method out of the controller into
  `TripItemsBulkImport` (`git diff` deletes `bulk_create_items` from
  `app/controllers/trip_items_controller.rb`; the new service is at
  `app/services/trip_items_bulk_import.rb`). The import use case and its observable
  behaviour are unchanged, but the persistence responsibility now sits with a new
  participant, so the collaboration is modified, not replaced.
- **P09 extended.** CH01 added a second trip-scoped Turbo notification stream for AI
  generation results (`GenerateItineraryJob#broadcast`,
  `app/jobs/generate_itinerary_job.rb:76-87`; subscription at
  `app/views/itinerary_generations/show.html.erb:4`) using the same framework-mediated
  Turbo/Action Cable mechanism. The original trip-refresh stream is preserved, so P09 is
  extended rather than replaced or removed.
- **P03 preserved.** `TripsController#set_editable_trip` was extracted to the new
  `EditableTripScoped` concern, but that concerns the edit/update actions; the
  trip-creation coordinator and its owner-membership behaviour are unchanged.
- P02, P04, P06, P07, P08 have no source change in the evolved tree (they are absent from
  `git status`), so they are preserved.

## 3. Newly introduced patterns

One new instance is claimed, of a pattern type already present in the baseline.

**NEW-01 - Controller (GRASP) - Personalized Itinerary Generation Coordination**
(`ItineraryGenerationsController`, `app/controllers/itinerary_generations_controller.rb:5-43`;
routes `config/routes.rb:41-43`). It is a system-event coordinator of the same GRASP
Controller type as P02-P07: it handles the generate (`create`), preview (`show`) and
`confirm` events, enforces owner/planner authorization through `EditableTripScoped`, delegates
the AI call to `GenerateItineraryJob`, and delegates persistence to `TripItemsBulkImport`.
The duplicate-generation guard (`GenerateItineraryJob.enqueue_unless_running`) is a small
idempotency helper inside that coordination, not claimed as a separate pattern.

## 3.1 Updated pattern counts by source version

The required `Pattern_count.csv` uses the faculty's four-column schema
(`source_version,summary,pattern_name,count`). It contains per-pattern counts,
distinct pattern-type totals and instance totals for all four source versions.

The following supplemental measures are recorded here because the four-column
CSV schema does not contain fields for participant-class counts or rejected and
uncertain observations.

| Source version | Pattern instances | Distinct pattern types | Distinct app-defined class names referenced in participant-role descriptions | Rejected/uncertain candidate observations |
|---|---:|---:|---:|---|
| Original code | 9 | 3 | 25 | Not verifiable: the baseline candidate-review register was not found in the current package |
| Code after Change1 | 10 | 3 | 28 | 4 CH01-related candidates, counted retrospectively from the current report |
| Code after Change2 | 10 | 3 | 28 | 5 cumulative Member 3 candidate records, counted retrospectively from the current report |
| Code after Change3 | 10 | 3 | 28 | 6 cumulative Member 3 candidate records, counted retrospectively from the current report |

**Participant-class counting rule:** count distinct application class names that
appear in a snapshot's `participant_roles` entries and match class declarations
under that snapshot's application source. Framework classes, functions, modules,
views and dependencies are excluded. The reported numbers were obtained by a
scripted name match; they are provisional until participant mappings are manually
reviewed. CH02 and CH03 introduce value modules rather than new class declarations,
which is consistent with the unchanged class-name count.

**Rejected/uncertain observations:** the four, five and six entries above are
retrospective cumulative counts of the candidate categories listed in section 4,
attributed to the scenario in which each candidate arose. They are not recovered
historical LLM observations. The original-code count remains unavailable because
the baseline candidate-review register was not found in the supplied package.
Do not interpret the unavailable baseline value as zero.

The available source archive retains only the original and final source trees.
Consequently, the Change1 and Change2 rows are reconciled against the staged
evolution records and scenario evidence, not independently preserved intermediate
source snapshots.

## 4. Evaluated and rejected new-pattern candidates

Mirroring the baseline's rejected-candidate discipline, the following additions were
checked and deliberately not counted as new design patterns:

| Candidate | Reason not counted |
|---|---|
| `BookingProvider` value module (`app/models/booking_provider.rb`) | A plain normalization lookup table (alias -> canonical string). No interchangeable algorithm or incompatible-interface translation; same reasoning as the baseline's rejected geocoding Adapter/Strategy. |
| `CancellationPolicy` value module (`app/models/cancellation_policy.rb`) | A three-entry policy table plus one pure `evaluate` calculation, stored on the model. It is not an interchangeable-strategy object graph; calling it a GoF Strategy would overclaim. |
| `ItineraryGenerator` service (`app/services/itinerary_generator.rb`) | A single AI boundary that builds a prompt, validates output and never persists. One fixed implementation, no family of interchangeable algorithms. |
| `GenerateItineraryJob` background job (`app/jobs/generate_itinerary_job.rb`) | Background execution; the baseline already treats Active Job as framework infrastructure, not as a pattern instance. |
| `TripItemsBulkImport` service (`app/services/trip_items_bulk_import.rb`) | Substantive but a single extracted batch-persistence operation shared by two callers; treated as a participant of the modified P05/New-01 collaborations rather than an independent Information Expert instance. |
| Turbo result broadcast for AI generation | Folded into P09 as an extension of the same framework-mediated Observer mechanism; not double-counted as a separate Observer instance (alternative reading noted below). |

Alternative reading, explicitly not adopted: the AI result stream could be argued to be a
second Observer instance distinct from P09 because it uses a different stream key. The
conservative choice is to treat it as an extension of P09 and count only one new pattern
(NEW-01). This is recorded so the decision is auditable rather than hidden.

## 5. Baseline preservation checks

- The frozen files `patterns.csv`, `pattern_counts.csv`, the nine Mermaid sources, the nine
  SVGs and `verification/Part2_Verification_Evidence.md` were not modified.
- `MISSION.md` was not modified.
- The Member 3 working tree contains no edits to the baseline extraction under
  `~/projects/daplanstan-member3/baseline/`.
- `Gemfile` and `Gemfile.lock` are unmodified (absent from `git status`).

## 6. Verification runs (this session)

### Fresh post-packaging test run — 2026-10-11

- Source tree: `A1/Part2/code`
- Command: `RAILS_ENV=test mise exec ruby@3.4.2 -- ruby bin/rails test`
- Raw output: `A1/Part2/evidence/final_test_run_2026-10-11.txt`
- Result: **65 runs, 204 assertions, 0 failures, 0 errors, 0 skips; exit code 0.**
- The test database was initialized from the checked-in `db/structure.sql` in
  the test environment only. The original test database was backed up outside
  the repository before replacement.
- Tailwind reported an `Invalid empty selector` warning during CSS optimization;
  the test command nevertheless completed successfully.
- Migration status reported all 40 actual migration files as `up`. It also
  displayed a `000 — NO FILE` version entry, which remains a reproducibility
  note to investigate.
- This is a fresh test run, but not a live Anthropic API integration test.
  CH01 tests use a fake client. The result does not establish browser/end-to-end
  coverage or complete formal equivalence with the baseline.



The verification table below contains historical implementation-run results from the earlier `member3/evolution` checkout at HEAD `cd306ec`; it is not the identity of the current submission branch. A separate fresh full-suite run on the packaged evolved source tree is recorded immediately below. Ruby
3.4.2 / Rails 8.1.3 run via `mise`. The test database was NOT reset; the existing test DB
(already carrying the CH02/CH03 columns) was used.

| Check | Command | Result | Exit |
|---|---|---|---|
| Full test suite | `mise exec ruby@3.4.2 -- bin/rails test` | 65 runs, 204 assertions, 0 failures, 0 errors, 0 skips | 0 |
| CH01 focused (6 files) | `... bin/rails test test/services/itinerary_generator_test.rb test/services/trip_items_bulk_import_test.rb test/controllers/itinerary_generations_controller_test.rb test/jobs/generate_itinerary_job_test.rb test/controllers/trip_items_controller_test.rb test/controllers/trips_controller_test.rb` | 47 runs, 160 assertions, 0 failures | 0 |
| CH02 focused (3 files) | `... bin/rails test test/models/booking_provider_test.rb test/models/inbox_item_test.rb test/controllers/trip_items_controller_test.rb` | 17 runs, 50 assertions, 0 failures | 0 |
| CH03 focused (3 files) | `... bin/rails test test/models/cancellation_policy_test.rb test/models/trip_item_test.rb test/controllers/trip_items_controller_test.rb` | 19 runs, 56 assertions, 0 failures | 0 |
| RuboCop (26 changed/new files) | `mise exec ruby@3.4.2 -- bin/rubocop --no-color <26 files>` | 26 files inspected, no offenses | 0 |
| Whitespace | `git diff --check` | clean (no output) | 0 |
| Migration status | `RAILS_ENV=test mise exec ruby@3.4.2 -- bin/rails db:migrate:status` | both new migrations `up` (`20260510000000`, `20260511120000`) | 0 |
| Brakeman (raw) | `mise exec ruby@3.4.2 -- bundle exec brakeman --no-pager --no-exit-on-warn` | Security Warnings: 0, Errors: 0 | 0 |
| Bundler audit | `mise exec ruby@3.4.2 -- bin/bundler-audit check` | vulnerabilities found (see section 7) | 1 |
| Importmap audit | `mise exec ruby@3.4.2 -- bin/importmap audit` | No vulnerable packages found | 0 |

Note: the focused CH01/CH02 totals are larger than when each scenario was first verified
(41 and 14 runs respectively) because the shared `trip_items_controller_test.rb` now also
contains the CH02 and CH03 tests. The full-suite total equals the sum of all ten test files
(65 test methods).

### Test file inventory (10 files, 65 methods)

| File | Methods |
|---|---:|
| `test/services/itinerary_generator_test.rb` | 13 |
| `test/controllers/itinerary_generations_controller_test.rb` | 10 |
| `test/controllers/trip_items_controller_test.rb` | 9 |
| `test/jobs/generate_itinerary_job_test.rb` | 8 |
| `test/models/cancellation_policy_test.rb` | 6 |
| `test/services/trip_items_bulk_import_test.rb` | 6 |
| `test/models/booking_provider_test.rb` | 4 |
| `test/models/inbox_item_test.rb` | 4 |
| `test/models/trip_item_test.rb` | 4 |
| `test/controllers/trips_controller_test.rb` | 1 |
| **Total** | **65** |

### Source LOC metrics (measured 2026-10-11)

The reproducible measurement script is `evidence/measure_source_loc.py`; the
captured output is `evidence/LOC_Metrics_2026-10-11.txt`.

| Metric | Baseline | Evolved (CH01-CH03) | Difference |
|---|---:|---:|---:|
| Ruby files | 103 | 112 | +9 |
| Physical lines in scope | 3,236 | 3,762 | +526 |
| Nonblank/non-`#`-comment lines | 2,480 | 2,842 | +362 |

Scope: Ruby files under `app/`, `config/`, and `db/migrate/`; tests, documentation,
dependencies, and generated files are excluded. The same Python script and counting
rules are used for both snapshots. Physical lines include blank and comment lines.
The nonblank/non-`#`-comment measure is a simple size proxy, **not strict executable
SLOC**: inline comments and comment forms other than lines beginning with `#` may
be counted. Increased LOC reflects the added behavior and collaborators; it does not
by itself demonstrate improved design.

### Refactoring versus functional evolution

`evidence/Refactoring_Evidence.md` records the distinction and its source/test
evidence. The behavior-preserving refactoring candidates are (1) extracting
`TripItemsBulkImport` from controller-owned batch persistence and (2) extracting
shared trip edit authorization into `EditableTripScoped`. CH01's generation workflow,
CH02's provider-aware matching and persistence, and CH03's cancellation policy
behavior are functional changes, not behavior-preserving refactorings as whole
scenarios.

The available final-tree test results support regression confidence, but an identical
baseline test run and raw final test log have not been preserved here. Therefore,
do not claim complete formal behavior equivalence; list the tested behaviors and the
verification limitation honestly.

## 7. Limitations and unresolved items

- **Faculty schema correction.** The earlier draft incorrectly claimed that no official Faculty Part 2 schema was available. The faculty instructions define the LLM record columns and require source-version pattern counts and evolution evidence. The current package includes the evolution registry, count dataset, LLM provenance record, and diagrams. Final integration must still reconcile the exact filename/path spelling in the faculty hierarchy with the team's chosen deliverable names.
- **Live Anthropic API not tested.** All CH01 AI tests use the fake client
  (`test/support/fake_anthropic.rb`); no real Claude request was made and no token/cost
  metrics exist.
- **CH01 duplicate-generation guard is best-effort.** `GenerateItineraryJob.enqueue_unless_running`
  uses a cache marker, not an atomic database lock; two truly concurrent requests in
  separate processes could still race before the marker is written.
- **Bundler audit is red (pre-existing).** The advisory database flags 20 gem/version pairs
  across 147 advisory entries (for example `activestorage 8.1.3`, `rack 3.2.5`,
  `websocket-driver 0.8.0`, and many 2026 advisories for `nokogiri`, `sqlite3`, `faraday`,
  `concurrent-ruby`). `Gemfile` and `Gemfile.lock` are unmodified by Member 3, so none of
  these were introduced here; they are baseline/environment findings and were not remedied
  (remediation would be an unrelated dependency change).
- **No CI verification.** The repository's `config/ci.rb` and `.github/workflows/ci.yml`
  contain no test step; no CI run was executed or observed, so CI is not claimed to pass.
- **No independent human sign-off, no browser/end-to-end test.** Verification is static
  source review plus Rails unit/controller/job tests.
- **`db:test:prepare` unusable in this environment.** The external `sqlite3` CLI is not
  installed and `db:test:prepare` shells out to it. `db/structure.sql` was updated by hand
  to match the two migrations and this consistency was verified with `db:migrate:status`.
- **Baseline Git provenance remains unverified** (as documented by Member 2); the frozen
  baseline is the `baseline` source label, not a verified commit.
- **Evolved UML prepared; human verification pending.** Three diagrams for CH01, CH02
  and CH03 are present under `diagrams/`, with DOT sources and SVG renderings. These are
  newly generated review artifacts, not recovered historical diagrams. A team member must
  verify their participants and relationships against the final source before submission.
  Keep the frozen baseline diagrams unchanged.

## 8. Deliverables (Member 3 / Faculty Part 2)

- `patterns_evolution.csv` - evolution status for P01-P09 plus the new instance NEW-01.
- `Member3_Evolution_Report.md` - this report.
- `REPRODUCTION.md` - reproduction/setup commands.
- `CH01_Personalized_Itinerary_Generation.md`, `CH02_Multiple_Booking_Providers.md`,
  `CH03_Different_Cancellation_Policies.md` - scenario evidence (preserved; reconciled).

- **Pattern-count status.** `Pattern_count.csv` matches the faculty's four-column schema and includes per-pattern, pattern-type and instance totals for all four source versions. Supplemental participant-class and rejected/uncertain counts are documented in section 3.1. The class counts remain provisional pending manual mapping review, and the baseline rejected/uncertain count is unavailable because its source register was not found in this package.
