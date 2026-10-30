# A12 - Design Pattern Analysis in a Next.js-Based Video Streaming Application

23CSE455 Design Patterns case study - OTT / video streaming application using React / Next.js.

| Roll number | Name | Batch |
|---|---|---|
| AM.SC.U4CSE23161 | Swaminathan A | CSE B |
| AM.SC.U4CSE23207 | Anna Ouseph | CSE C |
| AM.SC.U4CSE23230 | Leya Paul | CSE C |
| AM.SC.U4CSE23242 | Pooja Sathyan | CSE C |
| AM.SC.U4CSE23069 | Rahul Rajan | CSE A |

Report: `A12_Report.pdf` (source `A12_Report.tex`, regenerated from the datasets by
`data/test_result/tools/build_report.py`). Slides: `Part3/llm/A12_slide.pdf`.

## Results at a glance

| Part | Result | Where |
|---|---|---|
| 1 Pattern discovery | **16 pattern types, 28 instances** at the baseline (first pass 10 / 15, exhaustive second pass +6 types / +13 instances); 50 concrete participants; 11 rejected, 5 uncertain candidates; 156 cited line ranges checked (0 problems) | `Part1/patterns.csv`, `Part1/Pattern_count.csv`, `Part1/pattern_architecture/`, `data/test_result/part1/candidates.md` |
| 2 Evolution | 3 changes (premium content + Ultra plan, regional restrictions, parental control); 65/65 tests on the final snapshot; 17 types / 30 instances after CH01-CH03; 4 real refactorings | `Part2/changes/Change1..3/`, `Part2/pattern_evalution.csv`, `Part2/Pattern_count.csv`, `Part2/diagrams/` |
| 3 Cross-language | all 16 pattern types in Java, Python, JavaScript and C++: **64 implementations, 177 shared cases, 708/708 passing** | `Part3/NN_*/`, `Part3/llm/pattern_crosslanguage.csv` |

Pattern types: Chain of Responsibility, Singleton, Observer, Decorator, Adapter, Strategy, Facade,
Composite, Proxy, Read-Through Cache, Front Controller, Builder, Context Object, Error Boundary,
Suspense Boundary, Scatter-Gather (+ Template Method, introduced in CH01).

## Application and source
- Application: **netflx-web** - "An open source Netflix clone built using the new app router,
  server components, trpc, and everything new in Next.js 13" by sadmann7.
- URL: https://github.com/sadmann7/netflx-web (accessed 2026-10-10; 770 stars, 119 forks).
- Baseline commit: `676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258` (2024-06-12, "Merge pull request #11").
  Snapshot: `data/code/` (`git archive` of that commit; upstream line endings kept).
- **Licence: the repository has no LICENSE file** (all rights reserved by default). The code is
  used here for academic analysis only; the course faculty approved this use for the case study.
- Evolved versions (Part 2) on branch `a12-evolution` of a local clone:

| Snapshot | Commit | Content |
|---|---|---|
| baseline | 676e5dd | original application |
| tests_only | d68c773 | vitest + characterization tests, no production change |
| CH01 | 3f79642 | premium content + Ultra plan |
| CH02 | e420dcf | regional restrictions |
| CH03 | f393031 | parental control (final; snapshot in `Part2/code/`) |

  Reproduce (the commit hashes differ if your committer name/date differ; the trees are identical):
  ```
  git clone https://github.com/sadmann7/netflx-web && cd netflx-web && git checkout -b a12-evolution 676e5dd
  git am <A12>/data/test_result/part2/0001-*.patch <A12>/Part2/changes/Change1/0002-*.patch \
         <A12>/Part2/changes/Change2/0003-*.patch <A12>/Part2/changes/Change3/0004-*.patch
  ```

## Environment (versions from `yarn.lock` / tools used)
Application: Next.js 13.4.4 (`next ^13.3.1`), React 18.2.0, TypeScript 5.0.4, tRPC 10.28.0, NextAuth
4.22.1 (+ @next-auth/prisma-adapter 1.0.6), Prisma 4.14.1 (MySQL, `relationMode = "prisma"`), Stripe
12.7.0, Zustand 4.3.8, @tanstack/react-query 4.29.7, superjson 1.12.3, Tailwind CSS 3.3.2.

| Analysis run | Machine | Tools |
|---|---|---|
| 2026-10-10 (Parts 1-3, first pass) | Linux x86_64 sandbox | Node.js 22.22.0, yarn 1.22.22, vitest 1.6.0, lizard 1.24.1, OpenJDK 21.0.12.1, Python 3.13.16, g++ 13.3.0, PlantUML + Graphviz |
| 2026-10-29/30 (second pass, Part 3 re-run) | Windows 11 x64 | Temurin JDK 21.0.12, Python 3.12.10, Node.js 26.13.0, g++ 16.2.0 (WinLibs UCRT), lizard 1.24.3, PlantUML 1.2024.7 (smetana layout), MiKTeX pdflatex; dependency sources via `npm pack` |

The Part 3 numbers in `Part3/llm/pattern_crosslanguage.csv` are from the Windows run
(`data/test_result/part3/environment.txt`); the Part 2 numbers are from the Linux run.

## Run / test commands
```
# application (needs .env from .env.example: MySQL URL, Google OAuth, TMDB key, Stripe keys)
cd Part2/code            # or data/code/ for the baseline
yarn install             # runs prisma generate
npx prisma db push       # create tables (CH03 adds Profile.maturityLevel)
yarn dev                 # http://localhost:3000
yarn stripe:listen       # forward Stripe webhooks (Stripe CLI)

# checks (Part 2)
yarn typecheck           # tsc --noEmit   (Part2/code only; baseline: npx tsc --noEmit)
yarn test                # vitest run     (Part2/code: 65/65)

# Part 1 datasets and checks (from A12/)
python data/test_result/part1/part1_patterns.py            # writes Part1/patterns.csv, Part1/Pattern_count.csv
python data/test_result/part1/verify_locations.py Part1/patterns.csv
python Part1/pattern_architecture/make_diagrams.py         # needs java + PLANTUML_JAR

# Part 2 evolution dataset (worktrees of the a12-evolution branch, see "Reproduce")
A12_WORKTREE_PREFIX=/path/to/wt- python data/test_result/part2/part2_evolution.py

# Part 3: every problem, every language (javac/java, python, node, g++ on PATH; pip install lizard)
python data/test_result/part3/run_all.py                    # or: run_all.py 11 12  (selected problems)
```
Each `Part3/<problem>/<language>/README.md` gives the build/run command for that snippet (working
folder = the language folder, fixture `../cases.tsv`).

Results in the analysis environments: `tsc --noEmit` passes for every snapshot; tests pass
(13/13 at d68c773, 29/29 CH01, 45/45 CH02, 65/65 CH03). `next build` could not be completed in the
Linux sandbox because it cannot reach Google Fonts (`next/font` download) - not a code error. Prisma
engines could not be downloaded there either, so tests use an in-memory fake of the Prisma client
(`Part2/code/tests/helpers.ts`) and no MySQL instance was used.

## Scope (inspected modules)
Inspected: `src/server/**`, `src/lib/**`, `src/config/**`, `src/stores/**`, `src/app/**` (except
`(docs)` and `api/og`), `src/components/**` (except `ui/*`), `src/@trpc/next-layout/**`,
`src/pages/**`, `src/hooks/**`, `src/context/**`, `src/env.mjs`, `prisma/schema.prisma`. In the
second pass every one of these files was read completely. Dependency code only where a pattern role
lives there, at the exact `yarn.lock` versions: next-auth 4.22.1, @next-auth/prisma-adapter, zustand,
@trpc/server, client, react-query, next 10.28.0, @tanstack/react-query, next 13.4.4.
Excluded: `components/ui/*` (generated shadcn primitives), `styles/`, `public/`, `app/(docs)`
(static text), `app/api/og` (Open Graph image) - none touches the seven case-study areas.

## Measurement rules
- **Line ranges**: 1-based, inclusive, from the file in `data/code/` (baseline) or the snapshot named
  in `source_version`. Checked with `data/test_result/part1/verify_locations.py` (start lines,
  file length) and computed from anchors with `data/test_result/part2/locate.py` (bracket-balanced
  end lines). Dependency locations: `package@version file:lines`.
- **Pattern counts**: one instance = one independent collaboration; two concrete classes in one
  collaboration are one instance. "Concrete participants" counts implementations of variable
  roles: ConcreteHandler, ConcreteObserver, ConcreteStrategy, ConcreteComponent/Decorator,
  Adapter, Singleton, Facade (module), Composite routers, Proxy, Cache, ConcreteClass,
  FrontController, ConcreteBuilder, ContextFactory, boundary fallbacks, scatter/gather functions.
- **LOC / complexity (Parts 2 and 3)**: lizard. LOC = lizard NLOC (no blank lines or comments).
  Part 2 scope = `src/` of each snapshot, `*.css` excluded, tests excluded
  (`data/test_result/part2/run_snapshots.sh`, lizard 1.24.1). Part 3 scope = production snippet
  files only, runners excluded (lizard 1.24.3). Max CC = largest lizard cyclomatic complexity of a
  single function.
- **Timing (Part 3)**: compile first (not timed), then 1 warm-up and 5 measured runs of the test
  command on the same machine; reported value = median wall-clock time of the **whole process**
  (runtime start-up + reading the shared `cases.tsv` + running all cases). Raw times (6 rows per
  implementation): `data/test_result/part3/timings.csv`. Machine: Windows 11 x64 laptop.

## Folder map (matches the course hierarchy)
```
A12/
  README.md
  A12_Report.pdf
  A12_Report.tex
  data/
    code/            original application source (676e5dd)
    test_result/     test cases, logs and evidence:
      baseline/        baseline typecheck / build / characterization logs
      part1/           pattern generator, location checker + log, candidates.md
      part2/           test-harness patch 0001, snapshot metrics, lizard CSVs, test/typecheck logs, scripts
      part3/           run_all.py, raw timings.csv, environment.txt
      llm/             raw LLM output records with claim-by-claim verification
      tools/           build_report.py
  Part1/
    patterns.csv
    Pattern_count.csv
    pattern_architecture/   architecture + one UML diagram per instance (.puml + .png, make_diagrams.py)
    Part1_prompt.txt
    llm.csv
  Part2/
    code/            evolved application source (CH03)
    changes/
      Change1/         requirement (README.md), diff, test result, typecheck, patch
      Change2/         requirement, diff, test result, typecheck, patch
      Change3/         requirement, diff, test result, typecheck, patch
    pattern_evalution.csv
    Pattern_count.csv
    diagrams/        updated UML where needed
    Part2_prompt.text
    llm.csv
  Part3/
    NN_<pattern>_<problem>/   16 folders; spec.md + cases.tsv shared by
      java/ python/ javascript/ cpp/   snippet, test runner, README, test_result.log
    llm/
      part3_prompt.txt
      llm.csv
      pattern_crosslanguage.csv
      A12_slide.pdf  (+ A12_slide.tex)
```
File names follow the course hierarchy exactly (including `pattern_evalution.csv` and
`Part2_prompt.text`). CSV paths are relative to this team folder.

## LLM use
Two sessions with Claude Opus 5.5 (claude.ai on 2026-10-10; Claude Code desktop app on
2026-10-29/30). The prompts are in `Part1/Part1_prompt.txt`, `Part2/Part2_prompt.text` and
`Part3/llm/part3_prompt.txt`; each part's `llm.csv` records model, date, inputs, outputs and the
evaluation; the claim-by-claim checks are in `data/test_result/llm/`. Human review entries (reviewer,
date) and the access tier must be completed by the team.

## Limitations
- Static analysis + unit tests with a fake database; no end-to-end run with real Stripe / TMDB / Google.
  Framework-implemented roles (error/Suspense boundaries, NextAuth dispatch) were verified in the
  dependency source, not observed at run time.
- Region licences and premium titles are sample rules (originals row = premium; 3 licensed TMDB ids).
- The persisted (sessionStorage) profile keeps an old maturity rating until it is re-selected.
- Pre-existing issues reported, not fixed: client-side PIN check; profile/myList procedures do
  not check that a profileId belongs to the caller; dead `createTRPCNextLayout`; two tRPC clients.
- lizard's TSX parsing is imperfect (see Part2/changes/Change1/README.md on the max-CCN artefact).
- Part 3 timings include runtime start-up and are machine-specific; Part 2 and Part 3 were measured
  on different machines.
- The 13 second-pass instances were tracked through CH01-CH03 by reading the snapshots; the
  CH01-CH03 test suites were not re-run in the second pass (no production code changed).
