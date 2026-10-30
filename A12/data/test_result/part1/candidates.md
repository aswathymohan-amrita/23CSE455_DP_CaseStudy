# Part 1 - all candidates considered (scope: data/code/src, data/code/prisma/schema.prisma @ 676e5dd)

Method: two passes.

1. **First pass (2026-10-10)** - for each of the seven case-study areas we listed the entry files,
   read them fully, followed every import/call one hop (and into node_modules where a role is
   played by a dependency), and only confirmed a pattern when intent, the role relationships and
   the runtime delegation were all visible in code. Result: 10 types, 15 instances.
2. **Second, exhaustive pass (2026-10-29)** - every in-scope file was read top to bottom, not
   only the entry files of the seven areas, and each was checked against the GoF catalogue plus
   architectural (PoEAA, Core J2EE), concurrency/integration and React/Next.js framework idioms.
   Dependency roles were checked in the exact package versions of `yarn.lock`
   (`npm pack @trpc/server@10.28.0 @trpc/client@10.28.0 @trpc/react-query@10.28.0
   @trpc/next@10.28.0 next-auth@4.22.1 next@13.4.4`). Result: +6 types, +13 instances, one
   correction to an existing record (see below).

Names, comments or an LLM claim alone were never accepted. Line-range check:
`python data/test_result/part1/verify_locations.py Part1/patterns.csv`
(log: `data/test_result/part1/location_check.log`, 156 locations, 0 problems).

| Area | Files inspected |
|---|---|
| User management | server/api/routers/user.ts, profile.ts, icon.ts; components/forms/*; components/manage-profiles.tsx, icon-picker.tsx; stores/profile.ts; app/(dashboard)/* |
| Video catalogue | lib/fetchers.ts; app/(shows)/*; components/shows-*.tsx, hero.tsx, show-modal.tsx, my-shows.tsx, debounced-input.tsx; hooks/*; stores/modal.ts, search.ts |
| Subscription | config/subscriptions.ts, plans.ts; lib/subscription.ts, stripe.ts; app/api/users/stripe, app/api/webhooks/stripe; components/forms/billing-form.tsx, account-form.tsx |
| Recommendation | app/(shows)/page.tsx, new-and-popular/page.tsx, lib/fetchers.ts (only fixed TMDB lists exist) |
| Authentication | server/auth.ts; lib/session.ts; pages/api/auth/[...nextauth].ts; app/api/auth/[...nextauth]/_route.ts; components/login-button.tsx; server/api/trpc.ts |
| Content access | server/api/trpc.ts; components/screens/*; components/forms/pin-form.tsx; app/(shows)/layout.tsx, error.tsx, loading.tsx; app/global-error.tsx |
| Caching | lib/api/api.ts, client.ts; @trpc/next-layout/*; context/trpc-provider.tsx; components/show-modal.tsx + all forms using api.useContext(); next.config.mjs |
| Cross-cutting | env.mjs; server/db.ts; pages/api/trpc/[trpc].ts; server/api/root.ts; app/layout.tsx; config/site.ts; lib/utils.ts, constants.ts; types/index.ts |

Excluded: components/ui/* (shadcn primitives, generated UI kit), styles/, public/, app/(docs)
(static help/terms text), app/api/og (Open Graph image), node_modules except where a role is
mapped.

## Confirmed: 16 types, 28 instances (Part1/patterns.csv)

| Pattern type | Instances | Pass |
|---|---|---|
| Chain of Responsibility | Authenticated Procedure Pipeline; tRPC Client Link Chain | 1; 2 |
| Singleton | Shared Prisma Database Client; Stripe API Client | 1 |
| Observer | Show Modal Selection; Active Profile Selection; Search Results Broadcast; Search Input DOM Event Listeners | 1 (x3); 2 |
| Decorator | Persisted Profile Store | 1 |
| Adapter | NextAuth Prisma Persistence Adapter; tRPC Next.js API Handler Adapter | 1; 2 |
| Strategy | Sign-in Provider Strategy; Wire Serialization Transformer | 1; 2 |
| Facade | TMDB Catalogue Facade | 1 |
| Composite | API Router Tree | 1 |
| Proxy | Pages-Router tRPC Client Proxy; App-Router tRPC Client Proxy; Environment Secret Guard | 1 |
| Read-Through Cache | My List Query Cache; Profile and Account Query Cache | 1; 2 |
| Front Controller | tRPC API Front Controller; NextAuth Auth Route Front Controller | 2 |
| Builder | tRPC Procedure Builder | 2 |
| Context Object | tRPC Request Context | 2 |
| Error Boundary | Shows Segment Error Boundary; Root Global Error Boundary | 2 |
| Suspense Boundary | Shows Loading Placeholder | 2 |
| Scatter-Gather | TMDB Row Scatter-Gather | 2 |

**Correction made in pass 2:** the *Pages-Router tRPC Client Proxy* listed its own
`loggerLink + httpBatchLink` (lib/api/api.ts:36-45) as transport. Reading @trpc/next@10.28.0
shows `config()` is only evaluated inside `withTRPC`, which the app never mounts; the hooks of
that proxy resolve the client from the shared `TRPCContext` (@trpc/react-query
createHooksInternal:92,193) supplied by `TRPCProvider` from lib/api/client.ts. The Transport role
now points to client.ts:35-44.

## Rejected (11)
| Candidate | Where | Reason |
|---|---|---|
| Caching Proxy for server components (createTRPCNextLayout) | src/@trpc/next-layout/server/createTrpcNextLayout.tsx:89-168 | Real proxy + QueryClient cache structure, but `grep -rn createTRPCNextLayout src` finds no importer: dead code at baseline, not part of any running collaboration. |
| Factory Method (createTRPCContext / createInnerTRPCContext) | server/api/trpc.ts:47-69 | No creator hierarchy or overridable creation step, so not GoF Factory Method. The same functions are confirmed as the ContextFactory of the *tRPC Request Context* (Context Object). |
| Repository | server/api/routers/*.ts | Routers call ctx.prisma.<model> directly; no repository abstraction exists. (Prisma itself is a data-mapper style ORM - dependency, not mapped.) |
| Template Method (nested layouts) | app/**/layout.tsx | Layouts compose children; no base algorithm with overridable steps. |
| Recommendation strategy / engine | app/(shows)/page.tsx:13-42, lib/fetchers.ts | Rows are fixed TMDB queries (trending, top rated, genre ids 28/35/27/10749/99). No user signal is used, so no recommendation pattern exists at baseline. |
| Debounce as a design pattern | components/debounced-input.tsx:44-50 | UI timing technique (setTimeout reset) - not a GoF/GRASP/architecture pattern. |
| Explicit Suspense boundaries | app/(dashboard)/account/users/[userId]/page.tsx:50-64; app/(dashboard)/help-center/page.tsx:23-73 | `<Suspense fallback>` wraps client components (EditUserForm, ...) that never suspend (no async data read, no lazy import), so the fallback can never be shown: the idiom is present syntactically but not as a working collaboration. |
| Container / Presentational split | components/shows-container.tsx; shows-carousel.tsx; shows-grid.tsx | ShowsContainer does fetch and pass data, but ShowsCarousel/ShowsGrid themselves read and write the modal store, so presentational components are not state-free; the split is not maintained. |
| Mediator via Zustand stores | stores/*.ts | Stores only hold state and setters; they contain no coordination logic between colleagues. Already recorded as Observer subjects. |
| Command (react-query mutations) | components/forms/*.tsx `useMutation` | The mutation object exposes mutate(), but there is no app-level command interface, queue, undo or logging - a framework hook call, not a Command collaboration. |
| Registry (Icons, siteConfig) | components/icons.tsx; config/site.ts | Static constant lookup objects; no registration/lookup protocol. |

## Uncertain (5)
| Candidate | Where | Why uncertain |
|---|---|---|
| Observer / publish-subscribe via Stripe webhook | app/api/webhooks/stripe/route.ts:8-76 | Only the subscriber side is in the code; the subscription (endpoint registration) lives in Stripe dashboard config, and dispatch is an if-chain on event.type. Cannot confirm both roles from source. |
| Protection Proxy for profile PIN gate | components/screens/profiles-screen.tsx:43-143; forms/pin-form.tsx:16-26 | ProfilesScreen wraps children and decides whether to render them, but there is no shared interface with the protected object - it is conditional rendering. Also note: the PIN is sent to the browser and compared client-side (pin-form.tsx:19), so it is not a real access control. |
| Implicit server data cache (Next.js fetch) | lib/fetchers.ts:15-41 | Next 13 app router caches `fetch` by default, but the code sets no cache/revalidate option; behaviour comes entirely from the framework and was not observed at runtime here (no TMDB access in the analysis environment). |
| Facade over session / subscription lookup | lib/session.ts:4-11; lib/subscription.ts:6-53 | Thin wrappers: getCurrentUser hides authOptions, getUserSubscriptionPlan joins DB fields with plan config and an expiry rule. Too small / single-subsystem to separate from ordinary helper functions. |
| Second client link chain (pages-router client) | lib/api/api.ts:36-45 | Same loggerLink -> httpBatchLink chain as client.ts, but `config()` of createTRPCNext is only called by withTRPC, which is never mounted (@trpc/next@10.28.0 dist/index.js:171-188). Declared but not executed - not counted as an instance. |

Observation scope: static reading of the baseline, dependency source of the pinned versions and
typecheck; no runtime session with real Stripe/TMDB/Google credentials was possible in the
analysis environment.
