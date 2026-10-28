# Part 2 code snapshot and commit map

This repository preserves both the Part 1 baseline snapshot and the evolved Part 2 application source.

## Source locations

- **Baseline copy:** `B14/code/` (original Part 1 application snapshot).
- **Evolved feature source snapshot:** `B14/Part2/evolved-code/` (changed files from the application after the Part 2 feature branch was merged).
- **Full application repository:** https://github.com/nivedita-rmsh/nextjs-blog-cms
- **Application merge commit:** `cd435883322dc29da6943fc871dd40cb1c662299`
- **Application PR:** https://github.com/nivedita-rmsh/nextjs-blog-cms/pull/1

## Implemented Part 2 feature scope

| Change | Feature | Source location |
|---|---|---|
| CH01 | Related article recommendations with relevance ranking | `evolved-code/features/posts/recommendations.ts`, `evolved-code/features/posts/components/RelatedPosts.tsx` |
| CH02 | Content moderation states, admin review queue, and public visibility enforcement | `evolved-code/features/posts/moderation.ts`, `evolved-code/features/posts/moderation-actions.ts`, `evolved-code/components/dashboard/ModerationQueue.tsx`, database migration files |
| CH03 | Premium entitlement checks and server-side protected-body retrieval | `evolved-code/features/premium/access.ts`, premium access migration, and focused tests |

The `evolved-code/` folder contains the files changed by the feature branch and is not a standalone runnable Next.js application. For execution, environment configuration, and dependencies, use the full application repository.

## Tests and verification

Focused Vitest test files for recommendations, moderation, and premium access are included under `evolved-code/__tests__/`. The presence of tests does not establish that they passed. Record actual test, typecheck, lint, build, and database-migration results after running them in the application environment.

## Related historical refactoring branches

The earlier refactoring branches remain separate historical work:
- CH01 provider inference refactor: `part2/ch01-provider-refactor`, commit `e7dfd1c`
- CH02 publication validation refactor: `part2/ch02-publishing-workflow`, commit `7be15fb`
- CH03 shared AI JSON parser refactor: `part2/ch03-json-parsing-refactor`, commit `6ce7157`

These historical refactors are distinct from the feature scope above and should not be conflated with it. The separate Part 3 cross-language examples remain in the Part 3 section.
