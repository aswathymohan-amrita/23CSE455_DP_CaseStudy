# 13 Context Object - tRPC Request Context

Source instance: **tRPC Request Context** (`createTRPCContext` / `createInnerTRPCContext`, refined by
`enforceUserIsAuthed` and the CH01 middleware `attachSubscription`; region added in CH02).

- `createContext(headers)` (per HTTP request) reads the session and the region **once** and calls
  `createInnerContext(session, region)`, which returns the protocol-independent object `{session, db, region}`
  (tests may call it directly - inputs starting with `inner:`).
- Region: first non-empty header of `x-vercel-ip-country`, `cf-ipcountry`; normalised by trim + upper-case;
  anything that is not two letters (or no header) -> `US`. An invalid first header does **not** fall
  through to the second one (same as `regionFromHeaders`).
- Middlewares return a refined **copy**: `enforceUserIsAuthed` (no session -> `UNAUTHORIZED`),
  `attachSubscription` adds `subscription`, `planTier`, `maxProfiles` from the fake database
  (`u1` Premium tier 3 max 5, `u2` Mobile tier 1 max 2, others: no plan, tier 0, max 5).
- Procedures read only the context: `whoami` (protected) -> session, `region` (public) -> region,
  `plan` (protected + subscription) -> `tier=<t>,max=<m>`.

## Input / output
Input: `<k=v[,k=v...]|-|inner:user:region>|<procedure>`.
Output: `<result>;keys=<sorted keys of the context the resolver received>` or `ERROR:UNAUTHORIZED`.
