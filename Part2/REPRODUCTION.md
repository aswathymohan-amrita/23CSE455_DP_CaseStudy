# Member 3 - Reproduction and Setup Instructions

Project: DaPlanStan (Rails 8.1.3). Branch `member3/evolution`, HEAD `cd306ec`.
All CH01-CH03 changes are uncommitted in the working tree, so run the commands below
directly in the checkout; no checkout/commit step is required to reproduce.

## Environment

- Ruby 3.4.2, Rails 8.1.3, Minitest 6.x.
- The toolchain is managed with `mise`; prefix Rails commands with
  `mise exec ruby@3.4.2 --` (calling `bin/rails` directly fails in this environment).
- No live external services are needed for the test suite: the Anthropic client is faked
  (`test/support/fake_anthropic.rb`) and Geocoder is stubbed in tests.

## Setup

```bash
bundle install
```

The database schema is SQL (`db/structure.sql`). The external `sqlite3` CLI is not
installed here, and `bin/rails db:test:prepare` shells out to it, so load the test schema
from `db/structure.sql` with:

```bash
rm -f storage/test.sqlite3*
mise exec ruby@3.4.2 -- bin/rails runner --environment=test \
  'sql = File.read(Rails.root.join("db/structure.sql"));
   ActiveRecord::Base.connection.raw_connection.execute_batch(sql);
   m = ActiveRecord::InternalMetadata.new(ActiveRecord::Base.connection_pool);
   m[:environment] = "test";
   m[:schema_sha1] = OpenSSL::Digest::SHA1.hexdigest(sql)'
```

(On a machine that does have the `sqlite3` CLI, `RAILS_ENV=test bin/rails db:test:prepare`
is equivalent.)

## Run the tests

Full suite:

```bash
mise exec ruby@3.4.2 -- bin/rails test
```

Focused suites:

```bash
# CH01 - personalized itinerary generation
mise exec ruby@3.4.2 -- bin/rails test \
  test/services/itinerary_generator_test.rb \
  test/services/trip_items_bulk_import_test.rb \
  test/controllers/itinerary_generations_controller_test.rb \
  test/jobs/generate_itinerary_job_test.rb \
  test/controllers/trip_items_controller_test.rb \
  test/controllers/trips_controller_test.rb

# CH02 - multiple booking providers
mise exec ruby@3.4.2 -- bin/rails test \
  test/models/booking_provider_test.rb \
  test/models/inbox_item_test.rb \
  test/controllers/trip_items_controller_test.rb

# CH03 - different cancellation policies
mise exec ruby@3.4.2 -- bin/rails test \
  test/models/cancellation_policy_test.rb \
  test/models/trip_item_test.rb \
  test/controllers/trip_items_controller_test.rb
```

## Static and schema checks

```bash
mise exec ruby@3.4.2 -- bin/rubocop --no-color
git diff --check
RAILS_ENV=test mise exec ruby@3.4.2 -- bin/rails db:migrate:status
mise exec ruby@3.4.2 -- bundle exec brakeman --no-pager --no-exit-on-warn
mise exec ruby@3.4.2 -- bin/bundler-audit check
mise exec ruby@3.4.2 -- bin/importmap audit
```

Expected: tests green; RuboCop clean; `git diff --check` silent; both new migrations `up`;
Brakeman 0 warnings; importmap clean; bundler-audit reports pre-existing gem advisories
(exit 1) that are unrelated to the Member 3 changes and were not remedied.

## Running the app (optional, not required for the tests)

See `docs/SETUP.md` for the production/self-hosted setup. For a local run:

```bash
cp .env.example .env
mise exec ruby@3.4.2 -- bin/rails db:prepare
mise exec ruby@3.4.2 -- bin/dev
```
