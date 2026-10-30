# 01 Chain of Responsibility - Content Access Rule Chain

Source instance: **Content Access Rule Chain** (`Part2/code/src/lib/access/rules.ts`, `policy.ts`, state after CH03).
The base class also shows the **Access Rule Evaluation Template** (Template Method: `check` fixed, `evaluate` overridden).

## Rules (fixed chain order: Region -> Maturity -> Premium; first denial wins)
| Rule | Denies when | Result |
|---|---|---|
| Region | licence for the id exists and (allowed list does not contain region, or blocked list contains it). Licences: 550 blocked in `CN`; 1399 allowed only in `US`,`GB`,`IN` | `DENY:REGION_BLOCKED:hidden` |
| Maturity | KIDS: adult or any genre in {27,53,80,10752}; TEEN: adult or genre 27; ADULT/NONE: never | `DENY:MATURITY_BLOCKED:hidden` |
| Premium | premium and planTier < 3 | `DENY:PREMIUM_REQUIRED:locked` |
| none | - | `ALLOW` |

## Input (one case = one TSV line: `id<TAB>input<TAB>expected`)
`input` = `showId;premium;adult;genres;planTier;region;maturity`
- premium, adult: `0`/`1`; genres: comma list or `-`; maturity: `KIDS|TEEN|ADULT|NONE`.

## Error cases
Unknown maturity value -> `ERROR:unknown maturity`.
