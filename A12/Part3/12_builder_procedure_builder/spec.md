# 12 Builder - tRPC Procedure Builder

Source instance: **tRPC Procedure Builder** (`t.procedure`, `protectedProcedure = t.procedure.use(enforceUserIsAuthed)`,
`subscribedProcedure` from CH01, routers calling `.input(...).query(...)`; dependency `createBuilder` in
@trpc/server@10.28.0 `dist/index.js:326-438`).

- `ProcedureBuilder` steps: `use(name, middleware)`, `input(parser)` (appends a middleware named `input`),
  and the build steps `query(resolver)` / `mutation(resolver)` which return the product `Procedure`.
- Each step returns a **new** builder; the receiver is never modified.
- `Procedure.call(user, input)` runs the middlewares in the order they were added, recording their names
  (`trace`), then the resolver.
- Middlewares: `auth` (protected base; no user -> `UNAUTHORIZED`), `log`, `timing` (no-ops),
  `input:string` (missing -> `BAD_REQUEST`), `input:number` (not an integer -> `BAD_REQUEST`, normalises the number).
- Resolvers: `echo` (input or `none`), `whoami` (user or `anonymous`).
- A chain without a build step -> `NOT_BUILT`; a step after the build step -> `ALREADY_BUILT`.
- `immutable`: derive `subscribed = protected.use(plan)` and report middleware counts of base/protected/subscribed.

## Input / output
Input: `<base,step,...>;<user|->;<input|->` or `immutable;-;-`.
Output: `<kind>:<result>;trace=<a>b>c|none>`, `ERROR:<CODE>;trace=<middlewares run>`, `ERROR:NOT_BUILT`,
`ERROR:ALREADY_BUILT`, or `base=0;protected=1;subscribed=2`.
