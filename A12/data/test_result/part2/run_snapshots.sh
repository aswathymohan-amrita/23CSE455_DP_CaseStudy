#!/usr/bin/env bash
# Re-measures every Part 2 snapshot with the same tools and scope.
# Usage: bash data/test_result/part2/run_snapshots.sh <path-to-netflx-web-clone-with-a12-evolution-branch>
# Needs: node 22 + yarn deps installed in that clone, lizard (pip install lizard).
set -u
REPO=${1:?repo path}
OUT=$(cd "$(dirname "$0")" && pwd)
declare -A SNAP=( [baseline]=676e5ddd15d68fe6b83c2f9cc2494c6ece8b2258 [tests_only]=d68c773 [CH01]=3f79642 [CH02]=e420dcf [CH03]=f393031 )
echo "snapshot,commit,src_files,src_nloc,functions,avg_ccn,max_ccn,max_ccn_function,typecheck,tests_passed,tests_total" > "$OUT/metrics.csv"
for name in baseline tests_only CH01 CH02 CH03; do
  c=${SNAP[$name]}; wt=/tmp/a12-$name
  rm -rf "$wt"; git -C "$REPO" worktree prune; git -C "$REPO" worktree add -q --detach "$wt" "$c"
  ln -s "$REPO/node_modules" "$wt/node_modules"
  # metrics: production code only (src/, .ts/.tsx/.mjs), tests excluded
  lizard "$wt/src" -x "*.css" --csv > "$OUT/lizard_$name.csv" 2>/dev/null
  read files nloc fns avg max maxfn < <(python3 - "$OUT/lizard_$name.csv" "$wt/src" <<'PY'
import csv, sys
rows = list(csv.reader(open(sys.argv[1])))
# lizard csv: nloc,ccn,token,param,length,location,file,function,long_name,start,end
files = {r[6] for r in rows}
import os
allfiles = [os.path.join(d, f) for d, _, fs in os.walk(sys.argv[2]) for f in fs if f.endswith((".ts", ".tsx", ".mjs"))]
fn_nloc = sum(int(r[0]) for r in rows)
top = max(rows, key=lambda r: int(r[1]))
print(len(allfiles), "NLOC_PLACEHOLDER", len(rows), round(sum(int(r[1]) for r in rows) / len(rows), 2), top[1], top[7].replace(" ", "_") + "@" + top[6].split("/src/")[1] + ":" + top[9])
PY
)
  nloc=$(lizard "$wt/src" -x "*.css" 2>/dev/null | awk '/^Total nloc/{getline; getline; print $1}')
  # Prisma client must match the snapshot's schema before typechecking
  (cd "$wt" && PRISMA_QUERY_ENGINE_LIBRARY=/tmp/fake.so.node ./node_modules/.bin/prisma generate --schema prisma/schema.prisma >/dev/null 2>&1)
  (cd "$wt" && ./node_modules/.bin/tsc --noEmit > "$OUT/typecheck_$name.log" 2>&1); tc=$([ $? -eq 0 ] && echo pass || echo fail)
  if [ -d "$wt/tests" ]; then
    (cd "$wt" && ./node_modules/.bin/vitest run --reporter=verbose > "$OUT/tests_$name.log" 2>&1)
    passed=$(grep -oP 'Tests\s+\K[0-9]+(?= passed)' "$OUT/tests_$name.log" | tail -1); total=$(grep -oP 'Tests\s+.*\(\K[0-9]+(?=\))' "$OUT/tests_$name.log" | tail -1)
  else passed=0; total=0; echo "no test suite in this snapshot" > "$OUT/tests_$name.log"; fi
  echo "$name,$c,$files,$nloc,$fns,$avg,$max,$maxfn,$tc,${passed:-0},${total:-0}" >> "$OUT/metrics.csv"
done
# characterization tests written later, executed against the untouched baseline source
wt=/tmp/a12-baseline; cp "$REPO"/tests/{helpers.ts,characterization*.test.ts,subscription.test.ts} "$wt/tests/" 2>/dev/null || { mkdir -p "$wt/tests"; cp "$REPO"/tests/{helpers.ts,characterization*.test.ts,subscription.test.ts} "$wt/tests/"; }
cp "$REPO/vitest.config.mts" "$wt/"
git -C "$REPO" show d68c773:tests/helpers.ts > "$wt/tests/helpers.ts"   # fixture as it was before CH01
(cd "$wt" && ./node_modules/.bin/vitest run --reporter=verbose > "$OUT/tests_baseline_characterization.log" 2>&1)
# restore prisma client for the newest schema
(cd "$REPO" && PRISMA_QUERY_ENGINE_LIBRARY=/tmp/fake.so.node ./node_modules/.bin/prisma generate >/dev/null 2>&1)
cat "$OUT/metrics.csv"
