# 15 Suspense Boundary - Shows Loading Placeholder

Source instance: **Shows Loading Placeholder** (`app/(shows)/loading.tsx` used by Next.js `LoadingBoundary`
as `<Suspense fallback>`, next@13.4.4 `dist/client/components/layout-router.js:335-345`, around async
server pages such as `Home` that await TMDB).

- The page depends on N fetches, each finishing at `ms` (optionally failing, `!ms`). Like `Promise.all`,
  it can render only when **all** have finished; before that it *suspends* (throws `Pending`).
  When all are finished and one failed, it throws a fetch error naming the first failed dependency.
- With `loading.tsx` (`yes`) the segment is wrapped in a Suspense boundary whose fallback is `loading`;
  without it (`no`) nothing can be streamed while the page is pending.
- Streaming renders at t = 0 and at every dependency time, emits a frame `t=<ms>:<view>` only when the
  view changes, and stops after the first non-`loading` frame. Errors become `error(<name>)`
  (handled by the segment error boundary, problem 14).
- A page without dependencies never suspends, so the fallback is never shown (this is why the explicit
  `<Suspense>` wrappers around client components were rejected in Part 1).

## Input / output
Input: `<yes|no> <name:ms[,name:!ms...]|->`. Output: frames joined by ` | `.
