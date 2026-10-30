# CH03 - Parental control

**Commits:** before `e420dcf` -> after `f393031`
**Reproduce:** apply `0004-CH03-parental-control.patch` on CH02
**Files:** `change.diff`, `diffstat.txt` (19 files, +536 / -147), `test_result.log`, `typecheck.log`

## Requirement
Every profile gets a maturity rating: **KIDS**, **TEEN** or **ADULT** (default ADULT, so
existing profiles behave as before). It is set on the Edit Profile page.

| Rating | Hidden |
|---|---|
| KIDS | `adult` titles and genres Horror (27), Thriller (53), Crime (80), War (10752) |
| TEEN | `adult` titles and Horror (27) |
| ADULT | nothing |

Restricted titles disappear from rows, the hero banner, search results and My List of that
profile; the server refuses them in `catalogue.checkAccess` and `myList.create`. A profile id of
another account is refused.

## Acceptance criteria (`tests/ch03-parental.test.ts`)
| # | Observable result |
|---|---|
| C1 | 9 rating/signal cases (table above, plus "no profile selected" = unrestricted) |
| C2 | Order region -> maturity -> premium: Kids + premium horror -> `MATURITY_BLOCKED`; same in CN for a CN-blocked id -> `REGION_BLOCKED`; Adult -> `PREMIUM_REQUIRED` |
| C3 | `profileVisibleShows` returns the same array for ADULT/none; filters for KIDS |
| C4 | `checkAccess` with a Kids profile denies horror, allows animation; a foreign profile -> `FORBIDDEN` |
| C5 | Kids profile cannot save a horror title to My List; allowed titles are stored without `genre_ids` |
| C6 | `profile.update` stores `maturityLevel` |
| C7 | All earlier tests pass, incl. new myList update/delete characterization |

**Result:** `vitest run` -> **65/65 passed**, typecheck pass.

## Implementation
- `prisma/schema.prisma`: `enum MATURITY`, `Profile.maturityLevel @default(ADULT)`
  (apply with `npx prisma db push`, as the project has no migrations folder).
- `src/config/maturity.ts` (new); `src/lib/access/*`: `MaturityRule`, chain
  `Region -> Maturity -> Premium`, `profileVisibleShows`.
- `catalogue.checkAccess`: loads the profile (owner check) and passes its rating.
- `routers/my-list.ts`: maturity guard in `create`, refactoring (below).
- `routers/profile.ts`: `maturityLevel` in update. `edit-profile-form.tsx`: rating selector.
- `shows-container.tsx`, `hero.tsx`, `show-modal.tsx`: filter / pass the active profile's rating.
- `types/index.ts` + 4 pages: `maturityLevel` added to the hand-written profile `select`s.

## Pattern effects
| Instance | Status | Reason |
|---|---|---|
| Content Access Rule Chain | **extended** | `MaturityRule` linked between Region and Premium |
| Access Rule Evaluation Template | **extended** | new ConcreteClass `MaturityRule.evaluate` |
| Active Profile Selection (Observer) | **extended** | `Hero` becomes a new observer (selector on `maturityLevel`); ShowsContainer/ShowModal react to it |
| Search Results Broadcast (Observer) | **modified** | observer ShowsContainer filters the broadcast results |
| Persisted Profile Store (Decorator) | preserved | code unchanged; persisted profile now carries the rating (see limitation) |
| others | preserved | locations re-measured |
| second-pass instances (Front Controller x2, tRPC Adapter, Link Chain, Builder, Context Object, Transformer Strategy, DOM listeners, Error Boundary x2, Suspense Boundary, Scatter-Gather, Profile cache) | preserved | files unchanged or only new fields passed through (EditProfileForm `maturityLevel`; cache keys and invalidation unchanged) |


## Refactoring
- **Smell:** *Duplicate Code* in `routers/my-list.ts`: the same 17-field zod object was declared
  twice (create, update); the "load profile with list, else NOT_FOUND" block appeared three times;
  `create`/`update` copied all 17 fields one by one into `data`.
- **Technique:** *Extract Variable* (`showInput`), *Extract Function* (`findProfileWithList`,
  `findShowOrThrow`, `showData`).
- **Behaviour preservation:** `tests/characterization-mylist.test.ts` (update/delete errors and
  written data) was run on the **original** code first (19/19 with the other characterization
  tests) and passes on CH03, together with the baseline myList create/duplicate tests.

## Before / after metrics (lizard, `src/`)
| Measure | CH02 e420dcf | CH03 f393031 |
|---|---|---|
| src files / NLOC / functions | 119 / 6845 / 322 | 120 / 6916 / 328 |
| average CCN | 2.25 | 2.26 |
| `routers/my-list.ts` NLOC | 169 | **114** |
| access chain (`lib/access/*`) NLOC / max CCN | 116 / 7 | 168 / 7 |
| tests | 45/45 | 65/65 |

## Limitations found
- The profile `select` is hand-written in 4 pages (one more Shotgun Surgery spot; not refactored).
- The persisted (sessionStorage) profile keeps the old rating until the profile is chosen again.
- Pre-existing: profile/myList procedures accept any `profileId` without an ownership check
  (only the new `catalogue.checkAccess` checks it). Reported in Findings, not changed here.
