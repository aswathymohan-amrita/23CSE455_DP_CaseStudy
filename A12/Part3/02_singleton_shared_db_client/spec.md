# 02 Singleton - Shared Prisma Database Client

Source instance: **Shared Prisma Database Client** (`data/code/src/server/db.ts:5-16`).

The database module is evaluated once at start-up and again on every hot reload. On load it
reuses the client stored in the process-wide holder (`globalThis.prisma`) or constructs a new one;
outside `production` it stores the client in the holder so later reloads reuse it.
`NODE_ENV` must be `development`, `test` or `production` (env.mjs validation).

## Input
`env;ops` - `ops` is a comma list of `get` (ask the module for the client) and `reload`
(re-evaluate the module), or `-`. Every case starts with a fresh process and one initial load.

## Output
`constructed=<clients constructed>;distinct=<distinct clients returned by get>`
Invalid env -> `ERROR:invalid NODE_ENV`.
