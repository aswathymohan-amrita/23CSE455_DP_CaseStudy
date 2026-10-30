"""Single source of truth for the Part 1 pattern records of team A12.

Run from the A12 folder:  python3 data/test_result/part1/part1_patterns.py
Writes Part1/patterns.csv and Part1/Pattern_count.csv (baseline rows).
Every location below was checked by hand against code/ (baseline commit
676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258). Dependency locations point into
node_modules of that commit's yarn.lock (versions listed in README.md).
"""
import csv
import os

SV = "original@676e5dd"

# Each record: pattern, category, instance, roles[(role, symbol, location)],
# intent/evidence text, concrete participant count (variable-role implementations).
PATTERNS = [
    dict(
        pattern="Chain of Responsibility", ptype="Behavioral (GoF); tRPC middleware idiom",
        instance="Authenticated Procedure Pipeline", origin="application (create-t3-app scaffold) on framework",
        roles=[
            ("Handler", "tRPC MiddlewareFunction created by t.middleware", "dependency @trpc/server@10.28.0"),
            ("ConcreteHandler", "enforceUserIsAuthed", "data/code/src/server/api/trpc.ts:109-119"),
            ("Chain assembly", "protectedProcedure = t.procedure.use(enforceUserIsAuthed)", "data/code/src/server/api/trpc.ts:129"),
            ("Terminal handler", "procedure resolvers e.g. profileRouter.getAll", "data/code/src/server/api/routers/profile.ts:7-15"),
            ("Client", "createNextApiHandler (tRPC HTTP entry point)", "data/code/src/pages/api/trpc/[trpc].ts:8-19"),
        ],
        evidence="Problem: every private procedure must reject anonymous callers. enforceUserIsAuthed inspects ctx.session and either throws TRPCError UNAUTHORIZED (stops the chain) or calls next({ctx}) with a narrowed session, passing the request to the next link. protectedProcedure attaches the handler once; 18 of 19 procedures in user/profile/icon/myList routers are built on it, so the check runs before each resolver without being repeated.",
        concrete=1,
    ),
    dict(
        pattern="Singleton", ptype="Creational (GoF)",
        instance="Shared Prisma Database Client", origin="application (create-t3-app scaffold)",
        roles=[
            ("Singleton", "prisma (PrismaClient instance)", "data/code/src/server/db.ts:9-14"),
            ("Instance holder", "globalForPrisma (globalThis cache)", "data/code/src/server/db.ts:5-7,16"),
            ("Client", "createInnerTRPCContext", "data/code/src/server/api/trpc.ts:47-52"),
            ("Client", "authOptions.adapter = PrismaAdapter(prisma)", "data/code/src/server/auth.ts:48"),
            ("Client", "getUserSubscriptionPlan", "data/code/src/lib/subscription.ts:6-53"),
            ("Client", "Stripe webhook POST", "data/code/src/app/api/webhooks/stripe/route.ts:8-76"),
        ],
        evidence="Problem: Next.js hot reload re-evaluates modules, which would open a new connection pool each time. db.ts reuses globalForPrisma.prisma if present (??) and only constructs PrismaClient once, then stores it on globalThis outside production. All server code imports the same `prisma` export.",
        concrete=1,
    ),
    dict(
        pattern="Singleton", ptype="Creational (GoF); ES-module singleton idiom",
        instance="Stripe API Client", origin="application",
        roles=[
            ("Singleton", "stripe (Stripe instance)", "data/code/src/lib/stripe.ts:4-7"),
            ("Client", "Stripe webhook POST", "data/code/src/app/api/webhooks/stripe/route.ts:8-76"),
            ("Client", "checkout/portal POST", "data/code/src/app/api/users/stripe/route.ts:14-115"),
            ("Client", "PlansPage", "data/code/src/app/(auth)/login/plans/page.tsx:17-60"),
            ("Client", "AccountPage", "data/code/src/app/(dashboard)/account/page.tsx:16-61"),
        ],
        evidence="One configured Stripe client (API key, apiVersion 2022-11-15) is created at module load and exported; the ES module cache guarantees a single instance per server process. Four call sites share it instead of constructing their own. No global guard as in db.ts, so it relies on module caching only (noted as weaker form).",
        concrete=1,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Show Modal Selection", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi (subscribe/setState) created by create()", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useModalStore", "data/code/src/stores/modal.ts:13-20"),
            ("Publisher (calls setState)", "ShowCard onClick", "data/code/src/components/shows-carousel.tsx:93-113"),
            ("ConcreteObserver", "ShowsContainer", "data/code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "ShowModal", "data/code/src/components/show-modal.tsx:30-296"),
            ("ConcreteObserver", "Hero", "data/code/src/components/hero.tsx:17-102"),
            ("ConcreteObserver", "ShowsGrid", "data/code/src/components/shows-grid.tsx:13-48"),
        ],
        evidence="Selecting a poster calls useModalStore.setState({show, open, play}) (shows-carousel.tsx:105-109). Components that called useModalStore() are subscribed by the hook and re-render when state changes: ShowsContainer/ShowsGrid open ShowModal, ShowModal fetches the trailer for the new show (show-modal.tsx:45-74). Publisher and observers never reference each other.",
        concrete=4,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Active Profile Selection", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useProfileStore", "data/code/src/stores/profile.ts:12-27"),
            ("Publisher", "ProfilesScreen profile button / SiteHeader menu / siteConfig sign-out", "data/code/src/components/screens/profiles-screen.tsx:86-91; data/code/src/components/layouts/site-header.tsx:150-155; data/code/src/config/site.ts:57"),
            ("ConcreteObserver", "ProfilesScreen", "data/code/src/components/screens/profiles-screen.tsx:24-144"),
            ("ConcreteObserver", "PinForm", "data/code/src/components/forms/pin-form.tsx:10-104"),
            ("ConcreteObserver", "ShowsContainer", "data/code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "ShowModal", "data/code/src/components/show-modal.tsx:30-296"),
            ("ConcreteObserver", "SiteHeader", "data/code/src/components/layouts/site-header.tsx:35-261"),
            ("ConcreteObserver", "MyShows", "data/code/src/components/my-shows.tsx:16-54"),
        ],
        evidence="The selected profile and the PIN-gate flag live in one store. Setting {profile, pinForm} makes ProfilesScreen switch between profile picker, PinForm and the app shell (profiles-screen.tsx:43-143); ShowsContainer/ShowModal/MyShows re-query My List for the new profile id. Six components subscribe; three places publish.",
        concrete=6,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
        instance="Search Results Broadcast", origin="application on dependency (zustand@4.3.8)",
        roles=[
            ("Subject", "zustand StoreApi", "dependency zustand@4.3.8"),
            ("ConcreteSubject", "useSearchStore", "data/code/src/stores/search.ts:11-16"),
            ("Publisher", "SiteHeader.searchShowsByQuery", "data/code/src/components/layouts/site-header.tsx:51-55"),
            ("ConcreteObserver", "SiteHeader", "data/code/src/components/layouts/site-header.tsx:35-261"),
            ("ConcreteObserver", "ShowsContainer", "data/code/src/components/shows-container.tsx:22-65"),
            ("ConcreteObserver", "Hero", "data/code/src/components/hero.tsx:17-102"),
            ("ConcreteObserver", "MainNav", "data/code/src/components/layouts/main-nav.tsx:24-142"),
            ("ConcreteObserver", "MyShows", "data/code/src/components/my-shows.tsx:16-54"),
        ],
        evidence="SiteHeader writes query and results into useSearchStore; when query is non-empty ShowsContainer swaps carousels for ShowsGrid (shows-container.tsx:40-42) and Hero hides itself (hero.tsx:29-31); MainNav clears the query on navigation (main-nav.tsx:36-37). The search box does not know which views react.",
        concrete=5,
    ),
    dict(
        pattern="Decorator", ptype="Structural (GoF); Zustand middleware",
        instance="Persisted Profile Store", origin="application on dependency (zustand/middleware)",
        roles=[
            ("Component", "StateCreator<ProfileState>", "dependency zustand@4.3.8 (vanilla.d.ts)"),
            ("ConcreteComponent", "inline creator (set) => ({profile, setProfile, pinForm, setPinForm})", "data/code/src/stores/profile.ts:15-20"),
            ("ConcreteDecorator", "persist(..., {name, storage: sessionStorage})", "data/code/src/stores/profile.ts:14-25"),
            ("ConcreteDecorator", "devtools(...)", "data/code/src/stores/profile.ts:13-26"),
            ("Client", "create<ProfileState>()", "data/code/src/stores/profile.ts:12"),
        ],
        evidence="persist and devtools each take a StateCreator and return a StateCreator with the same shape, wrapping set/get to add sessionStorage persistence and Redux-devtools reporting. They are stacked devtools(persist(creator)); the modal and search stores use the undecorated creator, showing the behaviour is added per object without changing the creator.",
        concrete=3,
    ),
    dict(
        pattern="Adapter", ptype="Structural (GoF)",
        instance="NextAuth Prisma Persistence Adapter", origin="dependency (@next-auth/prisma-adapter@1.0.6) configured by application",
        roles=[
            ("Target", "Adapter (next-auth adapter interface)", "dependency next-auth@4.22.1 adapters.d.ts:57"),
            ("Adapter", "PrismaAdapter(p)", "dependency @next-auth/prisma-adapter@1.0.6 dist/index.js:206-264"),
            ("Adaptee", "prisma (PrismaClient)", "data/code/src/server/db.ts:9-14"),
            ("Client", "authOptions.adapter used by NextAuth handler", "data/code/src/server/auth.ts:38-64; data/code/src/pages/api/auth/[...nextauth].ts:4"),
        ],
        evidence="NextAuth persists users, accounts and sessions only through its Adapter interface (createUser, getUserByEmail, linkAccount, ...). PrismaAdapter returns an object implementing those methods by translating them to Prisma calls, e.g. createUser: (data) => p.user.create({data}) and getUserByEmail: (email) => p.user.findUnique({where:{email}}) (index.js:208-210). The app wires it with adapter: PrismaAdapter(prisma).",
        concrete=1,
    ),
    dict(
        pattern="Strategy", ptype="Behavioral (GoF)",
        instance="Sign-in Provider Strategy", origin="framework (next-auth@4.22.1) configured by application",
        roles=[
            ("Strategy", "Provider = OAuthConfig | EmailConfig | CredentialsConfig", "dependency next-auth@4.22.1 providers/index.d.ts:14"),
            ("ConcreteStrategy", "GoogleProvider({clientId, clientSecret})", "data/code/src/server/auth.ts:50-53"),
            ("Context", "NextAuth(authOptions) with providers[]", "data/code/src/server/auth.ts:38-64; data/code/src/pages/api/auth/[...nextauth].ts:4"),
        ],
        evidence="authOptions.providers is a list of interchangeable provider objects behind one Provider type; NextAuth selects the provider by id at sign-in and delegates the authorization/profile mapping to it. Only Google is configured; the commented block at auth.ts:54-62 documents adding more without changing NextAuth. Single concrete strategy, so variability is latent.",
        concrete=1,
    ),
    dict(
        pattern="Facade", ptype="Structural (GoF)",
        instance="TMDB Catalogue Facade", origin="application",
        roles=[
            ("Facade", "module lib/fetchers: getShows, getNewAndPopularShows, searchShows", "data/code/src/lib/fetchers.ts:5-77,82-122,124-142"),
            ("Subsystem", "TMDB REST endpoints (trending, top_rated, discover, popular, search/multi) + API key", "data/code/src/lib/fetchers.ts:15-41; data/code/src/env.mjs"),
            ("Client", "Home, MoviesPage, TVShowsPage", "data/code/src/app/(shows)/page.tsx:8-52; data/code/src/app/(shows)/movies/page.tsx:13-54; data/code/src/app/(shows)/tv-shows/page.tsx:12-51"),
            ("Client", "NewAndPopularPage", "data/code/src/app/(shows)/new-and-popular/page.tsx:12-39"),
            ("Client", "SiteHeader.searchShowsByQuery", "data/code/src/components/layouts/site-header.tsx:51-55"),
        ],
        evidence="Pages need categorised show lists, not URLs. getShows(mediaType) issues eight TMDB requests in parallel, checks all responses, parses JSON and returns one object of named rows; callers only call getShows('movie'). URL construction, API key, network errors and JSON shape are hidden behind three functions (module-level facade, no class).",
        concrete=1,
    ),
    dict(
        pattern="Composite", ptype="Structural (GoF); tRPC router tree",
        instance="API Router Tree", origin="application on framework (@trpc/server)",
        roles=[
            ("Component", "AnyRouter | AnyProcedure in ProcedureRouterRecord", "dependency @trpc/server@10.28.0"),
            ("Composite (root)", "appRouter", "data/code/src/server/api/root.ts:12-17"),
            ("Composite", "userRouter", "data/code/src/server/api/routers/user.ts:9-91"),
            ("Composite", "profileRouter", "data/code/src/server/api/routers/profile.ts:6-186"),
            ("Composite", "iconRouter", "data/code/src/server/api/routers/icon.ts:5-59"),
            ("Composite", "myListRouter", "data/code/src/server/api/routers/my-list.ts:6-184"),
            ("Leaf", "19 procedures e.g. profile.getAll", "data/code/src/server/api/routers/profile.ts:7-15"),
            ("Factory", "createTRPCRouter = t.router", "data/code/src/server/api/trpc.ts:97"),
        ],
        evidence="createTRPCRouter accepts a record whose values are procedures (leaves) or routers (composites); appRouter nests four routers that hold 19 procedures. Clients address any node uniformly by dotted path (api.profile.getAll), and the type AppRouter is the whole tree. The recursive DecoratedProcedureRecord type (src/@trpc/next-layout/server/createTrpcNextLayout.tsx:53-65) walks routers and procedures the same way.",
        concrete=5,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); remote proxy",
        instance="Pages-Router tRPC Client Proxy", origin="application on dependency (@trpc/next@10.28.0)",
        roles=[
            ("Subject", "AppRouter type", "data/code/src/server/api/root.ts:20"),
            ("RealSubject", "appRouter served by createNextApiHandler", "data/code/src/pages/api/trpc/[trpc].ts:8-19"),
            ("Proxy", "api = createTRPCNext<AppRouter>(...)", "data/code/src/lib/api/api.ts:21-54"),
            ("Transport", "client from the shared TRPCContext supplied by TRPCProvider (its own links in api.ts:36-45 are never executed)", "data/code/src/lib/api/client.ts:35-44; dependency @trpc/react-query@10.28.0 dist/createHooksInternal-9f8a4b21.js:92,193"),
            ("Client", "ShowsContainer, ShowModal, ProfilesScreen, SiteHeader and 7 more components", "data/code/src/components/shows-container.tsx:32-36; data/code/src/components/show-modal.tsx:93-124"),
        ],
        evidence="Components call api.myList.getAll.useQuery(...) as if the server router were local. api is a JavaScript Proxy (createRecursiveProxy/createFlatProxy, @trpc/server dist index-4a823936.js:55,87) that turns each property path into an HTTP batch request to /api/trpc and returns typed results. Same typed interface as the real router (AppRouter).",
        concrete=1,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); remote proxy",
        instance="App-Router tRPC Client Proxy", origin="application (vendored src/@trpc/next-layout) on dependency",
        roles=[
            ("Subject", "AppRouter type", "data/code/src/server/api/root.ts:20"),
            ("RealSubject", "appRouter served by createNextApiHandler", "data/code/src/pages/api/trpc/[trpc].ts:8-19"),
            ("Proxy", "api = createTRPCNextBeta<AppRouter>(...)", "data/code/src/lib/api/client.ts:22-45"),
            ("Proxy factory", "createTRPCNextBeta -> createFlatProxy", "data/code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:48-93"),
            ("Provider", "TRPCProvider wraps RootLayout", "data/code/src/context/trpc-provider.tsx:7-9; data/code/src/app/layout.tsx:80-96"),
            ("Client", "AddProfileForm, EditProfileForm", "data/code/src/components/forms/add-profile-form.tsx:13; data/code/src/components/forms/edit-profile-form.tsx:15"),
        ],
        evidence="A second client proxy built with the vendored createTRPCNextBeta returns createFlatProxy((key) => ...) (createTrpcNextBeta.tsx:76-92): 'Provider' and 'useContext' are served locally, every other key is decorated into React-Query hooks that call the server. It also supplies the QueryClient used by the app. Two independent proxies for one Subject is recorded as a smell (duplicated getBaseUrl/links).",
        concrete=1,
    ),
    dict(
        pattern="Proxy", ptype="Structural (GoF); protection proxy",
        instance="Environment Secret Guard", origin="application (create-t3-app scaffold)",
        roles=[
            ("Subject", "MergedOutput (validated env shape)", "data/code/src/env.mjs:67-71"),
            ("RealSubject", "parsed.data (zod-validated variables)", "data/code/src/env.mjs:75-90"),
            ("Proxy", "env = new Proxy(parsed.data, {get})", "data/code/src/env.mjs:92-105"),
            ("Client", "10 modules importing env, e.g. lib/stripe.ts, lib/fetchers.ts, server/db.ts", "data/code/src/lib/stripe.ts:1-7; data/code/src/server/db.ts:3"),
        ],
        evidence="Server secrets (STRIPE_API_KEY, DATABASE_URL, ...) must never be read in browser bundles. Every module imports `env`, which is a Proxy whose get trap checks the caller side: on the client any non NEXT_PUBLIC_ key throws a descriptive error, otherwise the value is forwarded from the validated object (env.mjs:93-103). Same interface as the real object, access control added transparently.",
        concrete=1,
    ),
    dict(
        pattern="Read-Through Cache", ptype="Architecture (caching); React Query",
        instance="My List Query Cache", origin="application configuration on dependency (@tanstack/react-query@4.29.7)",
        roles=[
            ("Cache", "QueryClient created once per TRPCProvider", "data/code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:55-63"),
            ("Cache policy", "cacheTime: Infinity, staleTime: Infinity, refetchOnWindowFocus: false", "data/code/src/lib/api/client.ts:24-34"),
            ("Loader (data source)", "myListRouter.getAll", "data/code/src/server/api/routers/my-list.ts:7-12"),
            ("Reader", "ShowsContainer myShowsQuery", "data/code/src/components/shows-container.tsx:32-36"),
            ("Reader", "ShowModal myShowsQuery", "data/code/src/components/show-modal.tsx:98-102"),
            ("Invalidator", "ShowModal effect apiUtils.myList.getAll.invalidate()", "data/code/src/components/show-modal.tsx:127-130"),
        ],
        evidence="useQuery(key) returns cached data for the key (profile id) and only calls the loader on a miss or after invalidation; with staleTime Infinity, repeated renders of ShowsContainer and ShowModal share one fetch. After each add/remove mutation ShowModal invalidates the key so the next read reloads. Caller never talks to the data source directly.",
        concrete=1,
    ),
    # ---- added 2026-10-29: second, exhaustive pass over every in-scope file (see candidates.md) ----
    dict(
        pattern="Front Controller", ptype="Architectural (Fowler PoEAA); Next.js API route",
        instance="tRPC API Front Controller", origin="application (create-t3-app scaffold) on framework (@trpc/server@10.28.0)",
        roles=[
            ("FrontController", "default export createNextApiHandler({router, createContext, onError}) at route /api/trpc/[trpc]", "data/code/src/pages/api/trpc/[trpc].ts:8-19"),
            ("Shared pre-processing", "createTRPCContext (session lookup for every call)", "data/code/src/server/api/trpc.ts:60-69"),
            ("Shared error handling", "onError logger (development only)", "data/code/src/pages/api/trpc/[trpc].ts:11-18"),
            ("Dispatcher", "nodeHTTPRequestHandler -> resolveHTTPResponse -> callProcedure(path)", "dependency @trpc/server@10.28.0 dist/nodeHTTPRequestHandler-5bbf93f1.js:7-34; dist/resolveHTTPResponse-9523b4e3.js:90"),
            ("Command registry", "appRouter (procedure paths user.*, profile.*, icon.*, myList.*)", "data/code/src/server/api/root.ts:12-17"),
            ("ConcreteCommand", "19 procedures e.g. profile.getAll", "data/code/src/server/api/routers/profile.ts:7-15"),
            ("Client", "httpBatchLink url /api/trpc", "data/code/src/lib/api/client.ts:41-43"),
        ],
        evidence="Problem: 19 server operations would otherwise need 19 API route files, each repeating session lookup, body parsing and error formatting. The single Next.js dynamic route /api/trpc/[trpc] receives every call; createNextApiHandler reads the procedure path from req.query.trpc (adapters/next.js:17-25), builds the context once with createTRPCContext, and nodeHTTPRequestHandler/resolveHTTPResponse dispatch to the procedure registered under that path in appRouter (callProcedure, resolveHTTPResponse.js:90). Unknown paths produce a NOT_FOUND error shape from the same place, so dispatch, pre-processing and error policy are centralised.",
        concrete=1,
    ),
    dict(
        pattern="Front Controller", ptype="Architectural (Fowler PoEAA); NextAuth catch-all route",
        instance="NextAuth Auth Route Front Controller", origin="application on dependency (next-auth@4.22.1)",
        roles=[
            ("FrontController", "NextAuth(authOptions) exported at catch-all route /api/auth/[...nextauth]", "data/code/src/pages/api/auth/[...nextauth].ts:4"),
            ("Request parsing", "NextAuthApiHandler maps req.query.nextauth -> {action, providerId}", "dependency next-auth@4.22.1 next/index.js:18-31"),
            ("Dispatcher", "AuthHandler switch (action): providers, session, csrf, signin, signout, callback", "dependency next-auth@4.22.1 core/index.js:68; core/index.js:159-206,257-340"),
            ("Configuration", "authOptions (adapter, providers, callbacks)", "data/code/src/server/auth.ts:38-64"),
            ("Client", "LoginButton.loginWithGoogle -> signIn('google')", "data/code/src/components/login-button.tsx:13-24"),
            ("Client", "SiteHeader sign-out -> signOut()", "data/code/src/components/layouts/site-header.tsx:230"),
        ],
        evidence="Every authentication request (GET /api/auth/providers, /session, /csrf, POST /signin/google, GET /callback/google, POST /signout) reaches the one handler exported by [...nextauth].ts. next-auth splits the catch-all segment into action and providerId and AuthHandler dispatches with switch(action) to the matching route module, applying the shared authOptions (adapter, providers, session callback). The app router copy app/api/auth/[...nextauth]/_route.ts is disabled by its leading underscore, so this is the only active controller.",
        concrete=1,
    ),
    dict(
        pattern="Adapter", ptype="Structural (GoF); tRPC framework adapter",
        instance="tRPC Next.js API Handler Adapter", origin="application wiring on dependency (@trpc/server@10.28.0 adapters/next)",
        roles=[
            ("Target", "Next.js pages-router API handler signature (req: NextApiRequest, res: NextApiResponse)", "dependency next@13.4.4 (NextApiHandler type)"),
            ("Adapter", "createNextApiHandler(opts) returns async (req, res) => ...", "dependency @trpc/server@10.28.0 dist/adapters/next.js:16-56"),
            ("Adaptee", "tRPC request resolution nodeHTTPRequestHandler/resolveHTTPResponse over appRouter", "dependency @trpc/server@10.28.0 dist/nodeHTTPRequestHandler-5bbf93f1.js:7-34"),
            ("Adapted context type", "CreateNextContextOptions used by createTRPCContext", "data/code/src/server/api/trpc.ts:28; data/code/src/server/api/trpc.ts:60-69"),
            ("Client", "Next.js route file default export", "data/code/src/pages/api/trpc/[trpc].ts:8-19"),
        ],
        evidence="tRPC's router knows nothing about Next.js; Next.js only calls functions of the form (req, res). createNextApiHandler converts between them: it extracts the path from Next's req.query.trpc (string or array), passes req/res into the framework-neutral nodeHTTPRequestHandler and writes the result back with res.json. The application only supplies appRouter and createTRPCContext typed with CreateNextContextOptions. Shares the route file with the tRPC API Front Controller but is a separate collaboration (interface conversion vs. central dispatch).",
        concrete=1,
    ),
    dict(
        pattern="Chain of Responsibility", ptype="Behavioral (GoF); tRPC client links",
        instance="tRPC Client Link Chain", origin="application configuration on dependency (@trpc/client@10.28.0)",
        roles=[
            ("Handler", "TRPCLink (op, next) => Observable", "dependency @trpc/client@10.28.0"),
            ("Chain runner", "createChain execute(index) -> links[index]({op, next: execute(index + 1)})", "dependency @trpc/client@10.28.0 dist/splitLink-aebd28df.js:4-23"),
            ("ConcreteHandler", "loggerLink({enabled}) - logs then forwards next(op)", "data/code/src/lib/api/client.ts:36-40; dependency @trpc/client@10.28.0 dist/links/loggerLink.js:71-112"),
            ("ConcreteHandler (terminal)", "httpBatchLink({url: /api/trpc}) - sends the batched HTTP request, never calls next", "data/code/src/lib/api/client.ts:41-43; dependency @trpc/client@10.28.0 dist/links/httpBatchLink.js:130-224"),
            ("Chain assembly", "links: [loggerLink, httpBatchLink] in createTRPCNextBeta options", "data/code/src/lib/api/client.ts:35-44"),
            ("Client", "trpc.createClient(opts) inside TRPCProvider", "data/code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:55-63"),
        ],
        evidence="Each client operation is passed along an ordered list of links. The chain runner calls links[0] with a next() that runs links[1]; loggerLink decides per operation whether to log (development or error results) and always forwards next(op); httpBatchLink is the terminal handler that performs the request. Adding/removing a link (e.g. a retry link) changes behaviour without touching callers. The identical links array in lib/api/api.ts:36-45 is never executed: createTRPCNext only reads config() inside withTRPC (dependency @trpc/next@10.28.0 dist/index.js:171-188), which the app never mounts, and its hooks use the shared TRPCContext supplied by TRPCProvider (dependency @trpc/react-query@10.28.0 createHooksInternal-9f8a4b21.js:92,193). That copy is therefore recorded as an uncertain/inactive observation, not a second instance.",
        concrete=2,
    ),
    dict(
        pattern="Builder", ptype="Creational (GoF); fluent immutable builder (tRPC)",
        instance="tRPC Procedure Builder", origin="application on dependency (@trpc/server@10.28.0)",
        roles=[
            ("Builder", "ProcedureBuilder returned by createBuilder (input, output, meta, use; build steps query/mutation/subscription)", "dependency @trpc/server@10.28.0 dist/index.js:326-438"),
            ("Builder factory", "t = initTRPC.context<typeof createTRPCContext>().create({transformer, errorFormatter})", "data/code/src/server/api/trpc.ts:71-83"),
            ("ConcreteBuilder (base)", "publicProcedure = t.procedure", "data/code/src/server/api/trpc.ts:106"),
            ("ConcreteBuilder (pre-configured)", "protectedProcedure = t.procedure.use(enforceUserIsAuthed)", "data/code/src/server/api/trpc.ts:129"),
            ("Director / Client", "router definitions, e.g. profile.getOthers = protectedProcedure.input(z.string()).query(resolver)", "data/code/src/server/api/routers/profile.ts:17-28"),
            ("Product", "Procedure (createProcedureCaller(_def)) with merged inputs, middlewares and resolver", "dependency @trpc/server@10.28.0 dist/index.js:412-438"),
        ],
        evidence="A procedure has many optional parts (input validators, output parser, meta, middleware stack, resolver kind). Instead of a large constructor, each builder call returns a NEW builder whose _def merges the previous definition (createNewBuilder concatenates inputs and middlewares, index.js:326-344), so shared partial builders such as protectedProcedure can be reused safely by all 18 private procedures. query()/mutation() are the final build steps that freeze the definition into a callable Procedure (createResolver -> createProcedureCaller).",
        concrete=2,
    ),
    dict(
        pattern="Context Object", ptype="Architectural (Core J2EE); tRPC request context / dependency injection",
        instance="tRPC Request Context", origin="application (create-t3-app scaffold)",
        roles=[
            ("ContextFactory", "createTRPCContext(opts: {req, res}) - resolves session per request", "data/code/src/server/api/trpc.ts:60-69"),
            ("Context builder (protocol independent)", "createInnerTRPCContext({session}) -> {session, prisma}", "data/code/src/server/api/trpc.ts:47-52"),
            ("ContextObject type", "CreateContextOptions / inferred ctx type bound by initTRPC.context<typeof createTRPCContext>()", "data/code/src/server/api/trpc.ts:33-35; data/code/src/server/api/trpc.ts:71"),
            ("Context refiner", "enforceUserIsAuthed next({ctx: {session: non-null}})", "data/code/src/server/api/trpc.ts:109-119"),
            ("Consumer", "resolvers reading ctx.prisma and ctx.session.user.id, e.g. profile.getAll", "data/code/src/server/api/routers/profile.ts:7-15"),
        ],
        evidence="Resolvers must not depend on Next.js req/res. createTRPCContext extracts the protocol-specific data once (getServerAuthSession(req,res)) and hands a protocol-independent object {session, prisma} to every middleware and resolver via the ctx argument; createInnerTRPCContext exists so tests can build the same object without HTTP (comment trpc.ts:37-46). Middleware can return a refined context (enforceUserIsAuthed narrows session to non-null). Resolvers get their collaborators (database client, caller identity) only from ctx.",
        concrete=1,
    ),
    dict(
        pattern="Strategy", ptype="Behavioral (GoF); tRPC data transformer",
        instance="Wire Serialization Transformer", origin="application configuration on dependency (@trpc/server@10.28.0, superjson@1.12.3)",
        roles=[
            ("Strategy", "DataTransformer {serialize, deserialize} (normalised by getDataTransformer to input/output pair)", "dependency @trpc/server@10.28.0 dist/config-f3ce0144.js:11-21"),
            ("ConcreteStrategy (default)", "defaultTransformer (identity) used when none is configured", "dependency @trpc/server@10.28.0 dist/config-f3ce0144.js:22-30"),
            ("ConcreteStrategy (selected)", "superjson", "dependency superjson@1.12.3; data/code/src/server/api/trpc.ts:30"),
            ("Context (server)", "initTRPC...create({transformer: superjson})", "data/code/src/server/api/trpc.ts:71-72"),
            ("Context (client)", "createTRPCNextBeta({transformer: superjson})", "data/code/src/lib/api/client.ts:22-23"),
            ("Context (hydration)", "createHydrateClient({transformer: superjson})", "data/code/src/lib/api/client.ts:51-53"),
        ],
        evidence="How Date, Map or undefined values cross the HTTP boundary is an interchangeable algorithm. tRPC calls only transformer.serialize/deserialize; with no option it uses the identity defaultTransformer (JSON loses Date), the app selects superjson on both sides so a Date such as user.stripeCurrentPeriodEnd arrives as a Date. Swapping the strategy changes the wire format without touching any procedure. Server and client must choose the same strategy - a configuration constraint the pattern makes explicit.",
        concrete=1,
    ),
    dict(
        pattern="Observer", ptype="Behavioral (GoF); DOM EventTarget listeners",
        instance="Search Input DOM Event Listeners", origin="application on browser platform (EventTarget)",
        roles=[
            ("Subject", "EventTarget addEventListener/removeEventListener (browser)", "browser DOM API"),
            ("ConcreteSubject", "document (mousedown, touchstart) and window (keydown)", "data/code/src/hooks/use-on-click-outside.ts:15-16; data/code/src/components/debounced-input.tsx:69"),
            ("ConcreteObserver", "useOnClickOutside listener (ignores clicks inside ref, else calls handler)", "data/code/src/hooks/use-on-click-outside.ts:8-14"),
            ("ConcreteObserver", "DebouncedInput handleKeyDown (Escape closes, Ctrl/Cmd+K opens)", "data/code/src/components/debounced-input.tsx:53-71"),
            ("Subscription lifecycle", "useEffect registers and its cleanup unregisters the listeners", "data/code/src/hooks/use-on-click-outside.ts:7-22; data/code/src/components/debounced-input.tsx:69-70"),
            ("Client", "DebouncedInput uses useOnClickOutside(inputRef, closeInput); rendered by SiteHeader", "data/code/src/components/debounced-input.tsx:36-37; data/code/src/components/layouts/site-header.tsx:80"),
        ],
        evidence="The search box must react to events that happen anywhere on the page. Instead of the page calling the input, the component subscribes listener objects to document/window; the browser notifies every registered listener on each event and the component unsubscribes on unmount (cleanup functions), so subject and observers stay decoupled and no listener leaks. Distinct from the Zustand observers: the subject is the browser EventTarget and the notification carries a DOM Event.",
        concrete=2,
    ),
    dict(
        pattern="Error Boundary", ptype="Framework idiom (React/Next.js App Router)",
        instance="Shows Segment Error Boundary", origin="application on framework (next@13.4.4 error.tsx convention)",
        roles=[
            ("Boundary", "ErrorBoundaryHandler (getDerivedStateFromError, reset) generated by Next for the (shows) segment", "dependency next@13.4.4 dist/client/components/error-boundary.js:53-110"),
            ("Fallback", "Error page component (shows)/error.tsx", "data/code/src/app/(shows)/error.tsx:10-12"),
            ("Fallback view", "ErrorScreen (message + Retry button calling reset())", "data/code/src/components/screens/error-screen.tsx:9-31"),
            ("Protected subtree", "ShowsLayout children: Home, Movies, TV Shows, New and Popular, My List pages", "data/code/src/app/(shows)/layout.tsx:8-18"),
            ("Error source", "getShows throws 'Failed to fetch shows' when a TMDB response is not ok", "data/code/src/lib/fetchers.ts:42-53"),
        ],
        evidence="A failed TMDB call in a page must not blank the whole app. Next.js wraps the (shows) segment in an ErrorBoundary class component whose getDerivedStateFromError switches to the segment's error.tsx; the fallback renders ErrorScreen with the message and a Retry button bound to reset(), which clears the boundary state and re-renders the subtree. Header/layout outside the segment stay mounted.",
        concrete=1,
    ),
    dict(
        pattern="Error Boundary", ptype="Framework idiom (React/Next.js App Router)",
        instance="Root Global Error Boundary", origin="application on framework (next@13.4.4 global-error.tsx convention)",
        roles=[
            ("Boundary", "ErrorBoundaryHandler wrapping the root layout", "dependency next@13.4.4 dist/client/components/error-boundary.js:53-110"),
            ("Fallback", "GlobalError (renders its own <html><body>)", "data/code/src/app/global-error.tsx:10-18"),
            ("Fallback view", "ErrorScreen", "data/code/src/components/screens/error-screen.tsx:9-31"),
            ("Protected subtree", "RootLayout (TRPCProvider, html, body, Toast, Analytics)", "data/code/src/app/layout.tsx:78-98"),
        ],
        evidence="Errors thrown by the root layout itself cannot be caught by segment boundaries. global-error.tsx replaces the whole document (it must render html/body because the root layout is gone) and reuses ErrorScreen with reset(). Independent of the shows boundary: different position in the tree, different fallback, catches different failures.",
        concrete=1,
    ),
    dict(
        pattern="Suspense Boundary", ptype="Framework idiom (React Suspense / Next.js loading.tsx)",
        instance="Shows Loading Placeholder", origin="application on framework (next@13.4.4 loading.tsx convention)",
        roles=[
            ("Boundary", "LoadingBoundary renders React.Suspense with the segment's loading component as fallback", "dependency next@13.4.4 dist/client/components/layout-router.js:335-345"),
            ("Fallback (placeholder)", "ShowsLoading skeleton", "data/code/src/app/(shows)/loading.tsx:3-9"),
            ("Suspending child", "async server pages awaiting TMDB, e.g. Home awaits getShows('movie')", "data/code/src/app/(shows)/page.tsx:8-52"),
        ],
        evidence="Async server pages suspend while getShows waits for eight TMDB requests. Because (shows)/loading.tsx exists, Next wraps the segment in <Suspense fallback={<ShowsLoading/>}> so a skeleton is streamed immediately and replaced when the page resolves. The two explicit <Suspense> wrappers in account/users/[userId]/page.tsx and help-center/page.tsx are NOT counted: their children are client components that never suspend, so the fallback can never show (rejected candidate).",
        concrete=1,
    ),
    dict(
        pattern="Scatter-Gather", ptype="Concurrency / Enterprise Integration (Hohpe & Woolf)",
        instance="TMDB Row Scatter-Gather", origin="application",
        roles=[
            ("Scatter", "Promise.all over 8 fetch calls (trending, top rated, Netflix originals, 5 genres)", "data/code/src/lib/fetchers.ts:6-40"),
            ("Gather / Aggregator", "fail if any !res.ok, then Promise.all(res.json()) and build one categorized object", "data/code/src/lib/fetchers.ts:42-76"),
            ("Scatter", "Promise.all over 4 fetch calls (popular/trending tv and movie)", "data/code/src/lib/fetchers.ts:83-97"),
            ("Gather / Aggregator", "fail if any !res.ok, then merge into {popularTvs, popularMovies, trendingTvs, trendingMovies}", "data/code/src/lib/fetchers.ts:99-121"),
            ("Recipients", "TMDB REST endpoints", "external api.themoviedb.org/3"),
            ("Client", "Home / MoviesPage / TVShowsPage / NewAndPopularPage", "data/code/src/app/(shows)/page.tsx:8-52; data/code/src/app/(shows)/new-and-popular/page.tsx:12-39"),
        ],
        evidence="A home page needs eight independent lists. getShows broadcasts all requests at once (Promise.all), waits for every reply, applies one all-or-nothing completeness rule (any non-ok response throws) and aggregates the replies into a single result keyed by row; getNewAndPopularShows does the same for four lists. Latency becomes the slowest call instead of the sum. Separate from the TMDB Catalogue Facade, which is about hiding endpoint details; this collaboration is about concurrent fan-out and aggregation.",
        concrete=2,
    ),
    dict(
        pattern="Read-Through Cache", ptype="Architecture (caching); React Query",
        instance="Profile and Account Query Cache", origin="application configuration on dependency (@tanstack/react-query@4.29.7)",
        roles=[
            ("Cache", "QueryClient created once per TRPCProvider (shared with My List Query Cache)", "data/code/src/@trpc/next-layout/client/createTrpcNextBeta.tsx:55-63"),
            ("Loader (data source)", "profileRouter.getAll / getOthers / getOne; userRouter.getCurrent / getCurrentWithProfile", "data/code/src/server/api/routers/profile.ts:7-38"),
            ("Reader", "ProfilesScreen profilesQuery", "data/code/src/components/screens/profiles-screen.tsx:29-31"),
            ("Reader", "ManageProfiles profilesQuery", "data/code/src/components/manage-profiles.tsx:20"),
            ("Reader", "SiteHeader otherProfilesQuery", "data/code/src/components/layouts/site-header.tsx:62-66"),
            ("Reader", "AccountForm userQuery / IconPicker userQuery", "data/code/src/components/forms/account-form.tsx:81; data/code/src/components/icon-picker.tsx:31"),
            ("Invalidator", "AddProfileForm onSuccess", "data/code/src/components/forms/add-profile-form.tsx:41-51"),
            ("Invalidator", "EditProfileForm effect on useIsMutating()", "data/code/src/components/forms/edit-profile-form.tsx:88-91"),
            ("Invalidator", "ResetPinForm onSuccess", "data/code/src/components/forms/reset-pin-form.tsx:44-63"),
            ("Invalidator", "AccountForm onSuccess", "data/code/src/components/forms/account-form.tsx:245-255"),
            ("Invalidator", "EditUserForm onSuccess", "data/code/src/components/forms/edit-user-form.tsx:40-48"),
        ],
        evidence="Profiles and the current user are read by many screens; with staleTime Infinity each key (profile.getAll, profile.getOthers[id], profile.getOne[id], user.getCurrent) is fetched once and then served from the QueryClient. Every mutation that changes those records explicitly invalidates the affected keys (apiUtils.profile.getAll.invalidate() etc.), so the next read goes through to the loader. Independent of the My List Query Cache: different keys, loaders, readers and invalidation points; only the cache store is shared.",
        concrete=1,
    ),
]


def roles_text(rec):
    return "; ".join(f"{r}={s}" for r, s, _ in rec["roles"])


def locs_text(rec):
    return "; ".join(f"{s}: {loc}" for _, s, loc in rec["roles"])


def main():
    with open("Part1/patterns.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["source_version", "pattern_name", "pattern_type", "instance_name",
                    "participant_roles", "source_locations", "intent_and_evidence"])
        for rec in PATTERNS:
            w.writerow([SV, rec["pattern"], rec["ptype"], rec["instance"],
                        roles_text(rec), locs_text(rec), rec["evidence"]])
    counts = {}
    for rec in PATTERNS:
        counts[rec["pattern"]] = counts.get(rec["pattern"], 0) + 1
    with open("Part1/Pattern_count.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source_version", "summary", "pattern_name", "count"])
        for name, n in counts.items():
            w.writerow([SV, "per_pattern", name, n])
        w.writerow([SV, "total_pattern_types", "", len(counts)])
        w.writerow([SV, "total_pattern_instances", "", len(PATTERNS)])
    print("types", len(counts), "instances", len(PATTERNS),
          "concrete", sum(r["concrete"] for r in PATTERNS),
          "unique in-repo symbols", len(IN_REPO_SYMBOLS), "dependency symbols", len(DEP_SYMBOLS))


# Distinct mapped symbols; a symbol shared by several instances (e.g. ShowsContainer,
# prisma, AppRouter) is listed once.
IN_REPO_SYMBOLS = """enforceUserIsAuthed protectedProcedure profile.getAll trpcApiHandler prisma
globalForPrisma createInnerTRPCContext authOptions getUserSubscriptionPlan webhookPOST stripe
checkoutPOST PlansPage AccountPage useModalStore ShowCard ShowsContainer ShowModal Hero ShowsGrid
useProfileStore ProfilesScreen SiteHeader siteConfig PinForm MyShows useSearchStore MainNav
profileStateCreator getShows getNewAndPopularShows searchShows Home MoviesPage TVShowsPage
NewAndPopularPage appRouter userRouter profileRouter iconRouter myListRouter myList.getAll
createTRPCRouter AppRouter api(lib/api/api.ts) api(lib/api/client.ts) createTRPCNextBeta
TRPCProvider RootLayout AddProfileForm EditProfileForm nextAuthHandler
env parsedEnvData MergedOutput
createTRPCContext createInnerTRPCContextType onErrorLogger LoginButton.loginWithGoogle signOutHandler
t(initTRPC) publicProcedure profile.getOthers loggerLink httpBatchLink linksArray HydrateClient superjsonConfig
useOnClickOutside.listener DebouncedInput.handleKeyDown DebouncedInput ShowsError GlobalError ErrorScreen
ShowsLayout ShowsLoading user.getCurrent profile.getOne ManageProfiles IconPicker AccountForm EditUserForm
ResetPinForm fetchers.getShows.scatter fetchers.getNewAndPopularShows.scatter""".split()
DEP_SYMBOLS = """MiddlewareFunction StoreApi StateCreator persist devtools Adapter PrismaAdapter
Provider GoogleProvider AnyRouter createRecursiveProxy/createFlatProxy QueryClient
nodeHTTPRequestHandler resolveHTTPResponse createNextApiHandler NextAuthApiHandler AuthHandler NextApiHandler
TRPCLink createChain createBuilder/ProcedureBuilder createProcedureCaller DataTransformer defaultTransformer
superjson EventTarget ErrorBoundaryHandler LoadingBoundary TRPCContext""".split()


if __name__ == "__main__":
    main()
