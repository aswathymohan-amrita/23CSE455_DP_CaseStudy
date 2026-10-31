# Required feature CH01 — Related article recommendations

> This file documents the required Part 2 feature. The original `requirement.md`, `implementation.md`, and evidence files in this folder are retained as historical evidence for the separate provider-inference refactoring at commit `e7dfd1c`.

## Requirement and acceptance criteria

Show relevant articles on a public article page using existing metadata. Do not recommend the current article, drafts, unapproved content, or unrelated articles. Rank shared tags more strongly than a shared category, resolve ties consistently, and limit the number of results.

## Merged implementation

Application repository: https://github.com/nivedita-rmsh/nextjs-blog-cms  
Merged feature commit: [`cd435883322dc29da6943fc871dd40cb1c662299`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/cd435883322dc29da6943fc871dd40cb1c662299)

- `features/posts/recommendations.ts`: `rankRelatedPosts()` scores each shared tag as 2 and a shared category as 1, filters out the current article and candidates that are not both published and approved, removes zero-score candidates, orders by score and then publication recency, and applies the limit (default 3).
- `features/posts/components/RelatedPosts.tsx`: loads candidate posts and renders the recommendation list when there are results.
- `app/(public)/blog/[slug]/page.tsx`: mounts the related-article component on the article detail page.
- Focused test: `__tests__/features/posts/recommendations.test.ts`.

## Verification record

The focused test file contains 4 test cases: tag-vs-category ranking, exclusion of the current article/drafts, relevance and result limit, and empty results. **Fresh rerun result: BLOCKED.** Attempted to clone the application repository to run the focused test; the environment could not resolve github.com (DNS/network failure), so no test process ran and no pass/fail test count can honestly be reported. A historical development run reported 4 focused cases passing, but a separate pre-commit run also reported two author-byline failures; neither historical result is a substitute for the fresh merged-snapshot run.

## LOC record

Counting rule: non-empty physical lines; blank lines excluded; comments included. Source snapshot: merged feature commit above.

| File | Non-empty lines | Measurement |
|---|---:|---|
| `features/posts/recommendations.ts` | 44 | Added production module; baseline file count 0 |
| `features/posts/components/RelatedPosts.tsx` | 21 | Added UI component; baseline file count 0 |
| `__tests__/features/posts/recommendations.test.ts` | 73 | Test LOC, recorded separately |

See `B14/Part2/loc_measurements.csv` for the canonical measurement table.

## Pattern effect

No new GoF pattern is claimed. The ranker is a deterministic helper, not a family of interchangeable ranking strategies. The existing Strategy, Observer and RBAC instances are treated as preserved.
