"""Builds Part2/pattern_evalution.csv and Part 2 rows of Part2/Pattern_count.csv.

Run from A12/ after run_snapshots.sh (needs worktrees /tmp/a12-<snapshot>):
    python3 data/test_result/part2/part2_evolution.py
Locations are computed with locate.span() from anchors so line numbers are exact for
each snapshot. Baseline rows are copied unchanged from Part1/patterns.csv.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from locate import span  # noqa: E402

# Worktrees of the a12-evolution branch (see README "Reproduce"); override the prefix with
# A12_WORKTREE_PREFIX, e.g. C:/Users/<me>/AppData/Local/Temp/a12/wt-  (default /tmp/a12-)
WT = os.environ.get("A12_WORKTREE_PREFIX", "/tmp/a12-")
VERSIONS = [  # name, commit, worktree, path prefix used in CSV
    ("CH01", "3f79642", WT + "CH01", "commit 3f79642:"),
    ("CH02", "e420dcf", WT + "CH02", "commit e420dcf:"),
    ("CH03", "f393031", WT + "CH03", "Part2/code/"),
]
ORDER = {"baseline": 0, "CH01": 1, "CH02": 2, "CH03": 3}

T, P, R, F = "src/server/api/trpc.ts", "src/server/api/routers/profile.ts", "src/server/api/root.ts", "src/lib/fetchers.ts"
SC, SM, HE, SH = "src/components/shows-container.tsx", "src/components/show-modal.tsx", "src/components/hero.tsx", "src/components/layouts/site-header.tsx"
RU, PO, CA, ML = "src/lib/access/rules.ts", "src/lib/access/policy.ts", "src/server/api/routers/catalogue.ts", "src/server/api/routers/my-list.ts"


def role(r, sym, file=None, anchor=None, dep=None, since="baseline", until=None, through=None):
    return dict(role=r, sym=sym, file=file, anchor=anchor, dep=dep, since=since, until=until, through=through)


# status per version and the change description (empty for "preserved" defaults)
INSTANCES = [
    dict(name="Authenticated Procedure Pipeline", pattern="Chain of Responsibility", ptype="Behavioral (GoF); tRPC middleware idiom",
         roles=[role("Handler", "tRPC MiddlewareFunction (t.middleware)", dep="dependency @trpc/server@10.28.0"),
                role("ConcreteHandler", "enforceUserIsAuthed", T, r"^const enforceUserIsAuthed"),
                role("ConcreteHandler", "attachSubscription", T, r"^const attachSubscription", since="CH01"),
                role("Chain assembly", "protectedProcedure = t.procedure.use(enforceUserIsAuthed)", T, r"^export const protectedProcedure"),
                role("Chain assembly", "subscribedProcedure = protectedProcedure.use(attachSubscription)", T, r"^export const subscribedProcedure", since="CH01"),
                role("Terminal handler", "profile.create resolver (uses ctx.maxProfiles)", P, r"^  create: subscribedProcedure", since="CH01"),
                role("Terminal handler", "catalogue.checkAccess resolver", CA, r"^  checkAccess: subscribedProcedure", since="CH01"),
                role("Client", "createNextApiHandler", "src/pages/api/trpc/[trpc].ts", r"^export default createNextApiHandler")],
         status={"CH01": "extended", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Added ConcreteHandler attachSubscription after enforceUserIsAuthed (subscribedProcedure). It loads the plan once per request and passes tier/maxProfiles down the chain; profile.create and catalogue.checkAccess use it. A denial in the first link still stops the chain before the DB lookup.",
                 "CH02": "Chain unchanged; createTRPCContext additionally resolves ctx.region from geo headers.",
                 "CH03": "Chain unchanged; catalogue.checkAccess resolver now also loads the profile maturity."},
         evidence="enforceUserIsAuthed throws UNAUTHORIZED or calls next({ctx}); attachSubscription calls getUserSubscriptionPlan(userId, ctx.prisma) and next({ctx:{subscription, planTier, maxProfiles}}). Tests: characterization 'rejects anonymous callers', ch01 'still rejects anonymous callers first', ch01 profile limit tests."),
    dict(name="Shared Prisma Database Client", pattern="Singleton", ptype="Creational (GoF)",
         roles=[role("Singleton", "prisma (PrismaClient instance)", "src/server/db.ts", r"^export const prisma"),
                role("Instance holder", "globalForPrisma", "src/server/db.ts", r"^const globalForPrisma"),
                role("Client", "createInnerTRPCContext", T, r"^const createInnerTRPCContext"),
                role("Client", "getUserSubscriptionPlan (default db parameter)", "src/lib/subscription.ts", r"^export async function getUserSubscriptionPlan")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Singleton unchanged. getUserSubscriptionPlan now takes db = prisma as a default parameter so the middleware can pass ctx.prisma (same instance in production, a fake in tests)."},
         evidence="db.ts unchanged in all snapshots; all server code still imports the one `prisma` export."),
    dict(name="Stripe API Client", pattern="Singleton", ptype="Creational (GoF); ES-module singleton idiom",
         roles=[role("Singleton", "stripe (Stripe instance)", "src/lib/stripe.ts", r"^export const stripe"),
                role("Client", "Stripe webhook POST", "src/app/api/webhooks/stripe/route.ts", r"^export async function POST"),
                role("Client", "checkout/portal POST", "src/app/api/users/stripe/route.ts", r"^export async function POST")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Unchanged; checkout POST now rejects a plan without a Stripe price before using the client."},
         evidence="lib/stripe.ts unchanged; clients unchanged except the early 400 guard in checkout."),
    dict(name="Show Modal Selection", pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
         roles=[role("Subject", "zustand StoreApi", dep="dependency zustand@4.3.8"),
                role("ConcreteSubject", "useModalStore", "src/stores/modal.ts", r"^export const useModalStore"),
                role("Publisher", "ShowCard onClick", "src/components/shows-carousel.tsx", r"^const ShowCard"),
                role("ConcreteObserver", "ShowsContainer", SC, r"^const ShowsContainer"),
                role("ConcreteObserver", "ShowModal", SM, r"^const ShowModal"),
                role("ConcreteObserver", "Hero", HE, r"^const Hero"),
                role("ConcreteObserver", "ShowsGrid", "src/components/shows-grid.tsx", r"^const ShowsGrid")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Same subject/observers. ShowModal additionally queries catalogue.checkAccess for the newly selected show and renders 'Upgrade to watch' when denied."},
         evidence="useModalStore unchanged; ShowModal still re-renders on {show, open, play} changes."),
    dict(name="Active Profile Selection", pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
         roles=[role("Subject", "zustand StoreApi", dep="dependency zustand@4.3.8"),
                role("ConcreteSubject", "useProfileStore", "src/stores/profile.ts", r"^export const useProfileStore"),
                role("ConcreteObserver", "ProfilesScreen", "src/components/screens/profiles-screen.tsx", r"^const ProfilesScreen"),
                role("ConcreteObserver", "PinForm", "src/components/forms/pin-form.tsx", r"^const PinForm"),
                role("ConcreteObserver", "ShowsContainer", SC, r"^const ShowsContainer"),
                role("ConcreteObserver", "ShowModal", SM, r"^const ShowModal"),
                role("ConcreteObserver", "SiteHeader", SH, r"^const SiteHeader"),
                role("ConcreteObserver", "MyShows", "src/components/my-shows.tsx", r"^const MyShows"),
                role("ConcreteObserver", "Hero (selector on profile.maturityLevel)", HE, r"^const Hero", since="CH03")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "extended"},
         change={"CH03": "Hero subscribes to useProfileStore (selector state.profile?.maturityLevel) - a new observer. ShowsContainer reacts to the selected profile's maturityLevel by filtering rows, search results and My List; ShowModal sends profileId to checkAccess."},
         evidence="Selecting a Kids profile in ProfilesScreen publishes it; Hero/ShowsContainer recompute profileVisibleShows(…, maturityLevel). Tests: ch03 'profileVisibleShows filters rows for restricted profiles only'."),
    dict(name="Search Results Broadcast", pattern="Observer", ptype="Behavioral (GoF); Zustand store subscription",
         roles=[role("Subject", "zustand StoreApi", dep="dependency zustand@4.3.8"),
                role("ConcreteSubject", "useSearchStore", "src/stores/search.ts", r"^export const useSearchStore"),
                role("Publisher", "SiteHeader.searchShowsByQuery", SH, r"^  async function searchShowsByQuery"),
                role("ConcreteObserver", "SiteHeader", SH, r"^const SiteHeader"),
                role("ConcreteObserver", "ShowsContainer", SC, r"^const ShowsContainer"),
                role("ConcreteObserver", "Hero", HE, r"^const Hero"),
                role("ConcreteObserver", "MainNav", "src/components/layouts/main-nav.tsx", r"^export function MainNav"),
                role("ConcreteObserver", "MyShows", "src/components/my-shows.tsx", r"^const MyShows")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "modified"},
         change={"CH03": "Observer ShowsContainer now filters the broadcast results for the active profile before rendering ShowsGrid. Subject and publisher unchanged."},
         evidence="shows-container: `return <ShowsGrid shows={forProfile(searchStore.shows)} />`."),
    dict(name="Persisted Profile Store", pattern="Decorator", ptype="Structural (GoF); Zustand middleware",
         roles=[role("Component", "StateCreator<ProfileState>", dep="dependency zustand@4.3.8"),
                role("ConcreteComponent", "profile creator", "src/stores/profile.ts", r"^      \(set\) => \(\{"),
                role("ConcreteDecorator", "persist(…, sessionStorage)", "src/stores/profile.ts", r"^    persist\("),
                role("ConcreteDecorator", "devtools(…)", "src/stores/profile.ts", r"^  devtools\(")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH03": "Unchanged code, but the persisted profile object now also carries maturityLevel; a rating changed in another tab is only picked up when the profile is selected again (limitation)."},
         evidence="stores/profile.ts unchanged in all snapshots."),
    dict(name="NextAuth Prisma Persistence Adapter", pattern="Adapter", ptype="Structural (GoF)",
         roles=[role("Target", "Adapter", dep="dependency next-auth@4.22.1 adapters.d.ts:57"),
                role("Adapter", "PrismaAdapter(p)", dep="dependency @next-auth/prisma-adapter@1.0.6 dist/index.js:206-264"),
                role("Adaptee", "prisma (PrismaClient)", "src/server/db.ts", r"^export const prisma"),
                role("Client", "authOptions", "src/server/auth.ts", r"^export const authOptions")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"}, change={},
         evidence="auth.ts unchanged in all snapshots."),
    dict(name="Sign-in Provider Strategy", pattern="Strategy", ptype="Behavioral (GoF)",
         roles=[role("Strategy", "Provider", dep="dependency next-auth@4.22.1 providers/index.d.ts:14"),
                role("ConcreteStrategy", "GoogleProvider", "src/server/auth.ts", r"^    GoogleProvider\("),
                role("Context", "authOptions.providers / NextAuth", "src/server/auth.ts", r"^export const authOptions")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"}, change={},
         evidence="auth.ts unchanged in all snapshots."),
    dict(name="TMDB Catalogue Facade", pattern="Facade", ptype="Structural (GoF)",
         roles=[role("Facade", "module lib/fetchers.ts: getShows", F, r"^export async function getShows"),
                role("Facade operation", "getNewAndPopularShows", F, r"^export async function getNewAndPopularShows"),
                role("Facade operation", "searchShows", F, r"^export async function searchShows"),
                role("Subsystem helper", "fetchRows + tmdbUrl + SHOW_ROWS/NEW_AND_POPULAR_ROWS", F, r"^async function fetchRows", since="CH02"),
                role("Client", "Home", "src/app/(shows)/page.tsx", r"^export default async function Home"),
                role("Client", "SiteHeader.searchShowsByQuery", SH, r"^  async function searchShowsByQuery")],
         status={"CH01": "modified", "CH02": "modified", "CH03": "preserved"},
         change={"CH01": "getShows marks the originals row (network 213) with isPremium: true; interface otherwise unchanged.",
                 "CH02": "Refactored inside the facade: rows are data (SHOW_ROWS, NEW_AND_POPULAR_ROWS) and one fetchRows helper replaces 12 copied fetch/ok/json blocks. Public functions, URLs, order, keys and errors unchanged (characterization tests pass on old and new code); max CCN of the file 9 -> 3."},
         evidence="tests/characterization*.test.ts pin URLs/order/keys/errors; run on 676e5dd (19/19) and on every later snapshot."),
    dict(name="API Router Tree", pattern="Composite", ptype="Structural (GoF); tRPC router tree",
         roles=[role("Component", "AnyRouter | AnyProcedure", dep="dependency @trpc/server@10.28.0"),
                role("Composite (root)", "appRouter", R, r"^export const appRouter"),
                role("Composite", "userRouter", "src/server/api/routers/user.ts", r"^export const userRouter"),
                role("Composite", "profileRouter", P, r"^export const profileRouter"),
                role("Composite", "iconRouter", "src/server/api/routers/icon.ts", r"^export const iconRouter"),
                role("Composite", "myListRouter", ML, r"^export const myListRouter"),
                role("Composite", "catalogueRouter", CA, r"^export const catalogueRouter", since="CH01"),
                role("Factory", "createTRPCRouter", T, r"^export const createTRPCRouter")],
         status={"CH01": "extended", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "New sub-composite catalogueRouter (leaf checkAccess) added to appRouter; clients reach it as api.catalogue.checkAccess with no client change. Leaves 19 -> 20."},
         evidence="root.ts adds `catalogue: catalogueRouter`; AppRouter type grows automatically."),
    dict(name="Pages-Router tRPC Client Proxy", pattern="Proxy", ptype="Structural (GoF); remote proxy",
         roles=[role("Subject", "AppRouter type", R, r"^export type AppRouter"),
                role("RealSubject", "createNextApiHandler", "src/pages/api/trpc/[trpc].ts", r"^export default createNextApiHandler"),
                role("Proxy", "api = createTRPCNext<AppRouter>", "src/lib/api/api.ts", r"^export const api"),
                role("Client", "ShowModal (catalogue.checkAccess query)", SM, r"^  const accessQuery", since="CH01")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Proxy code unchanged; because it is typed from AppRouter it exposes the new catalogue.checkAccess automatically (new client: ShowModal)."},
         evidence="lib/api/api.ts unchanged in all snapshots."),
    dict(name="App-Router tRPC Client Proxy", pattern="Proxy", ptype="Structural (GoF); remote proxy",
         roles=[role("Subject", "AppRouter type", R, r"^export type AppRouter"),
                role("Proxy", "api = createTRPCNextBeta<AppRouter>", "src/lib/api/client.ts", r"^export const api"),
                role("Proxy factory", "createTRPCNextBeta", "src/@trpc/next-layout/client/createTrpcNextBeta.tsx", r"^export function createTRPCNextBeta"),
                role("Provider", "TRPCProvider", "src/context/trpc-provider.tsx", r"^const TRPCProvider")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH03": "Unchanged; EditProfileForm (client of this proxy) now sends maturityLevel."},
         evidence="lib/api/client.ts and createTrpcNextBeta.tsx unchanged."),
    dict(name="Environment Secret Guard", pattern="Proxy", ptype="Structural (GoF); protection proxy",
         roles=[role("RealSubject", "parsed.data", "src/env.mjs", r"^if \(!!process.env.SKIP_ENV_VALIDATION"),
                role("Proxy", "env = new Proxy(parsed.data, {get})", "src/env.mjs", r"^  env = new Proxy"),
                role("Client", "config/subscriptions.ts (server-only price ids)", "src/config/subscriptions.ts", r"^const stripePriceIds", since="CH01")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "Proxy unchanged; schema gained optional STRIPE_ULTRA_PRICE_ID. The guard is why plan data had been duplicated: the new client-safe config/plan-catalog.ts holds only public data, and only subscriptions.ts reads secrets through the proxy."},
         evidence="env.mjs get trap unchanged."),
    dict(name="My List Query Cache", pattern="Read-Through Cache", ptype="Architecture (caching); React Query",
         roles=[role("Cache", "QueryClient in TRPCProvider", "src/@trpc/next-layout/client/createTrpcNextBeta.tsx", r"^  const TRPCProvider"),
                role("Cache policy", "staleTime/cacheTime Infinity", "src/lib/api/client.ts", r"^  queryClientConfig"),
                role("Loader", "myListRouter.getAll", ML, r"^  getAll: protectedProcedure"),
                role("Reader", "ShowsContainer myShowsQuery", SC, r"^  const myShowsQuery"),
                role("Invalidator", "ShowModal effect", SM, r"^  const mutationCount = useIsMutating", through=r"^  \}, \[apiUtils, mutationCount\]\)")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH03": "Cache unchanged; cached My List data is filtered for the profile after it is read (filtering never changes the cached entry)."},
         evidence="Readers and invalidation unchanged; catalogue.checkAccess results are cached under their own key."),
    # ---- newly introduced collaborations (Part 2) ----
    dict(name="Content Access Rule Chain", pattern="Chain of Responsibility", ptype="Behavioral (GoF)",
         roles=[role("Handler", "AccessRule (abstract, setNext/check)", RU, r"^export abstract class AccessRule", since="CH01"),
                role("ConcreteHandler", "RegionRule", RU, r"^export class RegionRule", since="CH02"),
                role("ConcreteHandler", "MaturityRule", RU, r"^export class MaturityRule", since="CH03"),
                role("ConcreteHandler", "PremiumContentRule", RU, r"^export class PremiumContentRule", since="CH01"),
                role("Chain assembly", "buildAccessChain / contentAccessChain", PO, r"^export function contentAccessChain", since="CH01"),
                role("Client", "checkAccess / visibleShows / profileVisibleShows", PO, r"^export function checkAccess", since="CH01"),
                role("Client", "catalogue.checkAccess", CA, r"^  checkAccess: subscribedProcedure", since="CH01"),
                role("Client", "toCategories (server rows)", "src/lib/catalogue.ts", r"^export function toCategories", since="CH02"),
                role("Client", "myList.create maturity guard", ML, r"^  create: protectedProcedure", since="CH03")],
         status={"CH01": "newly_introduced", "CH02": "extended", "CH03": "extended"},
         change={"CH01": "Student-added. AccessRule handlers linked by setNext; PremiumContentRule denies premium titles below tier 3 (visibility locked).",
                 "CH02": "RegionRule linked at the FRONT of the chain (hidden before locked); visibleShows and toCategories filter rows on the server.",
                 "CH03": "MaturityRule linked between RegionRule and PremiumContentRule; profileVisibleShows builds a one-link chain for the browser; myList.create uses a MaturityRule chain."},
         evidence="AccessRule.check returns the first denial or forwards to next; order verified by ch02 'region runs before premium' and ch03 'chain order is region -> maturity -> premium'."),
    dict(name="Access Rule Evaluation Template", pattern="Template Method", ptype="Behavioral (GoF)",
         roles=[role("AbstractClass", "AccessRule", RU, r"^export abstract class AccessRule", since="CH01"),
                role("TemplateMethod", "AccessRule.check", RU, r"^  check\(show", since="CH01"),
                role("PrimitiveOperation", "AccessRule.evaluate (abstract)", RU, r"^  protected abstract evaluate", since="CH01"),
                role("ConcreteClass", "RegionRule.evaluate", RU, r"^export class RegionRule", since="CH02"),
                role("ConcreteClass", "MaturityRule.evaluate", RU, r"^export class MaturityRule", since="CH03"),
                role("ConcreteClass", "PremiumContentRule.evaluate", RU, r"^export class PremiumContentRule", since="CH01")],
         status={"CH01": "newly_introduced", "CH02": "extended", "CH03": "extended"},
         change={"CH01": "Student-added. check() fixes the algorithm (evaluate, stop on denial, else forward/allow); subclasses only implement evaluate().",
                 "CH02": "New ConcreteClass RegionRule.", "CH03": "New ConcreteClass MaturityRule."},
         evidence="Same classes as the Content Access Rule Chain but a separate collaboration: inheritance-based fixed algorithm vs. the object links of the chain."),
    # ---- added 2026-10-29 (second Part 1 pass): instances that were not tracked before ----
    dict(name="tRPC API Front Controller", pattern="Front Controller", ptype="Architectural (Fowler PoEAA); Next.js API route",
         roles=[role("FrontController", "createNextApiHandler at /api/trpc/[trpc]", "src/pages/api/trpc/[trpc].ts", r"^export default createNextApiHandler"),
                role("Shared pre-processing", "createTRPCContext", T, r"^export const createTRPCContext"),
                role("Dispatcher", "nodeHTTPRequestHandler -> resolveHTTPResponse -> callProcedure(path)", dep="dependency @trpc/server@10.28.0 dist/nodeHTTPRequestHandler-5bbf93f1.js:7-34"),
                role("Command registry", "appRouter", R, r"^export const appRouter"),
                role("ConcreteCommand", "catalogue.checkAccess", CA, r"^  checkAccess: subscribedProcedure", since="CH01")],
         status={"CH01": "extended", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "New command catalogue.checkAccess registered in appRouter; it is reached through the same /api/trpc controller without a new route file.",
                 "CH02": "Controller unchanged; the shared pre-processing step (createTRPCContext) now also resolves the viewer region from request headers.",
                 "CH03": "Controller unchanged."},
         evidence="Same single route file in every snapshot; new procedures only add entries to appRouter. ch01/ch02/ch03 tests call procedures through appRouter.createCaller, the same dispatch table the controller uses."),
    dict(name="NextAuth Auth Route Front Controller", pattern="Front Controller", ptype="Architectural (Fowler PoEAA); NextAuth catch-all route",
         roles=[role("FrontController", "NextAuth(authOptions) at /api/auth/[...nextauth]", "src/pages/api/auth/[...nextauth].ts", r"^export default NextAuth"),
                role("Dispatcher", "AuthHandler switch (action)", dep="dependency next-auth@4.22.1 core/index.js:159-206"),
                role("Configuration", "authOptions", "src/server/auth.ts", r"^export const authOptions")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={},
         evidence="Files unchanged by CH01-CH03."),
    dict(name="tRPC Next.js API Handler Adapter", pattern="Adapter", ptype="Structural (GoF); tRPC framework adapter",
         roles=[role("Adapter", "createNextApiHandler", dep="dependency @trpc/server@10.28.0 dist/adapters/next.js:16-56"),
                role("Adapted context type", "createTRPCContext(opts: CreateNextContextOptions)", T, r"^export const createTRPCContext"),
                role("Client", "route default export", "src/pages/api/trpc/[trpc].ts", r"^export default createNextApiHandler")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH02": "Adapter unchanged; createTRPCContext reads req.headers through the adapted Next.js request to resolve the region."},
         evidence="Route file and adapter version unchanged in all snapshots."),
    dict(name="tRPC Client Link Chain", pattern="Chain of Responsibility", ptype="Behavioral (GoF); tRPC client links",
         roles=[role("Chain runner", "createChain", dep="dependency @trpc/client@10.28.0 dist/splitLink-aebd28df.js:4-23"),
                role("ConcreteHandler", "loggerLink", "src/lib/api/client.ts", r"^    loggerLink"),
                role("ConcreteHandler", "httpBatchLink (terminal)", "src/lib/api/client.ts", r"^    httpBatchLink"),
                role("Chain assembly", "links: [...]", "src/lib/api/client.ts", r"^  links: \[")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={},
         evidence="lib/api/client.ts unchanged by CH01-CH03."),
    dict(name="tRPC Procedure Builder", pattern="Builder", ptype="Creational (GoF); fluent immutable builder (tRPC)",
         roles=[role("Builder", "ProcedureBuilder (createBuilder)", dep="dependency @trpc/server@10.28.0 dist/index.js:326-438"),
                role("Builder factory", "t = initTRPC.context().create()", T, r"^const t = initTRPC"),
                role("ConcreteBuilder (base)", "publicProcedure", T, r"^export const publicProcedure"),
                role("ConcreteBuilder (pre-configured)", "protectedProcedure", T, r"^export const protectedProcedure"),
                role("ConcreteBuilder (pre-configured)", "subscribedProcedure = protectedProcedure.use(attachSubscription)", T, r"^export const subscribedProcedure", since="CH01"),
                role("Director / Client", "catalogue.checkAccess = subscribedProcedure.input(showAccessInput).query(...)", CA, r"^  checkAccess: subscribedProcedure", since="CH01")],
         status={"CH01": "extended", "CH02": "preserved", "CH03": "preserved"},
         change={"CH01": "New pre-configured builder subscribedProcedure derived from protectedProcedure; because builders are immutable, protectedProcedure is unaffected and the new procedures (catalogue.checkAccess, profile.create) start from the richer builder.",
                 "CH03": "Unchanged; showAccessInput schema gains adult/genre_ids/profileId, still passed to .input()."},
         evidence="createNewBuilder copies _def, so adding .use(attachSubscription) does not change protectedProcedure; ch01 tests 'still rejects anonymous callers first' and characterization tests for protected procedures pass in CH01-CH03."),
    dict(name="tRPC Request Context", pattern="Context Object", ptype="Architectural (Core J2EE); tRPC request context / dependency injection",
         roles=[role("ContextFactory", "createTRPCContext", T, r"^export const createTRPCContext"),
                role("Context builder", "createInnerTRPCContext", T, r"^const createInnerTRPCContext"),
                role("ContextObject type", "CreateContextOptions", T, r"^type CreateContextOptions"),
                role("Context refiner", "enforceUserIsAuthed", T, r"^const enforceUserIsAuthed"),
                role("Context refiner", "attachSubscription adds subscription, planTier, maxProfiles", T, r"^const attachSubscription", since="CH01"),
                role("Consumer", "catalogue.checkAccess reads ctx.planTier, ctx.region", CA, r"^  checkAccess: subscribedProcedure", since="CH01")],
         status={"CH01": "extended", "CH02": "extended", "CH03": "preserved"},
         change={"CH01": "Context refined with plan entitlements (subscription, planTier, maxProfiles) by the new middleware; resolvers read them from ctx instead of querying the plan themselves.",
                 "CH02": "Context object gains region: createTRPCContext resolves it from geo headers (regionFromHeaders) and createInnerTRPCContext normalises it, so tests can inject a region without HTTP.",
                 "CH03": "Unchanged; catalogue.checkAccess still receives everything through ctx."},
         evidence="ch02-region tests build the context with createInnerTRPCContext-style fixtures carrying region; ch01 tests read ctx.maxProfiles via profile.create."),
    dict(name="Wire Serialization Transformer", pattern="Strategy", ptype="Behavioral (GoF); tRPC data transformer",
         roles=[role("Strategy", "DataTransformer", dep="dependency @trpc/server@10.28.0 dist/config-f3ce0144.js:11-21"),
                role("ConcreteStrategy", "superjson", dep="dependency superjson@1.12.3"),
                role("Context (server)", "initTRPC...create({transformer: superjson})", T, r"^const t = initTRPC"),
                role("Context (client)", "createTRPCNextBeta({transformer: superjson})", "src/lib/api/client.ts", r"^export const api")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={},
         evidence="Transformer configuration unchanged in all snapshots."),
    dict(name="Search Input DOM Event Listeners", pattern="Observer", ptype="Behavioral (GoF); DOM EventTarget listeners",
         roles=[role("ConcreteObserver", "useOnClickOutside listener", "src/hooks/use-on-click-outside.ts", r"^    const listener"),
                role("ConcreteObserver", "DebouncedInput handleKeyDown", "src/components/debounced-input.tsx", r"^    const handleKeyDown"),
                role("Client", "DebouncedInput", "src/components/debounced-input.tsx", r"^export function DebouncedInput")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={},
         evidence="Files unchanged by CH01-CH03."),
    dict(name="Shows Segment Error Boundary", pattern="Error Boundary", ptype="Framework idiom (React/Next.js App Router)",
         roles=[role("Boundary", "ErrorBoundaryHandler", dep="dependency next@13.4.4 dist/client/components/error-boundary.js:53-110"),
                role("Fallback", "(shows)/error.tsx Error", "src/app/(shows)/error.tsx", r"^const Error"),
                role("Fallback view", "ErrorScreen", "src/components/screens/error-screen.tsx", r"^const ErrorScreen"),
                role("Error source", "getShows/getNewAndPopularShows throw 'Failed to fetch shows'", F, r"^export async function getShows", until="CH02"),
                role("Error source", "fetchRows throws errorMessage when any response is not ok", F, r"^async function fetchRows", since="CH02")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH02": "Boundary unchanged; the error now originates in the shared fetchRows helper (same message, pinned by characterization tests)."},
         evidence="error.tsx and ErrorScreen unchanged; characterization test 'throws Failed to fetch shows when one row fails' passes in CH02/CH03."),
    dict(name="Root Global Error Boundary", pattern="Error Boundary", ptype="Framework idiom (React/Next.js App Router)",
         roles=[role("Boundary", "ErrorBoundaryHandler", dep="dependency next@13.4.4 dist/client/components/error-boundary.js:53-110"),
                role("Fallback", "GlobalError", "src/app/global-error.tsx", r"^const GlobalError"),
                role("Protected subtree", "RootLayout", "src/app/layout.tsx", r"^export default function RootLayout")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={},
         evidence="Files unchanged by CH01-CH03."),
    dict(name="Shows Loading Placeholder", pattern="Suspense Boundary", ptype="Framework idiom (React Suspense / Next.js loading.tsx)",
         roles=[role("Boundary", "LoadingBoundary", dep="dependency next@13.4.4 dist/client/components/layout-router.js:335-345"),
                role("Fallback (placeholder)", "ShowsLoading", "src/app/(shows)/loading.tsx", r"^export default function ShowsLoading"),
                role("Suspending child", "Home (async server page)", "src/app/(shows)/page.tsx", r"^export default async function Home")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH02": "Unchanged boundary; Home now awaits getServerRegion() and getShows() before toCategories, so it still suspends."},
         evidence="loading.tsx unchanged; pages remain async server components."),
    dict(name="TMDB Row Scatter-Gather", pattern="Scatter-Gather", ptype="Concurrency / Enterprise Integration (Hohpe & Woolf)",
         roles=[role("Scatter / Gather", "getShows (8 parallel fetches, all-or-nothing, aggregate)", F, r"^export async function getShows", until="CH02"),
                role("Scatter / Gather", "getNewAndPopularShows (4 parallel fetches)", F, r"^export async function getNewAndPopularShows", until="CH02"),
                role("Scatter / Gather (generic)", "fetchRows(rows, errorMessage): Promise.all(fetch) -> some(!ok) -> Promise.all(json) -> Object.fromEntries", F, r"^async function fetchRows", since="CH02"),
                role("Row specification", "SHOW_ROWS / NEW_AND_POPULAR_ROWS", F, r"^const SHOW_ROWS", since="CH02"),
                role("Client", "getShows / getNewAndPopularShows (thin callers)", F, r"^export async function getShows", since="CH02")],
         status={"CH01": "preserved", "CH02": "modified", "CH03": "preserved"},
         change={"CH01": "Unchanged fan-out; the gathered originals row is additionally marked isPremium.",
                 "CH02": "Refactored (Duplicate Code -> Extract Function + table-driven rows): the two hand-written scatter/gather blocks were replaced by one generic fetchRows aggregator; request URLs, order, keys and error message preserved.",
                 "CH03": "Unchanged."},
         evidence="tests/characterization.test.ts pins the 8 URLs, their order and the error; passes on baseline (characterization log) and on CH02/CH03."),
    dict(name="Profile and Account Query Cache", pattern="Read-Through Cache", ptype="Architecture (caching); React Query",
         roles=[role("Cache policy", "QueryClient defaults (staleTime/cacheTime Infinity)", "src/lib/api/client.ts", r"^export const api"),
                role("Loader", "profileRouter.getAll", P, r"^  getAll: protectedProcedure"),
                role("Reader", "ProfilesScreen profilesQuery", "src/components/screens/profiles-screen.tsx", r"const profilesQuery"),
                role("Invalidator", "AddProfileForm onSuccess", "src/components/forms/add-profile-form.tsx", r"const createProfileMutation"),
                role("Invalidator", "EditProfileForm effect", "src/components/forms/edit-profile-form.tsx", r"^  React.useEffect\(\(\) => \{"),
                role("Invalidator", "ResetPinForm onSuccess", "src/components/forms/reset-pin-form.tsx", r"const updatePinMutation")],
         status={"CH01": "preserved", "CH02": "preserved", "CH03": "preserved"},
         change={"CH03": "Unchanged invalidation; EditProfileForm also submits maturityLevel, and the profile.getAll key is invalidated as before so the new rating is re-read."},
         evidence="Readers/invalidators unchanged apart from the CH03 form field."),
]

CONCRETE_ROLES = {"ConcreteHandler", "Singleton", "ConcreteObserver", "ConcreteComponent", "ConcreteDecorator",
                  "Adapter", "ConcreteStrategy", "Facade", "Composite", "Composite (root)", "Proxy", "Cache", "ConcreteClass",
                  # second-pass pattern types
                  "FrontController", "ConcreteBuilder (base)", "ConcreteBuilder (pre-configured)", "ContextFactory",
                  "Fallback", "Fallback (placeholder)", "Scatter / Gather", "Scatter / Gather (generic)",
                  "Cache policy"}


def active(r, v):
    return ORDER[r["since"]] <= ORDER[v] and (r["until"] is None or ORDER[v] < ORDER[r["until"]])


def main():
    out_rows, counts = [], {}
    base = list(csv.DictReader(open("Part1/patterns.csv", encoding="utf-8")))
    for b in base:
        out_rows.append({**b, "status_after_change": "baseline", "change_description": "Original application code at 676e5dd."})
    counts["baseline"] = {"types": len({b["pattern_name"] for b in base}), "instances": len(base)}
    problems = 0
    for v, commit, root, prefix in VERSIONS:
        types, inst, conc = set(), 0, 0
        for ins in INSTANCES:
            if ins["status"].get(v) is None:
                continue
            roles = [r for r in ins["roles"] if active(r, v)]
            locs, names = [], []
            for r in roles:
                if r["dep"]:
                    loc = r["dep"]
                else:
                    try:
                        loc = f"{prefix}{r['file']}:{span(root, r['file'], r['anchor'], r['through'])}"
                    except LookupError as e:
                        problems += 1
                        loc = f"NOT FOUND ({e})"
                locs.append(f"{r['sym']}: {loc}")
                names.append(f"{r['role']}={r['sym']}")
                if r["role"] in CONCRETE_ROLES:
                    conc += 1
            types.add(ins["pattern"]); inst += 1
            out_rows.append({
                "source_version": f"{v}@{commit}", "pattern_name": ins["pattern"], "pattern_type": ins["ptype"],
                "instance_name": ins["name"], "participant_roles": "; ".join(names), "source_locations": "; ".join(locs),
                "intent_and_evidence": ins["evidence"], "status_after_change": ins["status"][v],
                "change_description": ins["change"].get(v, "Unchanged by this change; locations re-measured."),
            })
        counts[v] = {"types": len(types), "instances": inst, "concrete": conc,
                     "per": {p: sum(1 for i in INSTANCES if i["pattern"] == p and i["status"].get(v)) for p in sorted(types)}}
    cols = ["source_version", "pattern_name", "pattern_type", "instance_name", "participant_roles", "source_locations",
            "intent_and_evidence", "status_after_change", "change_description"]
    with open("Part2/pattern_evalution.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader(); w.writerows(out_rows)
    # pattern_counts.csv: keep baseline rows, append one block per snapshot
    base_counts = [r for r in csv.reader(open("Part1/Pattern_count.csv", encoding="utf-8"))][1:]
    base_counts = [r for r in base_counts if r[0].startswith("original")]
    with open("Part2/Pattern_count.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source_version", "summary", "pattern_name", "count"])
        w.writerows(base_counts)
        for v, commit, _, _ in VERSIONS:
            sv = f"{v}@{commit}"
            for p, n in counts[v]["per"].items():
                w.writerow([sv, "per_pattern", p, n])
            w.writerow([sv, "total_pattern_types", "", counts[v]["types"]])
            w.writerow([sv, "total_pattern_instances", "", counts[v]["instances"]])
    conc_base = sum(1 for ins in INSTANCES if ins["status"].get("CH01") != "newly_introduced"
                    for r in ins["roles"] if active(r, "baseline") and r["role"] in CONCRETE_ROLES)
    counts["baseline"]["concrete"] = conc_base
    for v in ["baseline"] + [x[0] for x in VERSIONS]:
        print(v, counts[v])
    print("rows", len(out_rows), "location problems", problems)


if __name__ == "__main__":
    main()
