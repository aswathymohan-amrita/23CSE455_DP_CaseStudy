# 11 Front Controller - tRPC API Front Controller

Source instance: **tRPC API Front Controller** (`data/code/src/pages/api/trpc/[trpc].ts:8-19`,
`createNextApiHandler` dispatching to `appRouter`, state after CH01 with `catalogue.checkAccess`).

One controller object receives every HTTP request for `/api/trpc/<path>`. It
1. returns `INTERNAL_SERVER_ERROR` without creating a context if the path is missing (route not named `[trpc]`);
2. creates the request context **once per HTTP request** (a batched request `a,b,c` shares it);
3. for each call: looks the path up in the registry (`NOT_FOUND`), applies the protected check
   (`UNAUTHORIZED` if no user), the input check (`BAD_REQUEST` if required input is missing) and
   runs the resolver (an unexpected exception becomes `INTERNAL_SERVER_ERROR`);
4. reports every error once to the `onError` hook (development logger).

Registry: `user.getCurrent`, `profile.getAll` (protected); `profile.getOne`, `myList.getAll`,
`catalogue.checkAccess` (protected, input required; `myList.getAll=boom` makes the resolver throw);
`icon.getAll` (public).

## Input / output
Input: `<user|-> <call[,call...]|->`, call = `path` or `path=input`.
Output: results joined by `|` (`OK:<value>` or `ERROR:<CODE>`), then `;ctx=<contexts created>;logged=<errors logged>`.
