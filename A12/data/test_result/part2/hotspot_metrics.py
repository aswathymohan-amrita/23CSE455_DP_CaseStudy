"""Per-file NLOC / function count / max CCN for the refactored files at each snapshot.
Run after run_snapshots.sh (needs the /tmp/a12-<snapshot> worktrees). Tool: lizard."""
import csv, os, sys
import lizard

SNAPS = ["baseline", "CH01", "CH02", "CH03"]
GROUPS = {
    "plan data (plans.ts + subscriptions.ts + plan-catalog.ts)": ["src/config/plans.ts", "src/config/subscriptions.ts", "src/config/plan-catalog.ts"],
    "TMDB facade (lib/fetchers.ts)": ["src/lib/fetchers.ts"],
    "row pages (4 shows pages + lib/catalogue.ts)": ["src/app/(shows)/page.tsx", "src/app/(shows)/movies/page.tsx", "src/app/(shows)/tv-shows/page.tsx", "src/app/(shows)/new-and-popular/page.tsx", "src/lib/catalogue.ts"],
    "my-list router (routers/my-list.ts)": ["src/server/api/routers/my-list.ts"],
    "access chain (lib/access/*)": ["src/lib/access/types.ts", "src/lib/access/rules.ts", "src/lib/access/policy.ts"],
    "tRPC pipeline (server/api/trpc.ts)": ["src/server/api/trpc.ts"],
}
rows = []
for group, files in GROUPS.items():
    for snap in SNAPS:
        nloc = fns = maxccn = 0; present = 0
        for f in files:
            p = f"/tmp/a12-{snap}/{f}"
            if not os.path.exists(p):
                continue
            present += 1
            info = lizard.analyze_file(p)
            nloc += info.nloc; fns += len(info.function_list)
            maxccn = max([maxccn] + [fn.cyclomatic_complexity for fn in info.function_list])
        rows.append([group, snap, present, nloc, fns, maxccn])
w = csv.writer(sys.stdout)
w.writerow(["file_group", "snapshot", "files_present", "nloc", "functions", "max_ccn"])
w.writerows(rows)
