# CH02 Evidence - Multiple Booking Providers

Project: DaPlanStan (Rails 8.1.3)
Source version: `baseline` (frozen P01-P09 unchanged)
Working branch: `member3/evolution` at `cd306ec`
Scope: CH02 only. CH01 (personalized itinerary generation) was completed earlier and is
preserved. CH03 (different cancellation policies) was not started.

This record is an AFTER note for an extension to existing booking behavior. It does not
modify or re-count the frozen P01-P09 baseline.

## 1. Requirement and observable behavior

Requirement (handoff): "Multiple booking providers" - external integration boundaries,
provider interactions and booking-related data. The handoff describes this only as an
investigation entry point and prescribes no design. The concrete interpretation used
here is the smallest one supported by an actual limitation in the source:

Before CH02, an email-extracted booking's `provider` string was used as the trip item's
`name` and therefore as the item's matching key (`InboxItem#fill_missing_links!`). Two
distinct bookings from the same provider collapsed onto a single item, and the provider
was not stored as data of its own.

Observable behavior after CH02:

- A booking provider is stored as a separate, normalized `provider` attribute on the
  trip item (`trip_items.provider`).
- Known providers are canonicalized regardless of spelling ("booking.com", "Booking",
  "BOOKING.COM" all become "Booking.com"); unknown providers are preserved verbatim so
  bookings from unlisted providers still keep a usable name.
- Multiple bookings made through the same provider no longer collapse: the derived item
  name includes the provider, booking type and location (for example
  "Viator Tour - Colosseum" and "Viator Tour - Vatican Museums" become two items).
- Re-processing the same email stays idempotent: a booking already linked to the email
  is matched and updated rather than duplicated, and a missing provider is backfilled.
- Manual items can set a provider from the trip item form (with a suggestion list of
  known providers), and the detail page shows "Booked via".

## 2. Main files changed

New (CH02):

- `app/models/booking_provider.rb` - plain value module (no database table) that maps
  known provider spellings to a canonical name and preserves unknown ones.
- `db/migrate/20260510000000_add_provider_to_trip_items.rb` - adds `provider` (string)
  to `trip_items`.
- `test/models/booking_provider_test.rb` - normalization unit tests.
- `test/models/inbox_item_test.rb` - booking ingestion, collision, idempotency and
  blank-provider tests.

Modified (CH02):

- `db/structure.sql` - `trip_items.provider varchar` column and the matching
  `schema_migrations` version row.
- `app/models/trip_item.rb` - `provider` length validation (`:29`) and
  `before_validation :normalize_provider` (`:32`, definition `:77`).
- `app/models/inbox_item.rb` - booking branch stores a normalized provider (`:171-173`),
  backfills a missing provider on an existing item (`:90`), derives a distinguishing
  name via `booking_display_name` (`:198`), and uses the normalized provider as the
  expense description fallback (`:184`).
- `app/controllers/trip_items_controller.rb` - permits `:provider` (`:132`). This is the
  only CH02 change in this file; the rest of its uncommitted diff is CH01.
- `app/views/trip_items/_form.html.erb` - provider text field plus a `datalist` of
  known providers (`:107-116`).
- `app/views/trip_items/show.html.erb` - "Booked via" block (`:127-133`).
- `test/controllers/trip_items_controller_test.rb` - three tests: provider create
  (normalized), an over-long provider, and the item page rendering "Booked via".

## 3. Relevant before/after implementation and design-pattern effect

Before:

- `app/models/inbox_item.rb` (booking branch):
  `find_or_upsert.call(booking["provider"], kind, { ... })`. The provider was passed as
  the item `name`, and `find_or_upsert` matched on `name.downcase`, so any two bookings
  sharing a provider name were treated as the same item. No `provider` column existed
  on `trip_items`.

After:

- `app/models/booking_provider.rb:45` normalizes the raw extraction
  (`BookingProvider.normalize`) and `app/models/inbox_item.rb:198`
  (`booking_display_name`) folds provider + booking type + location into the item name,
  which becomes the matching key. This directly removes the same-provider collision.
- `app/models/inbox_item.rb:173` persists the normalized provider as its own attribute.
- `app/models/inbox_item.rb:90` backfills `provider` onto an already-linked item when it
  was missing, keeping the operation idempotent.
- `app/models/trip_item.rb:31` normalizes the provider on every save, so a manual entry
  such as "viator" is stored as "Viator".

Why this is a small, defensible change: it adds one value module and one column, and
changes one branch of one method. It reuses the existing idempotent matching mechanism
(`find_or_upsert`) rather than introducing a second path, does not touch routes, jobs or
the AI boundary, and does not change how bookings are extracted.

Design-pattern effect (baseline relation): the affected baseline collaboration is P01
(Information Expert - Parsed Email to Trip Record Linking, `InboxItem`). CH02 extends
that collaboration's booking responsibility; P01 remains one instance and the frozen
P01-P09 counts are unchanged. No baseline pattern is removed or reclassified. The new
normalization is a small plain module, not claimed as a new design pattern.

## 4. Test commands and actual results

Toolchain: Ruby 3.4.2, Rails 8.1.3, Minitest. Run with mise. The test database is
loaded from `db/structure.sql`.

### Historical results (CH02 standalone, at time of CH02 completion)

Focused CH02 tests (2 new files plus the extended controller test):

    mise exec ruby@3.4.2 -- bin/rails test \
      test/models/booking_provider_test.rb \
      test/models/inbox_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: **14 runs, 39 assertions, 0 failures, 0 errors, 0 skips.**

Full suite (at that time, CH01 + CH02):

    mise exec ruby@3.4.2 -- bin/rails test

Result: **52 runs, 168 assertions, 0 failures, 0 errors, 0 skips.** (Before CH02 the suite was
41 runs, 139 assertions; CH02 adds 11 tests.)

RuboCop on changed Ruby files:

    mise exec ruby@3.4.2 -- bin/rubocop --no-color \
      app/models/booking_provider.rb \
      app/models/trip_item.rb \
      app/models/inbox_item.rb \
      app/controllers/trip_items_controller.rb \
      db/migrate/20260510000000_add_provider_to_trip_items.rb \
      test/models/booking_provider_test.rb \
      test/models/inbox_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: 8 files inspected, no offenses detected.

Whitespace check:

    git diff --check

Result: clean (no output, exit 0).

Migration consistency check:

    RAILS_ENV=test mise exec ruby@3.4.2 -- bin/rails db:migrate:status

Result: `up 20260510000000 Add provider to trip items` (the new migration is present and
up against the structure.sql-loaded schema).

New tests added:

- BookingProvider: canonical normalization (alias, case, whitespace), unknown provider
  passthrough, blank returns nil, known list is unique.
- InboxItem: canonical provider stored with a distinguishing name; two same-provider
  bookings produce two items; re-processing is idempotent; a blank-provider booking is
  still created.
- TripItemsController: create with a provider stores it normalized; an over-long provider
  is rejected (`unprocessable_entity`); the item page renders "Booked via" with the
  provider.

### Combined-tree results (after CH03 added)

The final combined test suite (all 10 test files) yields:

    mise exec ruby@3.4.2 -- bin/rails test

Result: **65 runs, 204 assertions, 0 failures, 0 errors, 0 skips.**

The CH02-focused subset in the combined tree (same 3 files) now yields:

    mise exec ruby@3.4.2 -- bin/rails test \
      test/models/booking_provider_test.rb \
      test/models/inbox_item_test.rb \
      test/controllers/trip_items_controller_test.rb

Result: **17 runs, 50 assertions, 0 failures, 0 errors, 0 skips.**

The increase from 14 to 17 runs reflects additional CH03 tests now present in
`trip_items_controller_test.rb`. All CH02-specific assertions and behavior remain
unchanged.
