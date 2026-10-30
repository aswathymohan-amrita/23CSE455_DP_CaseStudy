# 09 Proxy - Environment Secret Guard (protection proxy)

Source instance: **Environment Secret Guard** (`data/code/src/env.mjs:92-105`).

RealSubject: the validated environment variables. Proxy: same read interface; on the **client**
any variable whose name does not start with `NEXT_PUBLIC_` is refused; otherwise the read is
forwarded. Missing variables read as `undefined`. Messages (emoji of the source omitted):
- development client: `Attempted to access server-side environment variable '<NAME>' on the client`
- production client: `Attempted to access a server-side environment variable on the client`

Shared fixture variables: `DATABASE_URL=mysql://db`, `STRIPE_API_KEY=sk_test_123`,
`NEXT_PUBLIC_TMDB_API_KEY=tmdb_abc`, `NEXT_PUBLIC_APP_URL=http://localhost:3000`.

## Input / output
`side;NAME`, side = `server`, `client` (development) or `client-prod`.
Output: the value, `undefined`, or `ERROR:<message>`.
