# Part 2 handoff — Team B14

## Current status

The team repository now contains both the original Part 1 baseline snapshot and a changed-file snapshot for the evolved Part 2 feature implementation. The full runnable application remains in the application repository.

- **Team repository:** https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy
- **Part 2 directory:** https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy/tree/main/B14/Part2
- **Full application:** https://github.com/nivedita-rmsh/nextjs-blog-cms
- **Application feature merge:** [`cd435883322dc29da6943fc871dd40cb1c662299`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/cd435883322dc29da6943fc871dd40cb1c662299)
- **Application PR #1:** https://github.com/nivedita-rmsh/nextjs-blog-cms/pull/1
- **Case-study feature snapshot PR #2:** https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy/pull/2
- **Case-study snapshot merge:** [`691e13ae50ed6e087a224b8e7904fa3f512037b4`](https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy/commit/691e13ae50ed6e087a224b8e7904fa3f512037b4)
- **Latest known case-study main commit before this handoff update:** [`457cb327d5da7bd4f8ef1f717243a88b7f439e44`](https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy/commit/457cb327d5da7bd4f8ef1f717243a88b7f439e44)

## Required feature scope and implementation

The master prompt specifies:

| Change | Required feature | Current source evidence |
|---|---|---|
| CH01 | Related article recommendations | `evolved-code/features/posts/recommendations.ts`, `evolved-code/features/posts/components/RelatedPosts.tsx`, `evolved-code/__tests__/features/posts/recommendations.test.ts` |
| CH02 | Content moderation | `evolved-code/features/posts/moderation.ts`, `evolved-code/features/posts/moderation-actions.ts`, `evolved-code/components/dashboard/ModerationQueue.tsx`, moderation migration and tests |
| CH03 | Subscription/paywall access control | `evolved-code/features/premium/access.ts`, premium access migration and tests |

The `evolved-code/` directory is a changed-file snapshot, not a standalone runnable Next.js application. Use the full application repository for installation, environment configuration, execution and verification. The presence of tests does not itself prove they passed.

## Historical refactoring work (separate from the required feature scope)

The following commits document earlier refactorings and should not be confused with CH01–CH03 feature implementations:

| Refactoring | Branch | Commit |
|---|---|---|
| Provider inference helper | `part2/ch01-provider-refactor` | [`e7dfd1c`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/e7dfd1c) |
| Publication validation helpers | `part2/ch02-publishing-workflow` | [`7be15fb`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/7be15fb) |
| Shared generated-post JSON parser | `part2/ch03-json-parsing-refactor` | [`6ce7157`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/6ce7157) |
| Related article recommendations (earlier feature branch) | `part2/ch01-article-recommendations` | [`68cd127`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/68cd127) |

## Pattern analysis and counts

- `pattern_evolution.csv` now includes a record for the merged feature snapshot as well as the earlier snapshots.
- `Pattern_count.csv` now includes counts for the merged feature snapshot.
- The three confirmed pattern/architecture instances tracked are the implicit LLM Provider Streaming Strategy, Auth State Observer and RBAC Permission Table.
- The current feature additions do not, by themselves, establish another GoF pattern. The moderation states use explicit workflow/state checks; do not label them the GoF State pattern without evidence of state-specific objects and delegated behavior.
- The original RBAC permission-table implementation remains; the premium entitlement and moderation authorization checks are additional feature-specific access gates.
- Source locations in the CSV should be interpreted against the named source version/commit. The evolved snapshot includes changed files only, so unchanged participants may be located in the full application repository.

## LOC measurements

See [`loc_measurements.csv`](https://github.com/nivedita-rmsh/23CSE455_DP_CaseStudy/blob/main/B14/Part2/loc_measurements.csv).

- Counts use non-empty physical source lines; blank lines are excluded and comments are included.
- Refactoring measurements cover the selected production source file only, not the entire repository.
- New feature modules are recorded as added source files with a baseline count of zero; test and SQL migration lines are listed separately.
- LOC is a size measure, not a quality measure. These counts do not establish maintainability or correctness by themselves.

## Test and verification caveats

- Existing evidence logs report results for earlier commits, not a fresh test run performed during this documentation update.
- Change 1's focused after-test log was overwritten during the recommendations branch work; its full-suite log reports 1,025 tests across 88 files, but the focused result should be rerun on `e7dfd1c` before claiming branch-specific verification.
- Change 2's evidence records 30 targeted publication tests and a full-suite result of 1,022 tests across 88 files.
- Change 3's full-suite log reports 1,022 tests across 88 files; confirm focused-log branch context before presenting it as proof for `6ce7157`.
- Two existing author-byline tests failed when the pre-commit hook ran on the recommendations branch; this failure remains a known caveat.
- Local Supabase/Docker and end-to-end testing were previously unavailable. Database migrations and server-side access rules still need verification in a configured environment.
- Do not claim that tests pass now unless they are rerun and the actual output is archived.

## Other deliverables and remaining checks

- `Part2_prompt.txt`: retained master prompt.
- `code/README.md`: describes the baseline and evolved source snapshots.
- `changes/Change1`, `Change2`, `Change3`: requirements, implementation notes and evidence. The historical refactoring records remain useful but are distinct from the required feature scope.
- `diagrams/pattern-evolution.mmd`: editable diagram source. Render it if the report requires an image.
- `llm.csv`: AI-use record; raw model transcripts were not separately archived, and this limitation must remain explicit.
- Update and regenerate `B14_Report.pdf` if the report source changes.
- Review the final commit and ensure it is on the team repository's `main` branch before submission.
