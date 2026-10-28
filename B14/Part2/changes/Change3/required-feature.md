# Required feature CH03 — Subscription/paywall access control

> This file documents the required Part 2 feature. The original `requirement.md`, `implementation.md`, and evidence files in this folder are retained as historical evidence for the separate generated-post JSON parsing refactoring at commit `6ce7157`.

## Requirement and acceptance criteria

Allow premium articles to have a public preview while protecting the full body. Only the author, an administrator or a user with an active, unexpired premium entitlement may retrieve the full content. Anonymous and inactive/revoked/expired users must be denied before the protected body is queried.

## Merged implementation

Application repository: https://github.com/nivedita-rmsh/nextjs-blog-cms  
Merged feature commit: [`cd435883322dc29da6943fc871dd40cb1c662299`](https://github.com/nivedita-rmsh/nextjs-blog-cms/commit/cd435883322dc29da6943fc871dd40cb1c662299)

- `features/premium/access.ts`: `hasPremiumAccess()` checks sign-in, administrator role, entitlement status and expiry; `getPremiumPostBody()` authorizes access before reading the protected body.
- `supabase/migrations/20261012103000_premium_content_access.sql`: adds premium metadata, a protected full-body table, subscription entitlements and database policies.
- The editor, public article page and persistence path integrate the premium flag, preview and protected body.
- Focused test: `__tests__/features/premium/access.test.ts`.

## Verification record

The focused test file contains 6 cases covering anonymous denial, active and expired entitlements, revoked subscriptions/admin access, author access to a protected body and denial before protected content is queried. **Fresh rerun status: pending until the merged-main test command has completed and its output has been recorded.** Unit tests do not verify SQL/RLS or runtime integration.

## LOC record

Counting rule: non-empty physical lines; blank lines excluded; comments included. Source snapshot: merged feature commit above.

| File | Non-empty lines | Measurement |
|---|---:|---|
| `features/premium/access.ts` | 26 | Added production module; baseline file count 0 |
| `supabase/migrations/20261012103000_premium_content_access.sql` | 164 | SQL migration LOC, recorded separately |
| `__tests__/features/premium/access.test.ts` | 66 | Test LOC, recorded separately |

See `B14/Part2/loc_measurements.csv` for the canonical measurement table.

## Scope and pattern effect

This is entitlement-based access control, not a payment/billing system. Active entitlement rows must be provisioned by a separate trusted process. The existing Strategy, Observer and RBAC instances remain; the helper and subscription table do not establish a new GoF pattern.
