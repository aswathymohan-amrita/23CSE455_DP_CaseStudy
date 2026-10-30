# 16 Scatter-Gather - TMDB Row Scatter-Gather

Source instance: **TMDB Row Scatter-Gather** (`getShows` / `getNewAndPopularShows` at the baseline;
the generic `fetchRows` aggregator after the CH02 refactoring, `Part2/code/src/lib/fetchers.ts`).

- Scatter: one concurrent request per row, using each language's standard concurrency primitive
  (CompletableFuture, asyncio.gather, Promise.all, std::async). Latency is **simulated**: every
  recipient reports its `ms` instead of sleeping, so results are deterministic.
- Gather: wait for all replies; if any reply is not ok the whole result is the error
  `Failed to fetch shows` (all-or-nothing, as in the source); otherwise aggregate `key=<number of results>`
  in **request order**, regardless of completion order.
- `elapsed` = slowest reply (concurrent cost); `sequential` = sum of all latencies (what a loop of awaits would cost).
- No rows: `none`, elapsed 0.

## Input / output
Input: `<key:ms:ok|fail:count[,...]|->`.
Output: `<k=v,...|none|ERROR:Failed to fetch shows>;elapsed=<ms>;sequential=<ms>`.
