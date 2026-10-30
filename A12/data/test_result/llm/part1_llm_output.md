# LLM output record - Part 1 (pattern discovery)

- Tool / model: Claude (claude.ai), displayed model **Claude Opus 5.5**; access tier: not recorded.
- Date: 2026-10-10. Prompt: `Part1/Part1_prompt.txt`. Input: repository `sadmann7/netflx-web` at
  `676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258` (copy in `data/code/`) plus the three assignment files.
- Raw transcript: not included; the exact prompts are in `Part1/Part1_prompt.txt`. This file lists the
  claims the model made and what they became after checking.
- The model also wrote files: `Part1/patterns.csv`, `Part1/Pattern_count.csv`,
  `data/test_result/part1/candidates.md`, `Part1/pattern_architecture/*.puml` and the scripts in `data/test_result/part1/`.

## Claims made by the model and their status after verification

| # | Model claim | Evaluation | Evidence / correction |
|---|---|---|---|
| 1 | netflx-web covers user management, catalogue, subscription, authentication strongly; content access and caching partially; recommendation not at all | correct | file inventory in `data/test_result/part1/candidates.md`; no recommendation code found by reading `app/(shows)` and `lib/fetchers.ts` |
| 2 | Repository has no LICENSE file | correct | `ls code/` (no LICENSE); README has no licence section |
| 3 | 10 pattern types / 15 instances (table in report section 2.2) | correct after correction | **first answer listed 14 instances**; on a second pass over `env.mjs` the model found the Environment Secret Guard proxy (`env.mjs:92-105`) and added it |
| 4 | All participant line ranges in `Part1/patterns.csv` | partially correct -> corrected | `verify_locations.py` checked that 90 cited ranges exist and start at the right symbol (0 problems), but it does not check end lines. An independent bracket-matching locator (`data/test_result/part2/locate.py`) later showed **two wrong end lines**: `getShows` 5-78 -> **5-77**, `getUserSubscriptionPlan` 6-50 -> **6-53**. Also one range was wrong at first (`createTrpcNextBeta.tsx:71-116`, an offset error from reading two files at once) -> **48-93**. All corrected in `Part1/patterns.csv`. |
| 5 | `createTRPCNextLayout` (server caching proxy) is dead code | correct | `grep -rn createTRPCNextLayout data/code/src` -> only its own definition |
| 6 | PIN check is done in the browser (`pin-form.tsx:19`) | correct | the profile object incl. `pin` is sent to the client by `profile.getAll`; comparison happens in `handleSubmit` |
| 7 | 18 of 19 procedures use `protectedProcedure` | correct | count of `protectedProcedure` uses in `routers/*.ts` (8 inline + 10 multi-line); `user.getSession` is public |
| 8 | Stripe webhook = Observer | **not accepted** (model itself marked it uncertain) | only the subscriber side is in the code; recorded as uncertain |
| 9 | `app/api/og/route.tsx` etc. excluded as out of scope | correct | Open Graph image generation, no case-study area |

## Human verification
| Reviewer (roll no., name) | Date | Items re-checked against source | Agree / disagree + notes |
|---|---|---|---|
| AM.SC.U4CSE23161, Swaminathan A | 2026-10-30 | Claims 1-9: application coverage, licence, 15 instances, line ranges, dead caching proxy, client-side PIN, protected procedures, webhook, exclusions | Agree; line-range corrections confirmed with `verify_locations.py` and `locate.py` |
| AM.SC.U4CSE23242, Pooja Sathyan | 2026-10-30 | Participant roles of all 15 first-pass records against `data/code/src` | Agree; Stripe webhook kept as uncertain |
