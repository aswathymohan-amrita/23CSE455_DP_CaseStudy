# 23CSE455 Design Patterns Case Study — DaPlanStan

Team repository for the **DaPlanStan** Rails application (Rails 8.1.3, Ruby 3.4.2) Design Patterns case study.

## Project Structure

```
.
├── Part1/                          # Member 1 & 2: Design Pattern Discovery & Verification (FROZEN)
│   ├── patterns.csv                # Baseline pattern inventory (P01–P09)
│   ├── pattern_counts.csv          # Baseline counts: 9 instances, 3 types
│   ├── verification/               # Evidence, UML diagrams, reviewer records
│   └── reference/                  # Faculty instructions & template
├── Part2/                          # Member 3: Software Evolution & Refactoring (THIS DELIVERY)
│   ├── baseline/                   # Frozen BEFORE source (commit cd306ec)
│   ├── code/                       # Evolved AFTER source (working tree at cd306ec + CH01–CH03)
│   ├── changes/
│   │   ├── Change1/evidence.md     # CH01: Personalized Itinerary Generation
│   │   ├── Change2/evidence.md     # CH02: Multiple Booking Providers
│   │   └── Change3/evidence.md     # CH03: Different Cancellation Policies
│   ├── evidence/                   # Per-scenario evidence (copied from changes/)
│   ├── Member3_Evolution_Report.md # Main evolution report
│   ├── Pattern_count.csv           # Before/after pattern counts
│   ├── REPRODUCTION.md             # Setup & verification commands
│   └── patterns_evolution.csv      # Per-pattern evolution status (P01–P09 + NEW-01)
├── Part3/                          # Member 4: Cross-language patterns (NOT IN THIS REPO)
├── data/
│   └── patterns_evolution.csv      # Duplicate of Part2/patterns_evolution.csv
├── reference/                      # Faculty PDFs & LaTeX template
└── README.md                       # This file
```

## Part 2 — Member 3 Deliverables (Complete)

### Implemented Change Scenarios

| Scenario | Description | Pattern Effect |
|----------|-------------|----------------|
| **CH01** | Personalized Itinerary Generation (AI-assisted, Turbo Stream preview, background job) | P05 modified, P09 extended, **NEW-01 introduced** (Controller/GRASP) |
| **CH02** | Multiple Booking Providers (normalization, collision fix, persistence) | P01 modified |
| **CH03** | Different Cancellation Policies (policy evaluation, deadline, penalty) | No baseline pattern affected |

### Pattern Evolution Summary

- **Frozen baseline (Part 1):** 9 instances across 3 types — Controller (GRASP): 6, Information Expert (GRASP): 1, Observer (GoF): 2
- **Evolved snapshot:** 10 instances (9 baseline + NEW-01), same 3 types — Controller (GRASP): 7, Information Expert (GRASP): 1, Observer (GoF): 2
- No baseline pattern was removed or reclassified.

### Verification Results (All Run in This Session)

| Check | Result |
|-------|--------|
| Full test suite (`bin/rails test`) | **65 runs, 204 assertions, 0 failures, 0 errors, 0 skips** |
| CH01 focused (6 files) | 47 runs, 160 assertions, 0 failures |
| CH02 focused (3 files) | 17 runs, 50 assertions, 0 failures |
| CH03 focused (3 files) | 19 runs, 56 assertions, 0 failures |
| RuboCop (132 files) | 0 offenses |
| `git diff --check` | Clean |
| `db:migrate:status` | Both new migrations `up` |
| Brakeman | 0 warnings, 0 errors |
| Importmap audit | No vulnerable packages |
| Bundler audit | **Pre-existing advisories (exit 1)** — 20 gem/version pairs, 147 advisories; `Gemfile.lock` unmodified by Member 3 |

### Known Limitations (Honestly Reported)

- Live Anthropic API not tested (fake client used in tests)
- CH01 duplicate-generation guard is best-effort cache marker, not atomic lock
- Bundler-audit reports pre-existing vulnerabilities — not remediated (out of scope)
- No CI pipeline configured / no CI run executed
- No browser/end-to-end tests, no independent human sign-off
- UML diagrams not updated for evolved patterns (baseline diagrams frozen)
- No official Faculty Part 2 template/schema found — report mirrors Part 1 structure

## Reproduction

From the **working source** (`~/projects/daplanstan-member3/work/daplanstan-main` on branch `member3/evolution`):

```bash
# Setup (uses mise for Ruby 3.4.2)
bundle install

# Load test schema from structure.sql (sqlite3 CLI not available in this env)
rm -f storage/test.sqlite3*
mise exec ruby@3.4.2 -- bin/rails runner --environment=test \
  'sql = File.read(Rails.root.join("db/structure.sql"));
   ActiveRecord::Base.connection.raw_connection.execute_batch(sql);
   m = ActiveRecord::InternalMetadata.new(ActiveRecord::Base.connection_pool);
   m[:environment] = "test";
   m[:schema_sha1] = OpenSSL::Digest::SHA1.hexdigest(sql)'

# Run tests
mise exec ruby@3.4.2 -- bin/rails test

# Static checks
mise exec ruby@3.4.2 -- bin/rubocop --no-color
git diff --check
RAILS_ENV=test mise exec ruby@3.4.2 -- bin/rails db:migrate:status
mise exec ruby@3.4.2 -- bundle exec brakeman --no-pager --no-exit-on-warn
mise exec ruby@3.4.2 -- bin/bundler-audit check
mise exec ruby@3.4.2 -- bin/importmap audit
```

## Team Integration Status

- **Part 1:** Present in `Part1/` (frozen, completed by Members 1 & 2)
- **Part 2:** Complete in `Part2/` (this delivery, Member 3)
- **Part 3:** Not present in this repository (separate Member 4 work)

## Safety Notes

- The `baseline/` and `code/` snapshots are **not byte-for-byte copies** of the original source. Six credential-related files have been **removed from the submission snapshots** to avoid packaging secrets:
  - `Part2/baseline/.kamal/secrets`
  - `Part2/baseline/.kamal/secrets.local.example`
  - `Part2/baseline/config/credentials.yml.enc`
  - `Part2/code/.kamal/secrets`
  - `Part2/code/.kamal/secrets.local.example`
  - `Part2/code/config/credentials.yml.enc`
- These files existed in the source archive but were **excluded from the packaged snapshots**. The original frozen baseline at `~/projects/daplanstan-member3/baseline/daplanstan-main` remains untouched and still contains them.
- No credentials, `.env` files, or local databases were added by Member 3.
- All changes are **uncommitted** in the working source; the team repo snapshots are static copies with the above exclusions.