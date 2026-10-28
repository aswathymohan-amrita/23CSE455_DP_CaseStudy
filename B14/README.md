# 23CSE455 Design Patterns Case Study: Team B14

**Case study:** Design Pattern Identification and Evolution in a Next.js-Based Digital News and Publishing Application
**Application:** Next.js Blog CMS 

## Students
| Roll number | Name | Batch |
|---|---|---|
| AM.SC.U4AIE23121 | Keziah Suzaine George | AIE |
| AM.SC.U4AIE23139 | Nivedita Ramesh | AIE |
| AM.SC.U4CSE23360 | Soorya Krishna | CSE |
| AM.SC.U4CSE23309 | B R Govind | CSE |

## Application and source
- **Repository:** https://github.com/thepracticalengineer/nextjs-blog-cms.git
- **Baseline commit:** `90ec6565877053ee0e93e9f09dcc7c7213aa4832`
  (Merge pull request #102, 8 Oct 2026)
- **Access date:** 2026-10-10
- **License:** MIT (see `code/LICENSE`)
- **Description:** Full-stack blog CMS with a TipTap editor, Supabase authentication (including MFA), Admin/Author roles, draft and publication workflow, comments, tags and categories, public author profiles, newsletter subscriptions, an AI writing assistant (Claude, Gemini, OpenAI) and a developer REST API.

## Environment
| Item | Version |
|---|---|
| OS | Windows (PowerShell) |
| Node.js | 24.14.0 (repo asks for 24.21.0; mismatch noted, nothing failed) |
| pnpm | 10.29.3 (via corepack) |
| Next.js | 16.3.8 (App Router) |
| React | 19.3.0 |
| TypeScript | 6.0.3 |
| Database / Auth | Supabase (`@supabase/supabase-js` 2.117.2, `@supabase/ssr` 0.12.7) |
| State | Zustand 5.0.15 |
| Validation | Zod 4.6.5 |
| Tests | Vitest 5.0.3, Playwright 1.63.0 |

## Source copy in `code/`
Copied from the clone at the baseline commit with robocopy. Excluded from the copy: `node_modules`, `.next`, `.git`, `.agents`, `.claude`. Deleted after copying: `.husky/`, `.github/` (tooling and CI), `tsconfig.tsbuildinfo` (generated cache), `package-lock.json` (created by an accidental `npm install`; the project uses pnpm). Everything else is unchanged.

This source copy already includes the app's AI writing assistant and its developer documentation about coding agents. Those documents belong to the original project at the baseline commit. The team's pattern analysis and Part 3 examples are outside `code/`.

## Run and test results (baseline)
Run from the cloned repository at the baseline commit.

| Command | Result |
|---|---|
| `pnpm install --frozen-lockfile` | Succeeded, 933 packages |
| `pnpm run test:run` | 927 of 927 passed in 83 files on the default settings (runs of 71.43 s and 80.10 s). Log: `test_result/test_result_vitest.log` |
| `pnpm exec vitest run --testTimeout=30000 --maxWorkers=2` | **83 test files passed, 927 of 927 tests passed (222.58 s).** Screenshot: `test_result/vitest_summary.png` |
| `pnpm run typecheck` | Passed. Log: `test_result/typecheck.log`. Screenshot: `test_result/typecheck.png` |
| `pnpm run dev` | **Not run** (see limitations) |
| `pnpm run test:e2e` | **Not run** (needs local Supabase) |

**Note on test stability.** Two further default-setting runs on the same Windows machine, made while it was under heavy load, failed with 6 and 12 test failures (130 s and 188 s). Every failure was a 5000 ms timeout in a jsdom UI test, or a follow-on assertion in the same file after a timeout. The repository sits in a OneDrive-synced folder. With a 30 s timeout and 2 workers, the same code passed 927 of 927. The failures were timing-related, not defects in the application.

stderr lines in the test logs (for example "Resend API error", "Queue unavailable") come from tests that deliberately simulate failures. They are not failures. The `NativeCommandError` text at the top of `test_result_vitest.log` is PowerShell wrapping the test output's stderr, not a test failure.

## Scope of Part 1 pattern discovery
- **Inspected:** `app/`, `components/`, `features/`, `lib/`, `proxy.ts`.
  Files read in full are listed in `Part1/rejected_uncertain.md`.
- **Excluded:** `node_modules`, `.next`, `.git`, `.husky`, `.github`, `.agents`, `.claude`, `docs/`, `public/`, `database/`, `supabase/migrations/`, `e2e/`, `__tests__/`, lockfiles and generated files. Reason: not application logic, or not relevant to pattern discovery. Tests were used only as supporting evidence.

## Part 1 results
| Item | Count |
|---|---|
| Confirmed pattern types | 3 (Strategy, Observer, RBAC) |
| Confirmed pattern instances | 3 |
| Uncertain candidates | 1 |
| Rejected candidates | 7 |

Details: `Part1/patterns.csv`, `Part1/pattern_counts.csv`, `Part1/rejected_uncertain.md`.
Diagrams: `Part1/architecture.*` and `Part1/uml_*.mmd` with matching `.png`.
Numbered source listings used for line ranges: `Part1/evidence/`.

## Rules used
- **Counting:** one row per independent collaboration. Several concrete strategies in one collaboration count as one instance. Rejected and uncertain items are not counted as instances.
- **Participants:** a role may be a function or module. No classes were invented. Where a role is not declared in the code (the Strategy interface) or comes from a dependency (the Observer subject), the CSV says so.
- **Part 3 code lines and complexity:** I used Lizard 1.24.1. The count leaves out blank lines, comments and tests. Results are in `Part3/evidence/static_metrics.json`.
- **Part 3 run time:** I ran each program once to warm it up, then timed it five times. The time includes starting the program and reading its JSON input. All times are in `Part3/evidence/timings/process_timings.json`.

## Part 2

Nivedita's change records, source commit map and test evidence are in `Part2/`.
Read `Part2/HANDOFF.md` for the remaining scope and evidence checks.

## Part 3

Govind's Python and JavaScript examples and Soorya's Java and C++ examples are
in `Part3/`. See `Part3/README.md` for code paths, test commands and results.
The two sets use different test inputs, so the team still needs to check all
four languages against one shared specification. `data/cross_language.csv`
currently contains Govind's measured rows; Soorya's separate rows are in
`Part3/cross_language.csv` until the comparison is reconciled.

## Limitations
- Docker is not installed on the analysis machine, so local Supabase and the running app were not available. Behavior was verified from source and the unit-test suite only.
- Node 24.14.0 was used instead of the requested 24.21.0.
- Playwright end-to-end tests were not run.
- Default-setting unit-test runs were unstable under machine load (see the note on test stability above).
- The Strategy instance has no declared interface and selects by an if-chain. The Observer subject belongs to a dependency (Supabase). RBAC is an architectural pattern, not GoF.
- `proxy.ts` is recorded as Uncertain.

## LLM use
Part 1 analysis used an LLM chat assistant. Exact prompts: `Part1/Part1_prompt.txt`. Evaluation of each analysis against the source: `Part1/llm.csv`.
Part 3's saved Govind prompt and partial verification record are in `Part3/llm/`. The full raw output, displayed model name and interaction date were not archived, so those fields are marked unavailable in `Part3/llm/llm.csv`.
