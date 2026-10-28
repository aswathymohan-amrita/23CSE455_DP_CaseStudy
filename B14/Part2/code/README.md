# Part 2 code snapshot and commit map

The source snapshot already stored under `B14/code/` is the Part 1 baseline copy, not the evolved application code. The actual evolved code is preserved in the separate application repository and branches below. This map makes those snapshots reproducible without copying multiple full app trees into this report folder.

Application repository: https://github.com/nivedita-rmsh/nextjs-blog-cms

| Work item | Branch | Commit | Changed paths |
|---|---|---|---|
| Baseline for Part 2 refactoring branches | `main` | `de5bc25` | Baseline before these three refactor commits |
| CH01 provider inference refactor | `part2/ch01-provider-refactor` | `e7dfd1c` | `features/ai-assistant/llmService.ts`, `__tests__/ai-assistant/llmService.test.ts` |
| CH02 publication validation refactor | `part2/ch02-publishing-workflow` | `7be15fb` | `features/posts/publication.ts` |
| CH03 shared AI JSON parser refactor | `part2/ch03-json-parsing-refactor` | `6ce7157` | `features/ai-assistant/llmService.ts` |
| Additional feature branch (not counted as one of the three refactor snapshots above) | `part2/ch01-article-recommendations` | `68cd127` | `features/posts/recommendations.ts`, `features/posts/components/RelatedPosts.tsx`, `app/(public)/blog/[slug]/page.tsx`, `__tests__/features/posts/recommendations.test.ts` |

The baseline application snapshot in `B14/code/` is not automatically updated by the external application branches. Use the application commit IDs above to reproduce the changed source. Do not report the Part 1 copied files as containing these evolved changes.

## Scope and naming warning

The original Part 2 prompt listed CH01 article recommendations, CH02 content moderation, and CH03 subscription/paywall access control. The three documented refactoring commits instead cover provider inference, publication validation, and generated-post JSON parsing. Related-article recommendations also exist as a separate feature commit, but no evidence in this folder establishes implementation of content moderation or a premium-content access gate. The team must confirm with the instructor whether the actual refactor scope is accepted. This report does not claim moderation/paywall are implemented.
