# CH01 - Premium content and a new subscription plan (Ultra)

**Commits:** before `d68c773` (baseline source + test harness, no production change) -> after `3f79642`
**Reproduce:** `git checkout 676e5dd && git am ../../../data/test_result/part2/0001-*.patch 0002-*.patch`
**Files:** `change.diff`, `diffstat.txt` (22 files, +642 / -186 incl. tests), `test_result.log`, `typecheck.log`

## Requirement
1. Introduce a new plan **Ultra** (tier 5, 12.99/month, 4K+HDR, all devices, up to **7 profiles**).
2. Introduce **premium content**: titles from the originals row (TMDB network 213) are premium
   and can only be played on **Standard, Premium or Ultra** (tier >= 3).
3. A viewer without the right plan still sees premium titles but gets an **"Upgrade to watch"**
   button (link to /login/plans) instead of Play, with an explanation.

## Acceptance criteria (all automated, `tests/ch01-premium-plan.test.ts`)
| # | Observable result | Test |
|---|---|---|
| A1 | Plan list is Mobile, Basic, Standard, Premium, Ultra; Ultra = tier 5, 7 profiles, 12.99 | "offers five plans including Ultra" |
| A2 | UI plan cards and server plan list contain the same names, prices, resolutions, devices | "UI and server plan lists cannot drift apart" |
| A3 | Premium title: tiers 0-2 -> `PREMIUM_REQUIRED` (locked); tiers 3-5 -> allowed | `it.each` 6 cases |
| A4 | Basic subscriber calling `catalogue.checkAccess` on a premium title is denied; Standard is allowed; anonymous -> `UNAUTHORIZED` first | 3 tRPC tests |
| A5 | Ultra account can create 6th and 7th profile, 8th is refused "You can only have 7 profiles"; Standard keeps 5 | 2 tests |
| A6 | Only the originals row is tagged `isPremium` | facade test |
| A7 | All baseline characterization tests still pass | characterization*.test.ts |

**Result:** `vitest run` -> **29/29 passed**, `tsc --noEmit` -> pass (logs in this folder).

## Implementation
- `src/config/plan-catalog.ts` (new): client-safe plan catalogue with `tier`, `maxProfiles`.
- `src/config/plans.ts`, `src/config/subscriptions.ts`: now *derived* from the catalogue.
- `src/env.mjs`, `.env.example`: optional `STRIPE_ULTRA_PRICE_ID`.
- `src/lib/access/{types,rules,policy}.ts` (new): `AccessRule` chain + `PremiumContentRule`.
- `src/server/api/trpc.ts`: middleware `attachSubscription`, `subscribedProcedure`.
- `src/server/api/routers/catalogue.ts` (new) + `root.ts`: `catalogue.checkAccess`.
- `src/server/api/routers/profile.ts`: limit from `ctx.maxProfiles`.
- `src/lib/fetchers.ts`: originals row tagged `isPremium`.
- `src/components/show-modal.tsx`: PREMIUM badge, upgrade button, denial message.
- `src/app/api/users/stripe/route.ts`: 400 for a plan without a Stripe price.
- Test fixture note: `tests/helpers.ts` fakePrisma.user.findFirst now returns a plan-less
  user row instead of `null` (a signed-in user always has a row; the new middleware reads it).
  No assertion of the characterization tests was changed.

## Pattern effects
| Instance | Status | Reason |
|---|---|---|
| Authenticated Procedure Pipeline (CoR) | **extended** | new ConcreteHandler `attachSubscription` linked after `enforceUserIsAuthed` |
| API Router Tree (Composite) | **extended** | new sub-composite `catalogueRouter` (leaves 19 -> 20) |
| TMDB Catalogue Facade | **modified** | facade tags premium rows; interface unchanged |
| Content Access Rule Chain (CoR) | **newly introduced** | student-added; first handler `PremiumContentRule` |
| Access Rule Evaluation Template (Template Method) | **newly introduced** | `AccessRule.check` template + abstract `evaluate` |
| Environment Secret Guard (Proxy) | preserved | unchanged; explains why plan data had to be split (see refactoring) |
| tRPC API Front Controller (Front Controller) | **extended** | new command `catalogue.checkAccess` registered in `appRouter`, reached through the same `/api/trpc` controller |
| tRPC Procedure Builder (Builder) | **extended** | new pre-configured builder `subscribedProcedure = protectedProcedure.use(attachSubscription)`; immutability keeps `protectedProcedure` unchanged |
| tRPC Request Context (Context Object) | **extended** | `attachSubscription` refines ctx with `subscription`, `planTier`, `maxProfiles` |
| TMDB Row Scatter-Gather | preserved | same 8-way fan-out; the gathered originals row is additionally marked `isPremium` |
| all others | preserved | re-measured locations in `Part2/pattern_evalution.csv` |

## Refactoring
- **Smell:** *Shotgun Surgery / Duplicated data.* Plans existed twice: `config/plans.ts` (UI) and
  `config/subscriptions.ts` (server). Adding Ultra would need edits in both plus the `PlansConfig`
  name union. They had already **drifted**: Basic devices were "Phone, Tablet, Computer" in the UI
  but "Phone, Tablet, Computer, TV" on the server. Root cause: the server list reads secret price
  ids through the `env` Protection Proxy, which throws in the browser, so the UI could not import it.
- **Technique:** *Extract shared data (Move Field into a new module) + derive both lists*; the
  server list adds price ids, the UI list adds icons. *Replace Magic Number* `5` in `profile.create`
  with the plan's `maxProfiles` (default 5 = baseline behaviour).
- **Behaviour preservation:** characterization tests for subscription resolution and the profile
  limit pass unchanged; test A2 makes future drift a test failure. Intentional fix: Basic device
  string now matches the UI ("Phone, Tablet, Computer").

## Before / after metrics (lizard 1.24.1, scope `src/`, `.css` excluded; same for all snapshots)
| Measure | Baseline 676e5dd | CH01 3f79642 |
|---|---|---|
| src files / NLOC / functions | 110 / 6694 / 280 | 115 / 6829 / 297 |
| average CCN | 2.31 | 2.35 |
| plan data NLOC (plans + subscriptions [+ catalog]) | 139 (2 files, 4 plans) | 123 (3 files, 5 plans) |
| tRPC pipeline `trpc.ts` NLOC / max CCN | 49 / 3 | 63 / 6 |
| tests | 0 in repo (13/13 characterization at d68c773) | 29/29 |

Max CCN reported 23 -> 25: **tool artefact**. The CCN-25 function is the unchanged "Add to My
List" `onClick` handler in `show-modal.tsx` (body identical, checked); lizard did not detect it as
a separate function in the baseline JSX. The highest CCN that was detected in both
snapshots (SiteHeader, 23) is unchanged.
