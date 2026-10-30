"""Generates A12_Report.tex from the team's data files and evidence.
Run from A12/:  python data/test_result/tools/build_report.py && pdflatex A12_Report.tex (twice)"""
import csv
import importlib.util
import statistics
from collections import Counter, defaultdict

spec = importlib.util.spec_from_file_location("p1", "data/test_result/part1/part1_patterns.py")
p1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p1)


def esc(s):
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
           "<": r"\textless{}", ">": r"\textgreater{}", "|": r"\textbar{}"}
    return "".join(rep.get(c, c) for c in str(s))


def path(p):
    return r"\path{" + p.replace("{", "").replace("}", "") + "}"


def loc_tex(loc):
    if loc.startswith("dependency"):
        return esc(loc)
    return "; ".join(path(x.strip()) for x in loc.split(";"))


SNAP = list(csv.DictReader(open("data/test_result/part2/metrics.csv")))
HOT = list(csv.DictReader(open("data/test_result/part2/hotspot_metrics.csv")))
EVO = list(csv.DictReader(open("Part2/pattern_evalution.csv", encoding="utf-8")))
XL = list(csv.DictReader(open("Part3/llm/pattern_crosslanguage.csv", encoding="utf-8")))
COUNTS = list(csv.DictReader(open("Part2/Pattern_count.csv", encoding="utf-8")))

out = []
w = out.append

w(r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage[T1]{fontenc}
\IfFileExists{lmodern.sty}{\usepackage{lmodern}}{}
\usepackage{tabularx,booktabs,xcolor,graphicx,longtable,float,array,enumitem}
\usepackage[hyphens]{xurl}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue!50!black,urlcolor=blue!50!black}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\newcommand{\entry}[2]{\textbf{#1:} #2\par}
\newcommand{\todo}[1]{\textcolor{red}{\textbf{[TEAM TO FILL: #1]}}}
\renewcommand{\arraystretch}{1.15}
\setlength{\emergencystretch}{3em}\sloppy
\setlist{nosep,leftmargin=1.5em}
\begin{document}
\begin{center}\Large\textbf{23CSE455 Design Patterns}\\[4pt]\LARGE Case Study Report\end{center}

\entry{Team}{A12}
\entry{Case study}{OTT / video streaming application using React / Next.js --- \emph{Design Pattern Analysis in a Next.js-Based Video Streaming Application}}
\entry{Application}{netflx-web (Netflix clone, Next.js 13 app router, tRPC, NextAuth, Prisma, Stripe) by sadmann7. Faculty approval: approved by the course faculty for use in this case study.}
\entry{Date}{2026-10-30 (first analysis 2026-10-10, exhaustive second pass 2026-10-29/30)}
\textbf{Submission repository:} \href{https://github.com/aswathymohan-amrita/23CSE455_DP_CaseStudy}{23CSE455\_DP\_CaseStudy}, folder \texttt{A12/}\par
\textbf{Students}\par
\begin{tabularx}{\linewidth}{@{}llX@{}}\toprule
Roll number & Student name & Batch\\\midrule
AM.SC.U4CSE23161 & Swaminathan A & CSE B\\
AM.SC.U4CSE23207 & Anna Ouseph & CSE C\\
AM.SC.U4CSE23230 & Leya Paul & CSE C\\
AM.SC.U4CSE23242 & Pooja Sathyan & CSE C\\
AM.SC.U4CSE23069 & Rahul Rajan & CSE A\\\bottomrule
\end{tabularx}
""")

# ---------------------------------------------------------------- section 1
w(r"""
\section{Application and architecture}
\entry{Original source}{\url{https://github.com/sadmann7/netflx-web}, branch \texttt{main}, no release tags; baseline commit \texttt{676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258} (2024-06-12, ``Merge pull request \#11''); accessed 2026-10-10. \textbf{Licence: none} --- the repository has no LICENSE file, so all rights are reserved by the author; the code is used only for this academic analysis. Snapshot: \path{data/code/}.}
\entry{Environment}{TypeScript 5.0.4 on Node.js; Next.js 13.4.4 (app router + pages router for API routes), React 18.2.0, tRPC 10.28.0, NextAuth 4.22.1 with @next-auth/prisma-adapter 1.0.6 (Google OAuth), Prisma 4.14.1 on MySQL (\texttt{relationMode = "prisma"}), Stripe 12.7.0, Zustand 4.3.8, @tanstack/react-query 4.29.7, Tailwind CSS 3.3.2; catalogue data from the TMDB REST API. Analysis tools (2026-10-10, Linux sandbox): Node.js 22.22.0, yarn 1.22.22, vitest 1.6.0, lizard 1.24.1, PlantUML + Graphviz. Second pass and Part 3 re-run (2026-10-29/30, Windows 11 x64): Temurin JDK 21.0.12, Python 3.12.10, Node.js 26.13.0, g++ 16.2.0 (WinLibs UCRT), lizard 1.24.3, PlantUML 1.2024.7 (built-in smetana layout); dependency sources inspected with \texttt{npm pack} at the versions of \path{yarn.lock}.}
\entry{Scope}{Inspected: \path{src/server/**}, \path{src/lib/**}, \path{src/config/**}, \path{src/stores/**}, \path{src/app/**}, \path{src/components/**}, \path{src/@trpc/next-layout/**}, \path{src/pages/**}, \path{src/hooks/**}, \path{src/context/**}, \path{src/env.mjs}, \path{prisma/schema.prisma} --- in the second pass every one of these files was read completely --- and dependency code where a role is implemented (next-auth, prisma-adapter, zustand, tRPC server/client/react-query/next, react-query, next). Excluded: \path{components/ui/*} (generated shadcn UI primitives), \path{styles/}, \path{public/}, \path{app/(docs)} (static help/terms text) and \path{app/api/og} (Open Graph image) --- none of them belongs to the seven case-study areas. The area-to-file map is in \path{data/test_result/part1/candidates.md}.}
""")
w(r"""\entry{Architecture}{Figure~\ref{fig:arch} (source \path{Part1/pattern_architecture/00_architecture.puml}).}
\begin{figure}[H]\centering\includegraphics[width=\linewidth]{Part1/pattern_architecture/00_architecture.png}
\caption{Component view of netflx-web at the baseline.}\label{fig:arch}\end{figure}
\textbf{Components.} \emph{Browser}: React client components (shows carousels, modal, profile screens, forms) keep UI state in three Zustand stores (modal, profile, search) and call the server through two tRPC client proxies backed by one React-Query cache. \emph{Server}: App-router server components render pages and fetch catalogue rows from TMDB through \path{lib/fetchers.ts}; the tRPC API (\path{/api/trpc}, pages router) serves user, profile, icon and My-List procedures behind an authentication middleware; NextAuth (\path{/api/auth}) signs users in with Google and stores users/sessions through the Prisma adapter; Stripe checkout (\path{/api/users/stripe}) and a Stripe webhook (\path{/api/webhooks/stripe}) maintain the subscription fields on the User row. Every server module reads configuration through the \texttt{env} proxy. Two \emph{front controllers} receive all API traffic: \path{/api/trpc/[trpc]} (all 19 procedures, adapted to Next.js by \texttt{createNextApiHandler}) and \path{/api/auth/[...nextauth]} (all auth actions). Route segments are wrapped by Next.js error boundaries (\path{error.tsx}, \path{global-error.tsx}) and a Suspense loading boundary (\path{(shows)/loading.tsx}).

\textbf{Request flow (adding a title to My List).} A viewer clicks a poster $\rightarrow$ \texttt{ShowCard} publishes \texttt{\{show, open\}} to \texttt{useModalStore} $\rightarrow$ \texttt{ShowsContainer} renders \texttt{ShowModal}, which fetches the trailer from TMDB $\rightarrow$ ``Add to My List'' calls \texttt{api.myList.create.useMutation} on the tRPC proxy $\rightarrow$ HTTP batch to \path{/api/trpc} $\rightarrow$ \texttt{createTRPCContext} loads the session $\rightarrow$ \texttt{enforceUserIsAuthed} passes the request on $\rightarrow$ the resolver loads the profile with its list through the Prisma singleton and inserts a \texttt{MyShow} row $\rightarrow$ the modal invalidates the cached \texttt{myList.getAll} query, so the next read reloads it.
""")
w(r"""\entry{Run instructions}{\path{README.md} (team) and \path{data/code/README.md} (original). Setup: copy \path{.env.example} to \path{.env} (MySQL URL, Google OAuth, TMDB key, Stripe keys), \texttt{yarn install} (runs \texttt{prisma generate}), \texttt{npx prisma db push}, \texttt{yarn dev}, \texttt{yarn stripe:listen}. \textbf{Actual result in the analysis environment:} \texttt{npx tsc --noEmit} passes on the baseline (\path{data/test_result/baseline/typecheck.log}); \texttt{next build} stops at \texttt{next/font} because the sandbox cannot download Inter from Google Fonts (\path{data/test_result/baseline/build.log}) --- an environment limit, not a code error; the baseline repository contains no tests. Prisma engines could not be downloaded either, so the database was replaced by an in-memory fake in all tests.}
""")

# ---------------------------------------------------------------- section 2
types = Counter(r["pattern"] for r in p1.PATTERNS)
w(r"""
\section{Part 1 Pattern discovery}
\entry{Method}{\textbf{First pass (2026-10-10).} (1) Listed the entry files of each of the seven areas and read them completely. (2) Followed every import/call one hop, including into \path{node_modules} when a role is played by a dependency (versions pinned by \path{yarn.lock}). (3) For each candidate, recorded intent, the role relationships and the delegation that happens at run time; a candidate was confirmed only when all three are visible in code, never from a name, comment or LLM statement alone. (4) Line ranges were checked by script: \path{data/test_result/part1/verify_locations.py} (all cited ranges exist and start at the named symbol) and an independent bracket-matching locator (\path{data/test_result/part2/locate.py}) for end lines, which found and fixed two wrong end lines. (5) Rejected and uncertain candidates were recorded with reasons. The first pass was done with an LLM (section 5) and every claim was then checked against the source; it found 10 types / 15 instances. \textbf{Second, exhaustive pass (2026-10-29/30).} (6) Every in-scope file was read top to bottom, not only the area entry files, and checked against the GoF catalogue, architectural (PoEAA, Core J2EE), concurrency/integration and React/Next.js idioms. (7) Dependency roles were verified in the exact package versions of \path{yarn.lock} (\texttt{npm pack} of @trpc/server, client, react-query, next 10.28.0, next-auth 4.22.1, next 13.4.4) with file:line references. (8) The location check was re-run over all \textbf{156} cited ranges: 0 problems (\path{data/test_result/part1/location_check.log}). The second pass added 6 types and 13 instances and corrected one role of an existing record (Transport of the Pages-Router tRPC Client Proxy, see its record).}
\subsection{Totals at the baseline}
""")
w(r"\entry{Confirmed pattern types}{" + esc(", ".join(types)) + f" --- \\textbf{{{len(types)}}}" + "}\n")
w(r"\entry{Confirmed pattern instances}{\textbf{" + str(len(p1.PATTERNS)) + r"} independent collaborations (table below).}" + "\n")
w(r"\entry{Concrete participant classes}{\textbf{" + str(sum(r["concrete"] for r in p1.PATTERNS)) + r"} implementations of variable roles (ConcreteHandler, ConcreteObserver, ConcreteStrategy, ConcreteComponent/Decorator, Adapter, Singleton, Facade module, Composite routers, Proxy, Cache, FrontController, ConcreteBuilder, ContextFactory, boundary fallbacks, scatter/gather functions). Many are React function components or modules, not classes; we do not invent classes for them.}" + "\n")
w(r"\entry{Unique participant symbols}{\textbf{" + str(len(p1.IN_REPO_SYMBOLS)) + r"} distinct mapped symbols in the repository (e.g.\ \texttt{ShowsContainer}, \texttt{prisma}, \texttt{AppRouter} counted once although they take part in several instances) plus \textbf{" + str(len(p1.DEP_SYMBOLS)) + r"} dependency symbols (e.g.\ \texttt{PrismaAdapter}, zustand \texttt{persist}); list in \path{data/test_result/part1/part1_patterns.py}.}" + "\n")
w(r"\entry{Rejected and uncertain candidates}{\textbf{11 rejected}, \textbf{5 uncertain} (table at the end of this section, full list with locations in \path{data/test_result/part1/candidates.md}). Observation scope: static reading of the baseline source and of the pinned dependency sources, plus type checking; no run with real Stripe, TMDB or Google credentials.}" + "\n")

w(r"""\subsection{Pattern inventory}
\begin{longtable}{@{}p{3.3cm}p{8.3cm}cc@{}}\toprule
Pattern type & Instance names & Instances & Concrete\\\midrule\endhead
""")
grouped = defaultdict(list)
for r in p1.PATTERNS:
    grouped[r["pattern"]].append(r)
for pat, recs in grouped.items():
    w(f"{esc(pat)} & {esc('; '.join(r['instance'] for r in recs))} & {len(recs)} & {sum(r['concrete'] for r in recs)}\\\\\n")
w(r"\midrule Total & & " + str(len(p1.PATTERNS)) + " & " + str(sum(r["concrete"] for r in p1.PATTERNS)) + r"\\\bottomrule\end{longtable}" + "\n")
w(r"""\textbf{Mapping to the seven areas.} User management: Active Profile Selection, Persisted Profile Store, API Router Tree, Profile and Account Query Cache. Video catalogue: TMDB Catalogue Facade, TMDB Row Scatter-Gather, Show Modal Selection, Search Results Broadcast, Search Input DOM Event Listeners, Shows Loading Placeholder, Shows Segment Error Boundary. Subscription: Stripe API Client (plans resolved in \path{lib/subscription.ts}). Authentication: Authenticated Procedure Pipeline, Sign-in Provider Strategy, NextAuth Prisma Persistence Adapter, NextAuth Auth Route Front Controller, Shared Prisma Database Client. Content access: Authenticated Procedure Pipeline and tRPC Request Context (server), Environment Secret Guard (configuration secrets); the profile PIN gate is only an uncertain candidate. Caching: My List Query Cache, Profile and Account Query Cache, (rejected) server caching proxy. Cross-cutting infrastructure used by all areas: tRPC API Front Controller, tRPC Next.js API Handler Adapter, tRPC Procedure Builder, tRPC Client Link Chain, Wire Serialization Transformer, Root Global Error Boundary. Recommendation: \textbf{no pattern} --- the home page shows fixed TMDB lists (trending, top rated, five genre ids); no user signal is used.
""")

w(r"\subsection{One record for each pattern instance}" + "\n")
DIAG = ["01_cor_authenticated_procedure_pipeline", "02_singleton_shared_prisma_client", "03_singleton_stripe_client",
        "04_observer_show_modal_selection", "05_observer_active_profile_selection", "06_observer_search_results_broadcast",
        "07_decorator_persisted_profile_store", "08_adapter_nextauth_prisma", "09_strategy_signin_provider",
        "10_facade_tmdb_catalogue", "11_composite_api_router_tree", "12_proxy_pages_router_trpc_client",
        "13_proxy_app_router_trpc_client", "15_proxy_environment_secret_guard", "14_cache_my_list_query_cache"]
VERIF = {
    "Authenticated Procedure Pipeline": "Confirmed. Characterization tests: anonymous caller -> UNAUTHORIZED, signed-in caller reaches the resolver with its id, public procedure stays open (\\path{tests/characterization.test.ts}). Alternative considered: Decorator (procedure.use wraps) --- rejected because each middleware decides whether to pass the request on, which is the defining CoR property.",
    "Shared Prisma Database Client": "Confirmed by reading; behaviour reproduced in Part 3 problem 02 (9/9 cases incl. hot reload). Alternative: plain module export --- the explicit globalThis guard makes it a deliberate singleton.",
    "Stripe API Client": "Confirmed as module-level singleton; weaker form (no guard, relies on the ES module cache).",
    "Show Modal Selection": "Confirmed by reading the store and its subscribers; publisher and observers never reference each other.",
    "Active Profile Selection": "Confirmed; six subscribing components, three publishers.",
    "Search Results Broadcast": "Confirmed; the search box does not know which views react.",
    "Persisted Profile Store": "Confirmed; same StateCreator interface in and out; other stores use the undecorated creator.",
    "NextAuth Prisma Persistence Adapter": "Confirmed by reading the adapter source in node\\_modules (createUser -> p.user.create, getUserByEmail -> p.user.findUnique).",
    "Sign-in Provider Strategy": "Confirmed with the caveat of a single configured strategy (latent variability).",
    "TMDB Catalogue Facade": "Confirmed; facade behaviour pinned by characterization tests (URLs, order, keys, errors).",
    "API Router Tree": "Confirmed; uniform dotted-path access to routers and procedures; 19 leaves.",
    "Pages-Router tRPC Client Proxy": "Confirmed; JS Proxy objects in @trpc/server dist (index-4a823936.js:55,87). \\textbf{Corrected in the second pass:} its own links (api.ts:36-45) are never executed because createTRPCNext evaluates config() only inside withTRPC (@trpc/next@10.28.0 dist/index.js:171-188), which the app never mounts; its hooks use the client supplied through the shared TRPCContext by TRPCProvider (client.ts).",
    "App-Router tRPC Client Proxy": "Confirmed; separate instance because it is a different proxy object built by vendored code; the duplication of two clients is noted as a smell.",
    "Environment Secret Guard": "Confirmed (found in the second pass); same mechanism reproduced in Part 3 problem 09.",
    "My List Query Cache": "Confirmed; cache behaviour reproduced in Part 3 problem 10. The two client proxies share one React-Query context (verified in @trpc/react-query createHooksInternal:92,193 in the second pass).",
    "tRPC API Front Controller": "Confirmed in the dependency source (adapters/next.js:16-56, resolveHTTPResponse.js:90). Reproduced in Part 3 problem 11 (14/14 cases incl. batching with one shared context). Alternative considered: Mediator --- rejected, procedures do not interact through the controller.",
    "NextAuth Auth Route Front Controller": "Confirmed in next-auth core/index.js:159-206 (switch on action). The app-router copy \\_route.ts is inactive (underscore prefix).",
    "tRPC Next.js API Handler Adapter": "Confirmed; separate collaboration from the Front Controller on the same line (interface conversion vs. central dispatch).",
    "tRPC Client Link Chain": "Confirmed for lib/api/client.ts; the identical chain in lib/api/api.ts is recorded as uncertain because it is never executed.",
    "tRPC Procedure Builder": "Confirmed in @trpc/server index.js:326-438 (createNewBuilder copies \\_def). Immutability reproduced in Part 3 problem 12 (case b11).",
    "tRPC Request Context": "Confirmed; the previously rejected Factory Method candidate on the same functions was reclassified as the ContextFactory role of this Context Object. Reproduced in Part 3 problem 13.",
    "Wire Serialization Transformer": "Confirmed with the caveat of one selected concrete strategy plus the framework default (identity).",
    "Search Input DOM Event Listeners": "Confirmed; subject is the browser EventTarget, listeners are unregistered in effect clean-ups.",
    "Shows Segment Error Boundary": "Confirmed in next@13.4.4 error-boundary.js:53-110; reproduced in Part 3 problem 14. Not observed at run time (no TMDB key in the analysis environment).",
    "Root Global Error Boundary": "Confirmed as a separate boundary (different tree position and fallback).",
    "Shows Loading Placeholder": "Confirmed in next@13.4.4 layout-router.js:335-345; the explicit Suspense wrappers around client forms were rejected because their children never suspend. Reproduced in Part 3 problem 15.",
    "TMDB Row Scatter-Gather": "Confirmed; separate from the Facade (fan-out and aggregation vs. hiding endpoints). Reproduced in Part 3 problem 16; modified by the CH02 refactoring.",
    "Profile and Account Query Cache": "Confirmed; independent of the My List cache except for the shared QueryClient.",
}
DIAG = dict(zip([r["instance"] for r in p1.PATTERNS[:15]], DIAG))
DIAG.update({
    "tRPC API Front Controller": "16_front_controller_trpc_api",
    "NextAuth Auth Route Front Controller": "17_front_controller_nextauth",
    "tRPC Next.js API Handler Adapter": "18_adapter_trpc_next_handler",
    "tRPC Client Link Chain": "19_cor_trpc_client_link_chain",
    "tRPC Procedure Builder": "20_builder_trpc_procedure_builder",
    "tRPC Request Context": "21_context_object_trpc_request",
    "Wire Serialization Transformer": "22_strategy_wire_serialization",
    "Search Input DOM Event Listeners": "23_observer_search_input_dom_events",
    "Shows Segment Error Boundary": "24_error_boundary_shows_segment",
    "Root Global Error Boundary": "25_error_boundary_root_global",
    "Shows Loading Placeholder": "26_suspense_shows_loading_placeholder",
    "TMDB Row Scatter-Gather": "27_scatter_gather_tmdb_rows",
    "Profile and Account Query Cache": "28_cache_profile_account_query",
})
for rec in p1.PATTERNS:
    dg = DIAG[rec["instance"]]
    w(r"\subsubsection*{" + esc(rec["instance"]) + "}\n")
    w(r"\entry{Pattern type and category}{" + esc(rec["pattern"]) + " --- " + esc(rec["ptype"]) + "}\n")
    w(r"\entry{Purpose and origin}{" + esc(rec["evidence"].split(". ")[0]) + ". Origin: " + esc(rec["origin"]) + ".}\n")
    w(r"\textbf{Participant mapping}\par" + "\n" + r"\begin{tabularx}{\linewidth}{@{}p{3.4cm}X>{\raggedright\arraybackslash}p{6.0cm}@{}}\toprule Pattern role & Actual class, interface and function & File and line range\\\midrule" + "\n")
    for role, sym, loc in rec["roles"]:
        w(f"{esc(role)} & {esc(sym)} & {loc_tex(loc)}\\\\\n")
    w(r"\bottomrule\end{tabularx}" + "\n")
    w(r"\entry{Evidence}{" + esc(rec["evidence"]) + "}\n")
    w(r"\entry{Diagram}{\path{Part1/pattern_architecture/" + dg + r".puml} (editable), \path{Part1/pattern_architecture/" + dg + ".png}}\n")
    if dg.startswith(("01_", "07_", "08_", "10_", "15_", "16_", "20_", "21_", "27_")):
        wid = "\\linewidth" if dg.startswith(("10_", "16_")) else "0.62\\linewidth"
        w(r"\begin{figure}[H]\centering\includegraphics[width=" + wid + r"]{Part1/pattern_architecture/" + dg + r".png}\caption{" + esc(rec["instance"]) + r"}\end{figure}" + "\n")
    w(r"\entry{Verification}{" + VERIF[rec["instance"]] + r" Reviewer: AM.SC.U4CSE23161 Swaminathan A and AM.SC.U4CSE23242 Pooja Sathyan (Part 1).}" + "\n")

w(r"""\subsection*{Rejected and uncertain candidates}
\begin{longtable}{@{}p{4.2cm}p{1.6cm}p{9.8cm}@{}}\toprule Candidate & Decision & Reason\\\midrule\endhead
Caching Proxy for server components (\texttt{createTRPCNextLayout}) & rejected & Proxy + QueryClient structure exists (\path{src/@trpc/next-layout/server/createTrpcNextLayout.tsx:89-168}) but nothing imports it: dead code.\\
Factory Method (\texttt{createTRPCContext}) & rejected & No creator hierarchy or overridable creation step; the same functions are the ContextFactory of the confirmed \emph{tRPC Request Context} (Context Object).\\
Explicit Suspense boundaries & rejected & \path{account/users/[userId]/page.tsx:50-64}, \path{help-center/page.tsx:23-73} wrap client components that never suspend, so the fallback can never be shown.\\
Container / Presentational & rejected & \texttt{ShowsCarousel}/\texttt{ShowsGrid} read and write the modal store themselves, so the split is not maintained.\\
Mediator (Zustand stores) & rejected & Stores hold state and setters only, no coordination logic; already recorded as Observer subjects.\\
Command (\texttt{useMutation}) & rejected & Framework hook; no app-level command interface, queue, undo or logging.\\
Registry (\texttt{Icons}, \texttt{siteConfig}) & rejected & Static constant objects without a registration/lookup protocol.\\
Repository & rejected & Routers call \texttt{ctx.prisma.<model>} directly; no repository abstraction.\\
Template Method (nested layouts) & rejected & Layouts compose children; no base algorithm with overridable steps.\\
Recommendation strategy/engine & rejected & Fixed TMDB queries only (\path{app/(shows)/page.tsx:13-42}); no recommendation logic exists.\\
Debounce & rejected & UI timing technique (\path{components/debounced-input.tsx:44-50}), not a design pattern.\\
Observer via Stripe webhook & uncertain & Only the subscriber side is in code; registration lives in the Stripe dashboard; dispatch is an if-chain on \texttt{event.type}.\\
Protection Proxy for the PIN gate & uncertain & \texttt{ProfilesScreen} conditionally renders children; no common interface. The PIN is sent to the browser and compared there (\path{forms/pin-form.tsx:19}), so it is not real access control.\\
Implicit Next.js data cache & uncertain & \texttt{fetch} in server components is cached by Next 13 by default, but the code sets no option and it was not observed at run time.\\
Facade over session/subscription helpers & uncertain & \path{lib/session.ts:4-11}, \path{lib/subscription.ts:6-53} are thin single-subsystem wrappers.\\
Second client link chain (\path{lib/api/api.ts:36-45}) & uncertain & Declared like the active chain in \path{client.ts} but never executed (\texttt{withTRPC} not mounted).\\\bottomrule
\end{longtable}
""")

# ---------------------------------------------------------------- section 3
snap = {r["snapshot"]: r for r in SNAP}
w(r"""
\section{Part 2 Evolution and refactoring}
All three changes were implemented on branch \texttt{a12-evolution}. Before any change, commit \texttt{d68c773} added vitest and \emph{characterization tests} that pin the baseline behaviour (no production code changed; 13/13 pass). Characterization tests added later for refactored code were first run on the untouched baseline (19/19, \path{data/test_result/part2/tests_baseline_characterization.log}). The four requirements of the case study are covered: \emph{premium content} and the \emph{new subscription plan} in CH01, \emph{regional restrictions} in CH02, \emph{parental control} in CH03. Patches: \path{data/test_result/part2/0001-*.patch} (test harness) and \path{Part2/changes/ChangeN/000*.patch}; evolved source: \path{Part2/code/}. The instances found in the Part 1 second pass were tracked through the same snapshots afterwards (rebuilt by applying the patches to the upstream commit; final tree identical to \path{Part2/code/}).
""")
CH = [
    ("CH01 --- Premium content and a new subscription plan (Ultra)", "d68c773", "3f79642", "Change1", "CH01",
     r"New plan \textbf{Ultra} (tier 5, 12.99/month, 4K+HDR, up to \textbf{7 profiles}). Titles of the originals row (TMDB network 213) are \textbf{premium} and playable only with Standard, Premium or Ultra (tier $\ge 3$); other viewers see the title with an ``Upgrade to watch'' button. Acceptance (all automated in \path{tests/ch01-premium-plan.test.ts}): five plans incl.\ Ultra; UI and server plan lists identical; premium title denied for tiers 0--2 and allowed for 3--5; Basic subscriber denied, Standard allowed, anonymous \texttt{UNAUTHORIZED}; Ultra may create a 6th/7th profile but not an 8th, Standard keeps 5; only the originals row tagged premium; all earlier tests pass.",
     r"New \path{config/plan-catalog.ts}; \path{config/plans.ts} and \path{config/subscriptions.ts} derived from it; \path{lib/access/*} (\texttt{AccessRule}, \texttt{PremiumContentRule}); \path{server/api/trpc.ts} (\texttt{attachSubscription}, \texttt{subscribedProcedure}); new \path{routers/catalogue.ts}; \path{routers/profile.ts} limit from \texttt{ctx.maxProfiles}; \path{lib/fetchers.ts} tags premium; \path{components/show-modal.tsx} upgrade button; checkout refuses a plan without Stripe price; env \texttt{STRIPE\_ULTRA\_PRICE\_ID}. Test fixture change disclosed: fake \texttt{user.findFirst} returns a plan-less user (a signed-in user always has a row); no assertion changed.",
     r"Authenticated Procedure Pipeline \textbf{extended} (new handler \texttt{attachSubscription}); API Router Tree \textbf{extended} (\texttt{catalogueRouter}); TMDB Catalogue Facade \textbf{modified} (premium tagging); tRPC API Front Controller \textbf{extended} (new command \texttt{catalogue.checkAccess}); tRPC Procedure Builder \textbf{extended} (\texttt{subscribedProcedure}; \texttt{protectedProcedure} unchanged thanks to immutable builders); tRPC Request Context \textbf{extended} (plan entitlements); \textbf{newly introduced}: Content Access Rule Chain (CoR) and Access Rule Evaluation Template (Template Method: \texttt{AccessRule.check} fixed, \texttt{evaluate} abstract); all others preserved.",
     r"\emph{Shotgun Surgery / duplicated data}: plans existed in \path{config/plans.ts} (UI) and \path{config/subscriptions.ts} (server) and had already drifted (Basic devices ``Phone, Tablet, Computer'' vs ``\ldots, TV''). Root cause: the server list reads secret price ids through the env Protection Proxy, which throws in the browser. Technique: extract a client-safe plan catalogue and derive both lists; \emph{Replace Magic Number} 5 with \texttt{plan.maxProfiles} (default 5). Behaviour preservation: subscription and profile-limit characterization tests unchanged and passing; a new test makes future drift fail."),
    ("CH02 --- Regional restrictions", "3f79642", "e420dcf", "Change2", "CH02",
     r"Titles are licensed per territory (\texttt{allowedRegions} or \texttt{blockedRegions}); region from the \texttt{x-vercel-ip-country} header, else \texttt{cf-ipcountry}, else US. Unlicensed titles must not appear in any row and must be refused on direct access; a region-blocked premium title is hidden, not upsold. Acceptance (\path{tests/ch02-region.test.ts}): region normalisation and header priority; tRPC context reads the header; Fight Club (550) hidden in CN, allowed in US; Game of Thrones (1399) allowed in IN, hidden in DE; blocked premium title gives \texttt{REGION\_BLOCKED}; locked titles stay visible, hidden ones are removed; row titles and order unchanged; \texttt{checkAccess} uses the request region.",
     r"\path{config/regions.ts}, \path{lib/region.ts}, \path{lib/server-region.ts}; \texttt{RegionRule} placed first in the chain, \texttt{visibleShows}; region in the tRPC context; \path{lib/catalogue.ts} + the four \path{(shows)} pages filter rows on the server.",
     r"Content Access Rule Chain \textbf{extended} (RegionRule linked at the front); Access Rule Evaluation Template \textbf{extended}; TMDB Catalogue Facade \textbf{modified} (internal refactoring, interface preserved); TMDB Row Scatter-Gather \textbf{modified} (two hand-written fan-outs replaced by the generic \texttt{fetchRows} aggregator); tRPC Request Context \textbf{extended} (\texttt{region}); others preserved.",
     r"(1) \emph{Duplicate Code / Long Method} in \path{lib/fetchers.ts}: 8 + 4 copies of fetch / ok-check / json / return field and an 8-term \texttt{||} condition. Technique: rows as data + one \texttt{fetchRows} helper (Extract Function). (2) \emph{Duplicate Code}: the same 7-entry title/row array in the Home, Movies and TV pages. Technique: \texttt{GENRE\_ROWS} + \texttt{toCategories} (Extract Function). Behaviour preservation: the URL/order/key/error characterization tests pass on the original and on CH02; row titles pinned (the TV page keeps ``Scary Movies'')."),
    ("CH03 --- Parental control", "e420dcf", "f393031", "Change3", "CH03",
     r"Each profile has a maturity rating \textbf{KIDS / TEEN / ADULT} (default ADULT, so existing profiles are unchanged), set on Edit Profile. KIDS hides adult titles and Horror, Thriller, Crime, War; TEEN hides adult titles and Horror. Restricted titles disappear from rows, hero, search and My List of that profile; the server refuses them in \texttt{catalogue.checkAccess} and \texttt{myList.create}; another account's profile id is refused. Acceptance (\path{tests/ch03-parental.test.ts}): 9 rating cases; chain order region $\rightarrow$ maturity $\rightarrow$ premium; client filter only for restricted profiles; foreign profile \texttt{FORBIDDEN}; Kids profile cannot save horror; rating stored by \texttt{profile.update}.",
     r"\texttt{enum MATURITY} + \texttt{Profile.maturityLevel} in \path{prisma/schema.prisma} (apply with \texttt{prisma db push}); \path{config/maturity.ts}; \texttt{MaturityRule} between Region and Premium; \texttt{profileVisibleShows}; \texttt{catalogue.checkAccess} loads the profile with an owner check; maturity guard in \texttt{myList.create}; rating selector in \path{edit-profile-form.tsx}; filtering in \texttt{ShowsContainer}, \texttt{Hero}, search grid.",
     r"Content Access Rule Chain and Access Rule Evaluation Template \textbf{extended} (MaturityRule); Active Profile Selection \textbf{extended} (Hero becomes a new observer, selector on \texttt{maturityLevel}); Search Results Broadcast \textbf{modified} (ShowsContainer filters the broadcast results); Persisted Profile Store preserved (persisted profile now carries the rating); all 13 second-pass instances preserved; others preserved.",
     r"\emph{Duplicate Code} in \path{routers/my-list.ts}: identical 17-field zod schema twice, the ``load profile or NOT\_FOUND'' block three times, field-by-field copies twice. Technique: Extract Variable (\texttt{showInput}), Extract Function (\texttt{findProfileWithList}, \texttt{findShowOrThrow}, \texttt{showData}). Behaviour preservation: \path{tests/characterization-mylist.test.ts} (update/delete errors and written data) ran on the original first and passes on CH03."),
]
hot = {(h["file_group"], h["snapshot"]): h for h in HOT}
HOTROW = {"CH01": ["plan data (plans.ts + subscriptions.ts + plan-catalog.ts)", "tRPC pipeline (server/api/trpc.ts)"],
          "CH02": ["TMDB facade (lib/fetchers.ts)", "row pages (4 shows pages + lib/catalogue.ts)"],
          "CH03": ["my-list router (routers/my-list.ts)", "access chain (lib/access/*)"]}
PREV = {"CH01": "baseline", "CH02": "CH01", "CH03": "CH02"}
STAT = {"CH01": "22 files, +642/-186", "CH02": "17 files, +499/-231", "CH03": "19 files, +536/-147"}
for title, before, after, folder, key, req, impl, eff, refac in CH:
    a, b = snap[PREV[key]], snap[key]
    w(r"\subsection*{" + title + "}\n")
    w(r"\entry{Change and acceptance criteria}{" + req + "}\n")
    w(r"\entry{Before and after}{commits \texttt{" + before + r"} $\rightarrow$ \texttt{" + after + r"} (" + STAT[key] + r" incl.\ tests); diff \path{Part2/changes/" + folder + r"/change.diff}, file list \path{Part2/changes/" + folder + r"/diffstat.txt}, requirement record \path{Part2/changes/" + folder + "/README.md}.}\n")
    w(r"\entry{Implementation and tests}{" + impl + r" Run: \texttt{yarn test} and \texttt{yarn typecheck} in \path{Part2/code}. \textbf{Actual result: " + b["tests_passed"] + "/" + b["tests_total"] + r" tests passed, typecheck " + b["typecheck"] + r"} (\path{Part2/changes/" + folder + r"/test_result.log}).}" + "\n")
    w(r"\entry{Pattern effects}{" + eff + "}\n")
    w(r"\entry{Refactoring}{" + refac + "}\n")
    w(r"\entry{Before/after metrics}{lizard 1.24.1, scope \path{src/} without tests and CSS, identical for every snapshot (\path{data/test_result/part2/run_snapshots.sh}).}" + "\n")
    w(r"\begin{tabularx}{\linewidth}{@{}Xrr@{}}\toprule Measure & " + PREV[key] + " & " + key + r"\\\midrule" + "\n")
    w(f"src files / NLOC / functions & {a['src_files']} / {a['src_nloc']} / {a['functions']} & {b['src_files']} / {b['src_nloc']} / {b['functions']}\\\\\n")
    w(f"average CCN & {a['avg_ccn']} & {b['avg_ccn']}\\\\\n")
    for g in HOTROW[key]:
        ha, hb = hot[(g, PREV[key])], hot[(g, key)]
        w(f"{esc(g)}: NLOC / max CCN & {ha['nloc']} / {ha['max_ccn']} & {hb['nloc']} / {hb['max_ccn']}\\\\\n")
    w(f"tests passed & {a['tests_passed'] if PREV[key] != 'baseline' else '0 (13/13 at d68c773)'} & {b['tests_passed']}/{b['tests_total']}\\\\\\bottomrule\\end{{tabularx}}\n")
    if key == "CH01":
        w(r"\par Max CCN of the whole \path{src/} is reported as 23 $\rightarrow$ 25 by lizard; this is a \textbf{parser artefact}: the CCN-25 function is the unchanged ``Add to My List'' \texttt{onClick} handler in \path{show-modal.tsx} (body identical, checked by script), which lizard did not detect as a function in the baseline JSX." + "\n")

w(r"""\begin{figure}[H]\centering\includegraphics[width=0.85\linewidth]{Part2/diagrams/01_content_access_rule_chain_CH03.png}
\caption{Newly introduced Content Access Rule Chain after CH03 (\texttt{Part2/diagrams/01\_content\_access\_rule\_chain\_CH03.puml}).}\end{figure}
\begin{figure}[H]\centering\includegraphics[width=\linewidth]{Part2/diagrams/02_content_access_sequence_CH03.png}
\caption{One \texttt{catalogue.checkAccess} request through both chains (auth middleware chain and access rule chain).}\end{figure}
Further updated UML: \path{Part2/diagrams/03_template_method_access_rule_CH03}, \path{04_cor_authenticated_pipeline_CH01}, \path{05_composite_api_router_tree_CH01}, \path{06_observer_active_profile_selection_CH03}, \path{07_facade_tmdb_refactored_CH02}, \path{08_plan_catalogue_refactor_CH01}, and for the second-pass instances \path{09_front_controller_trpc_api_CH01}, \path{10_builder_procedure_builder_CH01}, \path{11_context_object_request_context_CH02}, \path{12_scatter_gather_fetch_rows_CH02} (\texttt{.puml} + \texttt{.png}).
""")
w(r"""\subsection{Updated pattern counts}
Counts per snapshot (\path{Part2/Pattern_count.csv}); rows with participants, locations, status and change description per instance and snapshot in \path{Part2/pattern_evalution.csv} (118 rows; all 374 evolved locations computed from anchors per snapshot and checked, 0 problems).

\begin{tabularx}{\linewidth}{@{}lXcccc@{}}\toprule Snapshot & Change in counts & Types & Instances & Concrete & Rejected / uncertain\\\midrule
baseline 676e5dd & --- & 16 & 28 & 50 & 11 / 5\\
CH01 3f79642 & + Content Access Rule Chain (CoR), + Access Rule Evaluation Template (new type Template Method); Front Controller, Builder, Context Object extended & 17 & 30 & 56 & 11 / 5\\
CH02 e420dcf & instances continue (RegionRule added; Scatter-Gather modified; region in the context) & 17 & 30 & 57 & 11 / 5\\
CH03 f393031 & instances continue (MaturityRule, Hero observer) & 17 & 30 & 60 & 11 / 5\\\bottomrule
\end{tabularx}

Per-type instance counts after CH01--CH03: Observer 4, Chain of Responsibility 3, Proxy 3, Singleton 2, Adapter 2, Strategy 2, Read-Through Cache 2, Front Controller 2, Error Boundary 2, and Composite, Decorator, Facade, Builder, Context Object, Suspense Boundary, Scatter-Gather, Template Method 1 each. (Concrete counts: baseline from the Part 1 records, snapshots computed from the role definitions in \path{data/test_result/part2/part2_evolution.py}.) No instance was replaced or removed. The two new instances are student-added and share participant classes: the \emph{chain} is the object-level collaboration (links via \texttt{setNext}), the \emph{template} is the class-level one (\texttt{check} fixed in the base class, \texttt{evaluate} overridden). The old Authenticated Procedure Pipeline continues under its name and now feeds the plan tier into the new chain.
""")
w(r"""\entry{Interpretation}{\textbf{Benefits.} Each new rule was one class plus one line in \texttt{contentAccessChain}; the CH02/CH03 diffs did not touch \texttt{PremiumContentRule}. Ordering ``hide before lock'' is explicit and tested. Extending the existing tRPC chain (\texttt{attachSubscription}) gave every resolver the plan once per request; because tRPC builders are immutable, deriving \texttt{subscribedProcedure} could not change the 18 existing protected procedures, and the Context Object absorbed both the plan (CH01) and the region (CH02) without touching resolver signatures. The refactorings removed real duplication: the facade's max CCN fell 9 $\rightarrow$ 3, the row pages 174 $\rightarrow$ 116 NLOC, the My-List router 169 $\rightarrow$ 114 NLOC, and the plan data shrank 139 $\rightarrow$ 123 NLOC while gaining a fifth plan. \textbf{Trade-offs.} Total NLOC grew 6694 $\rightarrow$ 6916 (+3.3\%) and functions 280 $\rightarrow$ 328, mostly new features and small helpers; more LOC here is not worse design and less LOC alone would not prove better design. The rule chain is evaluated in three places (server rows, tRPC, browser) with different context completeness (rows know region only, the browser knows maturity only). \textbf{Remaining limitations.} Sample licence/premium data; hand-written profile \texttt{select} in four pages (another Shotgun Surgery spot); the persisted profile keeps an old rating until re-selected; pre-existing missing ownership checks on profile/My-List procedures; no end-to-end run with real services.}
""")

# ---------------------------------------------------------------- section 4
w(r"""
\section{Part 3 Cross-language comparison}
\entry{Selected instances}{One verified instance per confirmed baseline type (16 problems; problems 11--16 were added for the six types found in the second pass). Where a type has several instances we chose the one that best shows the pattern in a small problem: Chain of Responsibility --- \emph{Content Access Rule Chain} (CH03 state; richer than the one-handler auth pipeline and also exercises the Template Method introduced in CH01); Singleton --- \emph{Shared Prisma Database Client} (explicit holder, hot-reload behaviour); Observer --- \emph{Active Profile Selection} (most observers, extended in CH03); Proxy --- \emph{Environment Secret Guard} (protection logic shows the language mechanisms best); Decorator --- Persisted Profile Store; Adapter --- NextAuth Prisma Persistence Adapter; Strategy --- Sign-in Provider Strategy; Facade --- TMDB Catalogue Facade (after CH02); Composite --- API Router Tree (after CH01); Read-Through Cache --- My List Query Cache; Front Controller --- \emph{tRPC API Front Controller} (after CH01; richer than the NextAuth controller and shows batching with one shared context); Builder --- tRPC Procedure Builder; Context Object --- tRPC Request Context (after CH02, with region and plan refinement); Error Boundary --- Shows Segment Error Boundary, modelled together with the Root Global Error Boundary because their interaction (fallback errors propagate upwards) is the essential behaviour; Suspense Boundary --- Shows Loading Placeholder; Scatter-Gather --- TMDB Row Scatter-Gather (after CH02).}
\entry{Common specifications}{For each problem, \path{Part3/<problem>/spec.md} gives inputs, outputs, rules and error cases, and \path{Part3/<problem>/cases.tsv} is the \emph{single shared fixture} read by all four test runners (8--16 cases each, 177 in total, including error cases such as unknown maturity, invalid NODE\_ENV, unknown decorator, ORM constraint errors, unsupported provider, invalid media type, server-variable access on the client, missing My-List entry, unknown procedure path, missing input, unauthenticated call, building twice, invalid geo header, failing fallback, failing fetch). Test doubles that belong to the problem (fake HTTP client in 07) are defined identically in every runner.}
""")
w(r"\entry{Implementations}{Folders \texttt{Part3/NN\_<pattern>\_<problem>/\{java,python,javascript,cpp\}/} with production code, a separate test runner and a README with the run command. Runtimes: " + esc(XL[0]["runtime_compiler"]) + "; " + esc([r for r in XL if r["language"] == "Python"][0]["runtime_compiler"]) + "; " + esc([r for r in XL if r["language"] == "JavaScript"][0]["runtime_compiler"]) + "; " + esc([r for r in XL if r["language"] == "C++"][0]["runtime_compiler"]) + r""". Commands (working folder = language folder):
\begin{itemize}
\item Java: \texttt{javac -d build *.java}; \texttt{java -cp build Runner ../cases.tsv}
\item Python: \texttt{python -B test\_runner.py ../cases.tsv}
\item JavaScript: \texttt{node testRunner.js ../cases.tsv}
\item C++: \texttt{g++ -std=c++17 -O2 -Wall -o build/test\_runner test\_runner.cpp}; \texttt{./build/test\_runner ../cases.tsv}
\end{itemize}
All 64 are built, run, timed and measured by \path{data/test_result/part3/run_all.py} (run 2026-10-30 on Windows 11 x64; toolchain in \path{data/test_result/part3/environment.txt}); the script also regenerates every language README from the measured values.}""" + "\n")
w(r"\entry{Actual results}{\textbf{All 64 implementations pass all their cases} (177 cases $\times$ 4 languages = 708 checks); none marked not run. Logs: \path{Part3/<problem>/<language>/test_result.log}.}" + "\n")
w(r"""\entry{Static and dynamic comparison}{Rules: LOC = lizard NLOC of production files only; max CC = largest lizard cyclomatic complexity of one function; time = median of 5 runs after 1 warm-up, whole process incl.\ runtime start-up and reading the fixture (raw: \path{data/test_result/part3/timings.csv}). Full table with notes: \path{Part3/llm/pattern_crosslanguage.csv}.}
\begin{longtable}{@{}p{4.6cm}rrrrrrrr@{}}\toprule
& \multicolumn{4}{c}{source LOC} & \multicolumn{4}{c}{median ms}\\
Problem & Java & Py & JS & C++ & Java & Py & JS & C++\\\midrule\endhead
""")
byprob = defaultdict(dict)
for r in XL:
    byprob[r["snippet_path"].split("/")[1]][r["language"]] = r
L = ["Java", "Python", "JavaScript", "C++"]
for prob in sorted(byprob):
    d = byprob[prob]
    name = esc(d["Java"]["pattern_name"] + " (" + prob[:2] + ")")
    w(name + " & " + " & ".join(d[l]["source_loc"] for l in L) + " & " + " & ".join(d[l]["median_process_ms"] for l in L) + r"\\" + "\n")
agg = {l: [r for r in XL if r["language"] == l] for l in L}
w(r"\midrule Total LOC / median of medians & " + " & ".join(str(sum(int(r["source_loc"]) for r in agg[l])) for l in L) + " & " +
  " & ".join(f"{statistics.median(float(r['median_process_ms']) for r in agg[l]):.1f}" for l in L) + r"\\" + "\n")
w(r"Max function CC (all problems) & " + " & ".join(str(max(int(r["max_function_cc"]) for r in agg[l])) for l in L) + r" & & & & \\\bottomrule\end{longtable}" + "\n")
w(r"""\entry{Comparison}{\textbf{Participant structures.} The same roles appear in every language, but how they are expressed differs. Java and C++ name every role as a type (interfaces / abstract classes, \texttt{final}/\texttt{override}), so the participant mapping is visible in declarations; Python relies on duck typing (ABC only where an abstract step must be enforced, e.g.\ \texttt{AccessRule.evaluate}); JavaScript often needs no class at all: observers are functions in a \texttt{Set}, decorators are functions \texttt{store $\rightarrow$ store} that spread and override, the adapter is a factory returning an object literal --- exactly the style of zustand, next-auth and tRPC in the source. \textbf{Abstraction and inheritance vs.\ composition.} Template Method needs inheritance in all four (abstract \texttt{check}/\texttt{evaluate}); all other problems use composition: decorators wrap, chains link, the facade holds the HTTP client. In C++ ownership is part of the design (\texttt{unique\_ptr} for chain links and decorators, non-owning pointers for observers, \texttt{shared\_ptr} to keep the singleton's identity across reloads). \textbf{Language features.} Proxy is the clearest difference: JavaScript's built-in \texttt{Proxy} traps property access (identical to \path{env.mjs}); Python's \texttt{\_\_getattr\_\_} intercepts attribute reads; Java's \texttt{java.lang.reflect.Proxy} intercepts interface calls at run time via reflection; C++ has no run-time interception, so the proxy is an ordinary class implementing the same interface. Records/dataclasses/structs give value objects; \texttt{Optional}/\texttt{std::optional}/\texttt{None}/\texttt{null} express ``no result'' in the chain and adapter. JavaScript is the only version of the facade that is asynchronous (\texttt{Promise.all}), like the source. \textbf{Static vs.\ dynamic results.} @@DYN@@ The timing therefore compares runtimes, not the patterns. New problems: the Front Controller and the C++ Builder director have the highest function complexity (CC 9--11: one branch per error code / build step), Scatter-Gather is the smallest in JavaScript (10 NLOC) because \texttt{Promise.all} \emph{is} the pattern there, and the C++ Scatter-Gather is the only version that starts real OS threads (\texttt{std::async}).}
\entry{Technology discussion}{The case-study stack implements several patterns in its frameworks, so the application inherits them: tRPC middlewares form a Chain of Responsibility in which each middleware calls \texttt{next()} or stops the request [8]; zustand middlewares (\texttt{persist}, \texttt{devtools}) are decorators over a state creator [9]; NextAuth separates providers (strategies) and database adapters [10]; TanStack Query is a read-through cache with explicit invalidation [11]. JavaScript's \texttt{Proxy} [5] is used both by tRPC (remote proxy) and by the T3 \texttt{env} module (protection proxy), while Java offers dynamic proxies only for interfaces [6] and Python offers attribute hooks [7]. This matches the GoF observation that patterns depend on language features [1]: in a language with first-class functions and proxies several GoF patterns shrink to idioms, which is what the JavaScript column and the source code show.}
""")

# ---------------------------------------------------------------- section 5
w(r"""
\section{LLM records and human verification}
\entry{Run and model}{Session 1: Claude (claude.ai), displayed model \textbf{Claude Opus 5.5}, access tier not recorded, 2026-10-10, Parts 1--3 (PROMPT 1 in each prompt file). Session 2: Claude Code desktop app, displayed model \textbf{Claude Opus 5.5}, 2026-10-29/30, exhaustive second pass of Part 1, evolution of the new instances, Part 3 problems 11--16 and the full re-run (PROMPT 2). Prompt files: \path{Part1/Part1_prompt.txt}, \path{Part2/Part2_prompt.text}, \path{Part3/llm/part3_prompt.txt}; records: \path{Part1/llm.csv}, \path{Part2/llm.csv}, \path{Part3/llm/llm.csv}. The model worked in a sandbox with a shell: it cloned the application, ran the typechecker, tests, lizard and the Part 3 programs itself, so its numeric results come from real runs.}
\entry{Inputs and outputs}{Input: \path{data/code/} (commit 676e5dd), the three assignment files and (session 2) the dependency sources of the pinned versions. Outputs and claim tables: \path{data/test_result/llm/part1_llm_output.md}, \path{part2_llm_output.md}, \path{part3_llm_output.md} (session 1) and \path{part1_second_pass_output.md}, \path{part2_second_pass_output.md}, \path{part3_second_pass_output.md} (session 2), all in \path{data/test_result/llm/}. The raw transcript must be exported from claude.ai into the same folders (the conversation transcripts are not included; the exact prompts are in the prompt files and every model claim is listed with its check in these output records).}
\entry{Claims and evaluation}{Partially correct, corrected before submission. Errors found by checking the model's own work against the source and tools: (1) first inventory had 14 instances --- the Environment Secret Guard proxy was missed and added on a second pass; (2) three line ranges were wrong (two end lines, one offset) --- found by an independent locator and corrected; (3) first Part 2 NLOC run ignored \texttt{.tsx} files (1617 instead of 6694) --- corrected; (4) a reported max-CCN increase was identified as a lizard parsing artefact. One claim was not accepted: the Stripe webhook as Observer (kept as uncertain). Session 2: 16 Part 1 claims checked against application and dependency source --- 13 instances confirmed, the pages-router link chain claimed active was wrong (never executed; recorded as uncertain), explicit Suspense wrappers rejected, and one role of an existing record corrected; three first drafts of Part 3 code were wrong (Java cyclic inheritance, C++ \texttt{const} members preventing assignment, error-boundary reset rule) and fixed before the recorded runs. Correct claims include the missing licence, dead caching-proxy code, the client-side PIN check and the 18/19 protected procedures. Reviewer: Part 1 claims re-checked by AM.SC.U4CSE23161 Swaminathan A and AM.SC.U4CSE23242 Pooja Sathyan (Part 1); Part 2 claims by AM.SC.U4CSE23230 Leya Paul and AM.SC.U4CSE23207 Anna Ouseph (Part 2); Part 3 claims by AM.SC.U4CSE23069 Rahul Rajan (Part 3).}
\entry{Generated code}{All Part 2 production code and tests and all Part 3 code were generated by the model. Use and testing: Part 2 --- characterization tests run on the original before refactoring, acceptance tests per change, 65/65 passing plus typecheck on the final snapshot; Part 3 --- 64 implementations, 708/708 shared-fixture checks. The team must review and be able to explain this code Reviewers: AM.SC.U4CSE23161 Swaminathan A and AM.SC.U4CSE23242 Pooja Sathyan (Part 1); AM.SC.U4CSE23230 Leya Paul and AM.SC.U4CSE23207 Anna Ouseph (Part 2); AM.SC.U4CSE23069 Rahul Rajan (Part 3)..}
""")

# ---------------------------------------------------------------- section 6
w(r"""
\section{Findings, contributions and references}
\entry{Findings}{\begin{itemize}
\item netflx-web uses \textbf{16 pattern types in 28 collaborations} at the baseline (first pass: 10 / 15). Most come from frameworks and libraries (tRPC, zustand, NextAuth, React Query, Next.js, T3 scaffold) and are configured, not written, by the application; the second pass shows that a first pass limited to the feature areas misses exactly this infrastructure (front controllers, builder, context object, boundaries). Observer (4) is the most frequent; recommendation has no pattern because it has no logic.
\item The access requirements fitted the existing Chain of Responsibility idea: one tRPC middleware was added and a new rule chain absorbed premium, region and parental rules with one class each; the chain order (hide before lock) is a design decision of its own and is tested.
\item The env Protection Proxy explains a code smell: the plan list was duplicated because the server list reads secrets. Moving the client-safe part into one module removed the duplication and an existing inconsistency.
\item Security observations (pre-existing, reported): the profile PIN is checked in the browser; profile and My-List procedures accept any profileId; the server caching proxy is dead code; two tRPC client proxies exist side by side.
\item Limitations: no end-to-end run with real Stripe, TMDB and Google services; sample licence and premium data; lizard's TSX parsing is imperfect; Part 3 times are start-up dominated and machine-specific.
\end{itemize}}
\entry{Contributions}{Work was divided by part; each member reviewed the LLM output of their part against the source and tests.\par\medskip
\begin{tabularx}{\linewidth}{@{}lllX@{}}\toprule Roll number & Name & Batch & Contribution\\\midrule
AM.SC.U4CSE23161 & Swaminathan A & CSE B & Part 1 pattern discovery: application selection, pattern records and participant mapping, rejected/uncertain candidates, location checks, architecture and pattern UML (\path{Part1/}, \path{data/test_result/part1/}).\\
AM.SC.U4CSE23207 & Anna Ouseph & CSE C & Part 2 evolution: CH01--CH03 requirements, acceptance tests and implementation review, refactorings and before/after metrics (\path{Part2/changes/}, \path{Part2/code/}).\\
AM.SC.U4CSE23230 & Leya Paul & CSE C & Part 2 evolution: pattern status per snapshot, \path{Part2/pattern_evalution.csv}, \path{Part2/Pattern_count.csv}, updated UML (\path{Part2/diagrams/}).\\
AM.SC.U4CSE23242 & Pooja Sathyan & CSE C & Part 1 pattern discovery: exhaustive second pass, dependency-source verification, \path{Part1/patterns.csv}, \path{Part1/Pattern_count.csv}, \path{Part1/llm.csv}.\\
AM.SC.U4CSE23069 & Rahul Rajan & CSE A & Part 3 cross-language comparison: 16 problems in Java, Python, JavaScript and C++, shared fixtures, measurements, \path{Part3/llm/pattern_crosslanguage.csv}, slides (\path{Part3/}).\\\bottomrule\end{tabularx}}
\entry{References}{\begin{enumerate}[label={[\arabic*]}]
\item E. Gamma, R. Helm, R. Johnson, J. Vlissides, \emph{Design Patterns: Elements of Reusable Object-Oriented Software}, Addison-Wesley, 1994.
\item M. Fowler, \emph{Refactoring: Improving the Design of Existing Code}, 2nd ed., Addison-Wesley, 2018.
\item sadmann7, netflx-web, \url{https://github.com/sadmann7/netflx-web} (commit 676e5dd, accessed 2026-10-10).
\item Next.js documentation, \url{https://nextjs.org/docs}; T3 stack (create-t3-app), \url{https://create.t3.gg}.
\item MDN Web Docs, ``Proxy'', \url{https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy}.
\item Oracle, Java SE 21 API, \texttt{java.lang.reflect.Proxy}, \url{https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/Proxy.html}.
\item Python 3 Language Reference, Data model --- customizing attribute access, \url{https://docs.python.org/3/reference/datamodel.html}.
\item tRPC documentation (procedures and middlewares), \url{https://trpc.io/docs}.
\item zustand (incl.\ \texttt{persist} and \texttt{devtools} middleware), \url{https://github.com/pmndrs/zustand}.
\item NextAuth.js documentation (providers, adapters), \url{https://next-auth.js.org}.
\item TanStack Query v4 documentation (caching, invalidation), \url{https://tanstack.com/query/v4}.
\item lizard code complexity analyser, \url{https://github.com/terryyin/lizard}; PlantUML, \url{https://plantuml.com}; vitest, \url{https://vitest.dev}.
\end{enumerate}}
""")

# ---------------------------------------------------------------- section 7
w(r"""
\section{Team folder and datasets (take a screenshots from the GitHub repository--- your team)}
Screenshots of the uploaded team folder (\path{data/test_result/screenshots/}):
\begin{figure}[H]\centering
\begin{minipage}[t]{0.32\linewidth}\centering\includegraphics[width=\linewidth]{data/test_result/screenshots/github_part1.png}\\Part1\end{minipage}\hfill
\begin{minipage}[t]{0.32\linewidth}\centering\includegraphics[width=\linewidth]{data/test_result/screenshots/github_part2.png}\\Part2\end{minipage}\hfill
\begin{minipage}[t]{0.30\linewidth}\centering\includegraphics[width=\linewidth]{data/test_result/screenshots/github_part3.png}\\Part3\end{minipage}
\caption{Team A12 folder in the GitHub repository.}\end{figure}
\begin{verbatim}
A12/
  README.md
  A12_Report.pdf
  A12_Report.tex
  data/
    code/          original application source (676e5dd)
    test_result/   baseline logs, Part 1-3 evidence scripts and logs,
                   raw timings, LLM output records
  Part1/
    patterns.csv
    Pattern_count.csv
    pattern_architecture/   diagram sources (.puml) + images (.png)
    Part1_prompt.txt
    llm.csv
  Part2/
    code/          evolved application source (CH03)
    changes/Change1..3/     requirement, diff, test result (+ patch)
    pattern_evalution.csv
    Pattern_count.csv
    diagrams/      updated UML
    Part2_prompt.text
    llm.csv
  Part3/
    NN_<pattern>_<problem>/   16 folders, each with spec.md, cases.tsv and
      java/ python/ javascript/ cpp/   snippet, test runner, README, log
    llm/
      part3_prompt.txt
      llm.csv
      pattern_crosslanguage.csv
      A12_slide.pdf (+ .tex)
\end{verbatim}

\end{document}
""")

tot = {l: sum(int(r["source_loc"]) for r in agg[l]) for l in L}
rng = {l: (min(float(r["median_process_ms"]) for r in agg[l]), max(float(r["median_process_ms"]) for r in agg[l])) for l in L}
dyn = (f"Python and JavaScript need less code than Java and C++ ({tot['Python']} and {tot['JavaScript']} vs.\\ {tot['Java']} and {tot['C++']} NLOC in total over the 16 problems); "
       f"in {sum(1 for r in XL if int(r['max_function_cc']) <= 7)} of {len(XL)} implementations no function exceeds CC 7; the exceptions are the Front Controller dispatch methods and the C++ Builder director (CC 9--11). "
       f"Measured times (Windows 11 x64) are dominated by process start-up: native C++ {rng['C++'][0]:.1f}--{rng['C++'][1]:.1f}\\,ms, "
       f"Python {rng['Python'][0]:.1f}--{rng['Python'][1]:.1f}\\,ms (the maximum is Scatter-Gather, which starts an asyncio event loop per case), "
       f"Node.js {rng['JavaScript'][0]:.1f}--{rng['JavaScript'][1]:.1f}\\,ms, JVM {rng['Java'][0]:.1f}--{rng['Java'][1]:.1f}\\,ms.")
text = "".join(out).replace("@@DYN@@", dyn)
open("A12_Report.tex", "w", encoding="utf-8", newline="\n").write(text)
print("written A12_Report.tex", sum(len(x) for x in out), "chars")
