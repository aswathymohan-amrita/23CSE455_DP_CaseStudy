# Required feature CH02 — Content moderation

> This file documents the required Part 2 feature. The original `requirement.md`, `implementation.md`, and evidence files in this folder are retained as historical evidence for the separate publication-validation refactoring at commit `7be15fb`.

## Requirement and acceptance criteria

Publication requests must enter administrator review before becoming public. Pending and rejected content must remain unavailable in public views. Editing a live article must return it to review. The rule must be enforced across the editor, public queries and supported REST publication paths, with database-level policies as a further enforcement layer.

## Merged implementation

Application repository: https://github.com/nivedita-rmsh/nextjs-blog-cms  
Merged feature commit: [`cd435883322dc29da6943fc871dd40cb1c662299`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/cd435883322dc29da6943fc871dd40cb1c662299)

- `features/posts/moderation.ts`: defines moderation statuses, publication-request/edit transitions and the public visibility predicate.
- `features/posts/moderation-actions.ts`: administrator-only approve/reject actions, publication validation, stale-row checks and cache/newsletter updates.
- `components/dashboard/ModerationQueue.tsx`: moderation queue UI.
- `supabase/migrations/20261012100000_content_moderation.sql`: moderation column, backfill, database policies and atomic-save behavior.
- Related queries, editor and REST paths enforce or filter the moderation status in the full application repository.
- Focused test: `__tests__/features/posts/moderation.test.ts`.

## Verification record

The focused test file contains 5 cases for draft behavior, publication requests, edits to published posts, retaining pending submissions, and public visibility. **Fresh rerun result: BLOCKED.** Attempted to clone the application repository to run the focused test; the environment could not resolve github.com (DNS/network failure), so no test process ran and no pass/fail test count can honestly be reported. The focused unit tests do not validate the SQL migration, RLS policies or end-to-end moderation workflow; these require a configured Supabase environment.

## LOC record

Counting rule: non-empty physical lines; blank lines excluded; comments included. Source snapshot: merged feature commit above.

| File | Non-empty lines | Measurement |
|---|---:|---|
| `features/posts/moderation.ts` | 10 | Added production helper; baseline file count 0 |
| `features/posts/moderation-actions.ts` | 58 | Added server actions; baseline file count 0 |
| `components/dashboard/ModerationQueue.tsx` | 55 | Added UI component; baseline file count 0 |
| `supabase/migrations/20261012100000_content_moderation.sql` | 114 | SQL migration LOC, recorded separately |
| `__tests__/features/posts/moderation.test.ts` | 28 | Test LOC, recorded separately |

See `B14/Part2/loc_measurements.csv` for the canonical measurement table.

## Pattern effect and limitation

The existing RBAC permission table remains. Moderation adds explicit administrator checks and database RLS; it is not claimed as a new GoF pattern. The feature implements editorial review, not a separate generalized state-object hierarchy. Migration/runtime verification remains distinct from unit testing.
