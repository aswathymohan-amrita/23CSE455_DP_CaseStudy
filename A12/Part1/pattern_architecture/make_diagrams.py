"""Writes editable PlantUML sources (*.puml) for Part 1 and renders PNGs.
Run from A12/:  python Part1/pattern_architecture/make_diagrams.py [name ...]
Needs java and plantuml.jar (path in PLANTUML_JAR, default ~/tools/plantuml.jar) + graphviz dot (falls back to PlantUML's smetana layout)."""
import os
import shutil
import subprocess
import sys

OUT = "Part1/pattern_architecture"
HEAD = "@startuml\nskinparam classAttributeIconSize 0\nskinparam shadowing false\nhide empty members\n"

D = {}

D["00_architecture"] = """@startuml
skinparam shadowing false
skinparam componentStyle rectangle
title netflx-web @676e5dd - component view (Part 1 baseline, 16 pattern types / 28 instances)
actor Viewer
package "Browser (React client components)" {
  [Pages: (shows) / (dashboard) / (auth)] as UI
  [Zustand stores\\nmodal / profile / search] as Stores
  [tRPC client proxies + link chain\\nlib/api/api.ts, lib/api/client.ts] as Client
  [React Query cache\\n(QueryClient)] as RQ
  [Error / loading boundaries\\nerror.tsx, global-error.tsx, loading.tsx] as EB
}
package "Next.js 13 server (Vercel/Node)" {
  [App Router server components\\n(shows pages, plans, account)] as RSC
  [lib/fetchers.ts\\nTMDB facade + scatter-gather] as Fetchers
  [lib/subscription.ts\\nplan resolution] as Sub
  [/api/trpc/(trpc)  front controller\\n(createNextApiHandler adapter)\\nappRouter: user, profile, icon, myList] as TRPC
  [tRPC middleware + ctx\\nenforceUserIsAuthed, createTRPCContext] as MW
  [/api/auth/(...nextauth)  front controller\\nGoogleProvider + PrismaAdapter] as Auth
  [/api/users/stripe  checkout] as Checkout
  [/api/webhooks/stripe] as Hook
  [Prisma client (singleton)] as Prisma
}
database "MySQL (relationMode = prisma)" as DB
cloud "TMDB API" as TMDB
cloud "Stripe" as Stripe
cloud "Google OAuth" as Google
Viewer --> UI
UI --> Stores : setState / subscribe
EB --> UI : wraps segments
UI --> Client : api.x.y.useQuery()
Client --> RQ
RQ --> TRPC : HTTP batch
TRPC --> MW
MW --> Prisma
UI ..> RSC : navigation
RSC --> Fetchers
Fetchers --> TMDB
RSC --> Sub
Sub --> Prisma
RSC --> Auth : getServerSession
Auth --> Google
Auth --> Prisma
UI --> Checkout : fetch POST
Checkout --> Stripe
Stripe --> Hook : checkout.session.completed\\ninvoice.payment_succeeded
Hook --> Prisma
Prisma --> DB
@enduml
"""

D["01_cor_authenticated_procedure_pipeline"] = HEAD + """title Chain of Responsibility - Authenticated Procedure Pipeline
interface "MiddlewareFunction\\n<<@trpc/server>>" as H {
  +({ctx, next}) : Promise<MiddlewareResult>
}
class "enforceUserIsAuthed\\n<<trpc.ts:109-119>>" as A {
  +({ctx, next}) : throws UNAUTHORIZED | next({ctx: session})
}
class "protectedProcedure\\n<<trpc.ts:129>>" as P {
  = t.procedure.use(enforceUserIsAuthed)
}
class "procedure resolver\\n(e.g. profile.getAll)" as R {
  +({ctx, input})
}
class "createNextApiHandler\\n<<[trpc].ts:8-19>>" as C
H <|.. A
P o--> A : first link
A --> R : next()
C --> P : invokes
@enduml
"""

D["02_singleton_shared_prisma_client"] = HEAD + """title Singleton - Shared Prisma Database Client
class "db.ts module" as M <<singleton holder>> {
  -globalForPrisma : {prisma?: PrismaClient}
  +prisma : PrismaClient = globalForPrisma.prisma ?? new PrismaClient()
}
class PrismaClient <<@prisma/client>>
class createInnerTRPCContext
class "authOptions.adapter" as AO
class getUserSubscriptionPlan
class "webhook POST" as W
M --> "1" PrismaClient : creates once
createInnerTRPCContext ..> M : import prisma
AO ..> M
getUserSubscriptionPlan ..> M
W ..> M
@enduml
"""

D["03_singleton_stripe_client"] = HEAD + """title Singleton (module) - Stripe API Client
class "lib/stripe.ts" as S <<module singleton>> {
  +stripe : Stripe = new Stripe(key, {apiVersion: 2022-11-15})
}
class Stripe <<stripe@12>>
class "webhooks/stripe POST" as A
class "users/stripe POST" as B
class PlansPage
class AccountPage
S --> "1" Stripe
A ..> S
B ..> S
PlansPage ..> S
AccountPage ..> S
@enduml
"""

OBS_HEAD = HEAD + """interface "StoreApi<T>\\n<<zustand>>" as Subject {
  +getState() : T
  +setState(partial)
  +subscribe(listener) : unsubscribe
}
"""

D["04_observer_show_modal_selection"] = OBS_HEAD + """title Observer - Show Modal Selection
class "useModalStore\\n<<stores/modal.ts:13-20>>" as CS {
  open : boolean
  show : Show | null
  play : boolean
}
class "ShowCard.onClick\\n<<shows-carousel.tsx:93-113>>" as Pub
class ShowsContainer <<observer>>
class ShowModal <<observer>>
class Hero <<observer>>
class ShowsGrid <<observer>>
Subject <|.. CS
Pub --> CS : setState({show, open, play})
CS --> ShowsContainer : notify (re-render)
CS --> ShowModal : notify
CS --> Hero : notify
CS --> ShowsGrid : notify
@enduml
"""

D["05_observer_active_profile_selection"] = OBS_HEAD + """title Observer - Active Profile Selection
class "useProfileStore\\n<<stores/profile.ts:12-27>>" as CS {
  profile : ProfileWithIcon | null
  pinForm : boolean
}
class "publishers:\\nProfilesScreen button, SiteHeader menu,\\nsiteConfig sign-out" as Pub
class ProfilesScreen <<observer>>
class PinForm <<observer>>
class ShowsContainer <<observer>>
class ShowModal <<observer>>
class SiteHeader <<observer>>
class MyShows <<observer>>
Subject <|.. CS
Pub --> CS : setState({profile, pinForm})
CS --> ProfilesScreen
CS --> PinForm
CS --> ShowsContainer
CS --> ShowModal
CS --> SiteHeader
CS --> MyShows
@enduml
"""

D["06_observer_search_results_broadcast"] = OBS_HEAD + """title Observer - Search Results Broadcast
class "useSearchStore\\n<<stores/search.ts:11-16>>" as CS {
  query : string
  shows : Show[]
}
class "SiteHeader.searchShowsByQuery\\n<<site-header.tsx:51-55>>" as Pub
class SiteHeader <<observer>>
class ShowsContainer <<observer>>
class Hero <<observer>>
class MainNav <<observer>>
class MyShows <<observer>>
Subject <|.. CS
Pub --> CS : setQuery / setShows
CS --> SiteHeader
CS --> ShowsContainer
CS --> Hero
CS --> MainNav
CS --> MyShows
@enduml
"""

D["07_decorator_persisted_profile_store"] = HEAD + """title Decorator - Persisted Profile Store
interface "StateCreator<ProfileState>\\n<<zustand>>" as C {
  +(set, get, api) : ProfileState
}
class "profile creator\\n<<profile.ts:15-20>>" as CC
class "persist(creator, {sessionStorage})\\n<<zustand/middleware>>" as P {
  wraps set: write to storage
  +api.persist.clearStorage()
}
class "devtools(creator)\\n<<zustand/middleware>>" as DV {
  wraps set: report action
}
class "create<ProfileState>()\\n<<profile.ts:12>>" as Client
C <|.. CC
C <|.. P
C <|.. DV
P o--> C : wraps
DV o--> C : wraps
Client --> DV : devtools(persist(creator))
@enduml
"""

D["08_adapter_nextauth_prisma"] = HEAD + """title Adapter - NextAuth Prisma Persistence Adapter
interface "Adapter\\n<<next-auth adapters.d.ts:57>>" as T {
  +createUser(user)
  +getUserByEmail(email)
  +linkAccount(account)
  +createSession(session)
  ...()
}
class "PrismaAdapter(p)\\n<<@next-auth/prisma-adapter index.js:206-264>>" as A {
  createUser: p.user.create({data})
  getUserByEmail: p.user.findUnique({where:{email}})
}
class "PrismaClient (prisma)\\n<<db.ts:9-14>>" as Ad {
  +user.create()
  +user.findUnique()
  +account.create()
}
class "NextAuth(authOptions)\\n<<auth.ts:38-64>>" as Cl
T <|.. A
A --> Ad : translates calls
Cl --> T : adapter
@enduml
"""

D["09_strategy_signin_provider"] = HEAD + """title Strategy - Sign-in Provider Strategy
interface "Provider\\n<<next-auth providers/index.d.ts:14>>" as S {
  id, type
  authorization / token / profile()
}
class "GoogleProvider({clientId, clientSecret})\\n<<auth.ts:50-53>>" as G
class "(GitHub, Email, Credentials...)\\nnot configured" as O #eeeeee
class "NextAuth(authOptions)\\nproviders: Provider[]" as Ctx {
  +signIn(providerId)
}
S <|.. G
S <|.. O
Ctx o--> "1..*" S : selects by id
@enduml
"""

D["10_facade_tmdb_catalogue"] = HEAD + """title Facade - TMDB Catalogue Facade
package "lib/fetchers.ts (Facade, module)" {
  class "getShows(mediaType)" as F1
  class "getNewAndPopularShows()" as F2
  class "searchShows(query)" as F3
}
package "Subsystem" {
  class "TMDB /trending, /top_rated" as T1
  class "TMDB /discover (genres, networks)" as T2
  class "TMDB /popular, /search/multi" as T3
  class "env.NEXT_PUBLIC_TMDB_API_KEY" as K
  class "fetch + JSON parse + error check" as J
}
class "Home / MoviesPage / TVShowsPage" as P1
class NewAndPopularPage
class "SiteHeader.searchShowsByQuery" as SH
P1 --> F1
NewAndPopularPage --> F2
SH --> F3
F1 --> T1
F1 --> T2
F1 --> J
F2 --> T3
F3 --> T3
F1 ..> K
F2 ..> K
F3 ..> K
@enduml
"""

D["11_composite_api_router_tree"] = HEAD + """title Composite - API Router Tree
interface "Router record entry\\nAnyRouter | AnyProcedure" as C
class "Router\\n(createTRPCRouter)" as R {
  _def.record : {key: Router | Procedure}
}
class "Procedure (leaf)" as L {
  query() / mutation()
}
C <|.. R
C <|.. L
R o--> "*" C : children
object "appRouter" as root
object "userRouter (4)" as u
object "profileRouter (7)" as p
object "iconRouter (4)" as i
object "myListRouter (4)" as m
root *-- u
root *-- p
root *-- i
root *-- m
@enduml
"""

PROXY = """class "AppRouter (type)\\n<<root.ts:20>>" as S
class "appRouter via createNextApiHandler\\n<<[trpc].ts:8-19>>" as RS
"""

D["12_proxy_pages_router_trpc_client"] = HEAD + """title Proxy - Pages-Router tRPC Client Proxy
""" + PROXY + """class "api = createTRPCNext<AppRouter>\\n<<lib/api/api.ts:21-54>>\\n(JS Proxy)" as P {
  +[router].[proc].useQuery()
  +[router].[proc].useMutation()
  +useContext()
}
class "httpBatchLink(/api/trpc)" as L
class "ShowsContainer, ShowModal,\\nProfilesScreen, ..." as Cl
S <|.. RS
S <|.. P : typed as
P --> L
L --> RS : HTTP
Cl --> P
@enduml
"""

D["13_proxy_app_router_trpc_client"] = HEAD + """title Proxy - App-Router tRPC Client Proxy
""" + PROXY + """class "api = createTRPCNextBeta<AppRouter>\\n<<lib/api/client.ts:22-45>>" as P
class "createFlatProxy(key => ...)\\n<<createTrpcNextBeta.tsx:76-92>>" as FP
class "TRPCProvider\\n<<context/trpc-provider.tsx>>" as Prov
class "AddProfileForm, EditProfileForm" as Cl
S <|.. RS
S <|.. P : typed as
P --> FP : built by
FP --> RS : hooks -> HTTP batch
Prov --> P : api.Provider
Cl --> P
@enduml
"""

D["14_cache_my_list_query_cache"] = HEAD + """title Read-Through Cache - My List Query Cache
class "QueryClient\\n<<createTrpcNextBeta.tsx:55-63>>" as Q {
  staleTime = Infinity, cacheTime = Infinity
  +fetchQuery(key, loader)
  +invalidateQueries(key)
}
class "ShowsContainer.myShowsQuery" as R1
class "ShowModal.myShowsQuery" as R2
class "ShowModal effect\\ninvalidate on mutation" as I
class "myList.getAll (loader)\\n<<my-list.ts:7-12>>" as L
R1 --> Q : useQuery(profileId)
R2 --> Q : useQuery(profileId)
I --> Q : invalidate
Q --> L : on miss / after invalidate
@enduml
"""

D["15_proxy_environment_secret_guard"] = HEAD + """title Proxy (protection) - Environment Secret Guard
interface "MergedOutput\\n<<env.mjs:67-71>>" as S {
  DATABASE_URL, STRIPE_API_KEY, ...
  NEXT_PUBLIC_TMDB_API_KEY, ...
}
class "parsed.data\\n(zod validated)" as RS
class "env = new Proxy(parsed.data, {get})\\n<<env.mjs:92-105>>" as P {
  get(target, prop): throw if client && !NEXT_PUBLIC_
}
class "lib/stripe.ts, server/db.ts,\\nlib/fetchers.ts ... (10 modules)" as C
S <|.. RS
S <|.. P
P --> RS : forwards allowed reads
C --> P : env.X
@enduml
"""


# ---- added 2026-10-29: diagrams for the second-pass instances ----
D["16_front_controller_trpc_api"] = HEAD + """title Front Controller - tRPC API Front Controller
class "Browser httpBatchLink\\nPOST /api/trpc/a,b,c" as Cl
class "createNextApiHandler({router, createContext, onError})\\n<<pages/api/trpc/[trpc].ts:8-19>>" as FC {
  +handler(req, res)
  -getPath(): req.query.trpc
}
class "createTRPCContext\\n<<trpc.ts:60-69>>" as Ctx
class "onError (dev logger)\\n<<[trpc].ts:11-18>>" as Err
class "nodeHTTPRequestHandler / resolveHTTPResponse\\n<<@trpc/server@10.28.0>>" as D {
  +callProcedure(path, input, ctx)
}
class "appRouter (command registry)\\n<<root.ts:12-17>>" as Reg
class "procedure e.g. profile.getAll\\n<<profile.ts:7-15>>" as P
Cl --> FC : every tRPC call
FC --> Ctx : once per request
FC --> D : delegates
D --> Reg : lookup(path)
Reg o--> "19" P
D --> P : invoke
D ..> Err : TRPCError
@enduml
"""

D["17_front_controller_nextauth"] = HEAD + """title Front Controller - NextAuth Auth Route Front Controller
class "LoginButton signIn('google')\\nSiteHeader signOut()" as Cl
class "NextAuth(authOptions)\\n<<pages/api/auth/[...nextauth].ts:4>>" as FC
class "NextAuthApiHandler\\nreq.query.nextauth -> {action, providerId}\\n<<next-auth next/index.js:18-31>>" as Parse
class "AuthHandler switch(action)\\n<<next-auth core/index.js:159-206,257-340>>" as D
class "routes: providers / session / csrf /\\nsignin / callback / signout" as R
class "authOptions\\n(adapter, providers, callbacks)\\n<<auth.ts:38-64>>" as Opt
Cl --> FC : /api/auth/*
FC --> Parse
Parse --> D
D --> R : dispatch by action
D --> Opt : shared config
@enduml
"""

D["18_adapter_trpc_next_handler"] = HEAD + """title Adapter - tRPC Next.js API Handler Adapter
interface "NextApiHandler (Target)\\n(req: NextApiRequest, res: NextApiResponse)\\n<<next@13.4.4>>" as T
class "createNextApiHandler(opts) (Adapter)\\n<<@trpc/server adapters/next.js:16-56>>" as A {
  +(req, res): path = req.query.trpc
}
class "nodeHTTPRequestHandler (Adaptee)\\nframework-neutral tRPC resolution" as Ad
class "Next.js pages router\\n(Client)" as C
class "createTRPCContext(opts: CreateNextContextOptions)\\n<<trpc.ts:60-69>>" as Ctx
T <|.. A
A --> Ad : nodeHTTPRequestHandler({...opts, req, res, path})
C --> T : calls default export
Ad ..> Ctx : createContext({req, res})
@enduml
"""

D["19_cor_trpc_client_link_chain"] = HEAD + """title Chain of Responsibility - tRPC Client Link Chain
interface "TRPCLink (Handler)\\n(op, next) => Observable" as H
class "createChain execute(index)\\n<<@trpc/client splitLink-*.js:4-23>>" as Chain
class "loggerLink({enabled})\\n<<client.ts:36-40>>" as L {
  log if dev or error; next(op)
}
class "httpBatchLink({url: /api/trpc})\\n<<client.ts:41-43>>" as B {
  terminal: HTTP request, no next
}
class "links: [loggerLink, httpBatchLink]\\n<<client.ts:35-44>>" as Asm
class "trpc.createClient in TRPCProvider\\n<<createTrpcNextBeta.tsx:55-63>>" as Cl
H <|.. L
H <|.. B
Chain --> H : links[index]
L --> B : next(op)
Asm --> L
Asm --> B
Cl --> Chain : every query/mutation
note bottom of Asm : identical array in lib/api/api.ts:36-45\\nis never executed (withTRPC not mounted)
@enduml
"""

D["20_builder_trpc_procedure_builder"] = HEAD + """title Builder - tRPC Procedure Builder
class "ProcedureBuilder (immutable)\\n<<@trpc/server index.js:326-438>>" as B {
  +input(parser): ProcedureBuilder
  +output(parser): ProcedureBuilder
  +meta(m): ProcedureBuilder
  +use(middleware): ProcedureBuilder
  +query(resolver): Procedure
  +mutation(resolver): Procedure
}
class "Procedure (Product)\\ncreateProcedureCaller(_def)" as P
object "t = initTRPC.context().create()\\n<<trpc.ts:71-83>>" as T
object "publicProcedure = t.procedure\\n<<trpc.ts:106>>" as Pub
object "protectedProcedure = t.procedure.use(enforceUserIsAuthed)\\n<<trpc.ts:129>>" as Pro
class "routers (Director)\\nprotectedProcedure.input(z.string()).query(fn)\\n<<profile.ts:17-28>>" as Dir
T --> Pub : creates
Pub ..> Pro : .use() returns new builder
Dir --> Pro : starts from
Dir --> B : chain steps
B --> P : query()/mutation() build
@enduml
"""

D["21_context_object_trpc_request"] = HEAD + """title Context Object - tRPC Request Context
class "createTRPCContext({req, res})\\n(ContextFactory) <<trpc.ts:60-69>>" as F
class "createInnerTRPCContext({session})\\n<<trpc.ts:47-52>>" as I
class "ctx (Context Object)" as C {
  session: Session | null
  prisma: PrismaClient
}
class "enforceUserIsAuthed\\nnext({ctx: {session: non-null}})\\n<<trpc.ts:109-119>>" as R
class "resolvers\\nctx.prisma / ctx.session.user.id\\n<<routers/*.ts>>" as U
class "getServerAuthSession(req, res)\\n<<auth.ts:71-76>>" as S
F --> S : once per request
F --> I
I --> C : builds
R --> C : refines (copy)
U --> C : reads only ctx
@enduml
"""

D["22_strategy_wire_serialization"] = HEAD + """title Strategy - Wire Serialization Transformer
interface "DataTransformer (Strategy)\\nserialize(v) / deserialize(v)\\n<<@trpc/server config-*.js:11-21>>" as S
class "defaultTransformer (identity)\\n<<config-*.js:22-30>>" as D #eeeeee
class "superjson (selected)\\n<<superjson@1.12.3>>" as SJ
class "initTRPC...create({transformer: superjson})\\nserver context <<trpc.ts:71-72>>" as Srv
class "createTRPCNextBeta({transformer: superjson})\\nclient context <<client.ts:22-23>>" as Cli
class "createHydrateClient({transformer: superjson})\\n<<client.ts:51-53>>" as H
S <|.. D
S <|.. SJ
Srv o--> S
Cli o--> S
H o--> S
@enduml
"""

D["23_observer_search_input_dom_events"] = HEAD + """title Observer - Search Input DOM Event Listeners
interface "EventTarget (Subject)\\naddEventListener / removeEventListener" as S
class "document\\n(mousedown, touchstart)" as Doc
class "window\\n(keydown)" as Win
interface "EventListener (Observer)" as O
class "useOnClickOutside listener\\n<<use-on-click-outside.ts:8-14>>" as L1
class "DebouncedInput handleKeyDown\\n<<debounced-input.tsx:53-71>>" as L2
class "DebouncedInput (rendered by SiteHeader)\\nregisters in useEffect, cleanup unregisters" as C
S <|.. Doc
S <|.. Win
O <|.. L1
O <|.. L2
Doc o--> "*" O : notifies
Win o--> "*" O : notifies
C --> L1 : useOnClickOutside(ref, closeInput)
C --> L2
@enduml
"""

D["24_error_boundary_shows_segment"] = HEAD + """title Error Boundary - Shows Segment Error Boundary
class "ErrorBoundaryHandler\\n<<next@13.4.4 error-boundary.js:53-110>>" as B {
  getDerivedStateFromError(e)
  reset()
}
class "(shows)/error.tsx Error\\n<<error.tsx:10-12>>" as F
class "ErrorScreen(error, reset)\\n<<error-screen.tsx:9-31>>" as V
class "ShowsLayout children\\nHome / Movies / TV / New & Popular / My List" as P
class "getShows throws 'Failed to fetch shows'\\n<<fetchers.ts:42-53>>" as E
B --> P : renders children
P ..> E : may throw
B --> F : on error renders fallback
F --> V
V ..> B : Retry -> reset()
@enduml
"""

D["25_error_boundary_root_global"] = HEAD + """title Error Boundary - Root Global Error Boundary
class "ErrorBoundaryHandler (root)\\n<<next@13.4.4 error-boundary.js:53-110>>" as B
class "GlobalError renders own <html><body>\\n<<global-error.tsx:10-18>>" as F
class "ErrorScreen\\n<<error-screen.tsx:9-31>>" as V
class "RootLayout\\nTRPCProvider, html, body, Toast, Analytics\\n<<layout.tsx:78-98>>" as R
class "(shows) segment boundary" as Inner
B --> R : protects
R --> Inner : contains
B --> F : layout error -> fallback
F --> V
@enduml
"""

D["26_suspense_shows_loading_placeholder"] = HEAD + """title Suspense Boundary - Shows Loading Placeholder
class "LoadingBoundary -> React.Suspense\\n<<next@13.4.4 layout-router.js:335-345>>" as B {
  fallback = loading component
}
class "ShowsLoading skeleton\\n<<(shows)/loading.tsx:3-9>>" as F
class "Home (async server page)\\nawait getShows('movie')\\n<<(shows)/page.tsx:8-52>>" as P
B --> F : while child suspends
B --> P : renders when resolved
note bottom of B : explicit <Suspense> around client forms\\n(account/users, help-center) never suspend -> rejected
@enduml
"""

D["27_scatter_gather_tmdb_rows"] = HEAD + """title Scatter-Gather - TMDB Row Scatter-Gather
class "getShows(mediaType)\\n<<fetchers.ts:5-77>>" as G1 {
  scatter: Promise.all(8 x fetch) <<6-40>>
  gather: any !ok -> throw; json(); aggregate <<42-76>>
}
class "getNewAndPopularShows()\\n<<fetchers.ts:82-122>>" as G2 {
  scatter: Promise.all(4 x fetch) <<83-97>>
  gather <<99-121>>
}
class "TMDB endpoints (Recipients)\\ntrending, top_rated, discover x6, popular" as R
class "Home / Movies / TV / New & Popular pages" as C
C --> G1
C --> G2
G1 --> "8" R : concurrent
G2 --> "4" R : concurrent
note bottom of G1 : CH02: both replaced by generic fetchRows(rows, errorMessage)
@enduml
"""

D["28_cache_profile_account_query"] = HEAD + """title Read-Through Cache - Profile and Account Query Cache
class "QueryClient (shared)\\nstaleTime/cacheTime Infinity\\n<<createTrpcNextBeta.tsx:55-63>>" as Q
class "profile.getAll / getOthers / getOne\\nuser.getCurrent / getCurrentWithProfile\\n(loaders)" as L
class "Readers: ProfilesScreen, ManageProfiles,\\nSiteHeader, AccountForm, IconPicker" as R
class "Invalidators: AddProfileForm, EditProfileForm,\\nResetPinForm, AccountForm, EditUserForm\\napiUtils.profile.getAll.invalidate()" as I
R --> Q : useQuery(key)
Q --> L : miss / after invalidate
I --> Q : invalidate(key) after mutation
@enduml
"""


def main(names=None):
    jar = os.environ.get("PLANTUML_JAR", os.path.expanduser("~/tools/plantuml.jar"))
    for name, src in D.items():
        with open(os.path.join(OUT, name + ".puml"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(src)
    files = [os.path.join(OUT, n + ".puml") for n in (names or D)]
    # without Graphviz on PATH, use PlantUML's built-in smetana layout engine
    layout = [] if shutil.which("dot") else ["-Playout=smetana"]
    subprocess.run(["java", "-jar", jar, *layout, "-tpng", *files], check=True)
    print("rendered", len(files))

if __name__ == "__main__":
    main(sys.argv[1:] or None)
