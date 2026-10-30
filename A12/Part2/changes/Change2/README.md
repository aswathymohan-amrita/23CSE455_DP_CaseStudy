# CH02 - Regional restrictions

**Commits:** before `3f79642` -> after `e420dcf`
**Reproduce:** apply `0003-CH02-regional-restrictions.patch` on CH01
**Files:** `change.diff`, `diffstat.txt` (17 files, +499 / -231), `test_result.log`, `typecheck.log`

## Requirement
Titles are licensed per territory. A title may list the only regions where it can be shown
(`allowedRegions`) or regions where it may not (`blockedRegions`). The viewer's region comes from
the hosting geo header (`x-vercel-ip-country`, else `cf-ipcountry`, else default `US`).
Unlicensed titles must **not appear** in any row and must be **refused** if requested directly
(deep link / My List). A region-blocked premium title must be hidden, not offered for upgrade.

## Acceptance criteria (`tests/ch02-region.test.ts`)
| # | Observable result |
|---|---|
| B1 | Region codes normalised (" in " -> IN, invalid -> US); Vercel header wins over Cloudflare |
| B2 | tRPC context built from a request with `x-vercel-ip-country: in` has `region = IN` |
| B3 | Fight Club (550) hidden in CN, allowed in US; Game of Thrones (1399) allowed in IN, hidden in DE; unlisted titles allowed |
| B4 | Premium + region-blocked title in CN -> `REGION_BLOCKED` (not `PREMIUM_REQUIRED`) |
| B5 | `visibleShows` keeps locked premium titles, drops hidden ones |
| B6 | Row titles and order are exactly the baseline ones; every row is filtered for the region |
| B7 | `catalogue.checkAccess` uses ctx.region; without a region it defaults to US |
| B8 | All earlier tests still pass |

**Result:** `vitest run` -> **45/45 passed**, typecheck pass.

## Implementation
- `src/config/regions.ts` (new): licence table (sample data keyed by TMDB id), `normaliseRegion`.
- `src/lib/region.ts`, `src/lib/server-region.ts` (new): region from headers (request / RSC).
- `src/lib/access/*`: `RegionRule`; chain is now `Region -> Premium`; `visibleShows`.
- `src/server/api/trpc.ts`: `region` in the tRPC context. `catalogue.checkAccess` passes it.
- `src/lib/catalogue.ts` (new) + the 4 `(shows)` pages: shared row layout, server-side filtering, Hero filtered.
- `src/lib/fetchers.ts`: refactored (below).

## Pattern effects
| Instance | Status | Reason |
|---|---|---|
| Content Access Rule Chain | **extended** | new ConcreteHandler `RegionRule` linked first |
| Access Rule Evaluation Template | **extended** | new ConcreteClass `RegionRule.evaluate` |
| TMDB Catalogue Facade | **modified** | internal restructuring only, interface preserved |
| others | preserved | locations re-measured || tRPC Request Context (Context Object) | **extended** | ctx gains `region` (resolved once per request by `regionFromHeaders`, normalised in `createInnerTRPCContext`) |
| TMDB Row Scatter-Gather | **modified** | the two hand-written scatter/gather blocks are replaced by one generic `fetchRows` aggregator (same URLs, order, keys, error) |
| Shows Segment Error Boundary | preserved | the error it catches now originates in `fetchRows` (same message) |


## Refactoring
1. **Smell:** *Duplicate Code / Long Method* in `lib/fetchers.ts`. `getShows` had 8 copies of
   `fetch(...)`, an 8-term `!a.ok || !b.ok || ...` condition, 8 `.json()` calls and 8 return
   fields; `getNewAndPopularShows` repeated the same structure 4 times.
   **Technique:** *Replace repeated code with data + Extract Function*: rows are `SHOW_ROWS` /
   `NEW_AND_POPULAR_ROWS`, one `fetchRows` does fetch / ok-check / parse / premium tag.
2. **Smell:** *Duplicate Code* across pages. Home, Movies and TV pages each contained the same
   7-entry `{title, shows}` array (TV page still says "Scary Movies"); adding region filtering
   would have meant three more copies. **Technique:** *Extract Function* `toCategories` +
   `GENRE_ROWS` / `NEW_AND_POPULAR_LAYOUT` constants in `lib/catalogue.ts`.

**Behaviour preservation:** `tests/characterization.test.ts` (getShows URLs, order, keys, error)
and the new `tests/characterization-new-popular.test.ts` were run on the **original** code
(`../../evidence/tests_baseline_characterization.log`, 19/19) and on CH02 (45/45). B6 pins the
row titles. Visible titles are kept as they were (incl. "Scary Movies" on the TV page).

## Before / after metrics (lizard, `src/`)
| Measure | CH01 3f79642 | CH02 e420dcf |
|---|---|---|
| src files / NLOC / functions | 115 / 6829 / 297 | 119 / 6845 / 322 |
| average CCN | 2.35 | 2.25 |
| `lib/fetchers.ts` NLOC / functions / max CCN | 126 / 5 / **9** | 120 / 20 / **3** |
| row pages (4 pages [+ lib/catalogue.ts]) NLOC | 174 | **116** (incl. new module) |
| tests | 29/29 | 45/45 |

The function count of `fetchers.ts` rises because lizard counts each arrow function in
`SHOW_ROWS` (8 one-line `path` lambdas) as a function.
