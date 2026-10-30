# 14 Error Boundary - Shows Segment and Root Global Error Boundaries

Source instances: **Shows Segment Error Boundary** (`app/(shows)/error.tsx` + `ErrorScreen`) and
**Root Global Error Boundary** (`app/global-error.tsx`), both wrapped by Next.js `ErrorBoundaryHandler`
(next@13.4.4 `dist/client/components/error-boundary.js:53-110`).

Tree: `GlobalBoundary( RootLayout[ header, ShowsBoundary( ShowsPage ) ] )`.
- A boundary catches errors thrown while rendering its children and renders its fallback instead;
  an error thrown by the fallback itself goes to the next boundary up.
- Shows fallback: `shows-error(<message>)`; global fallback: `global-error(<message>)`; normal: `root[header,page]`.
- Retry (`reset`) resets the boundary that is showing its fallback (global first); resetting a boundary
  remounts its subtree, so boundaries below it are reset too. Reset with no boundary in error does nothing.
- Every frame is a full render from the global boundary.
- Scripted failures `<component>:<n>` = the component throws on its first n renders:
  `page` ("Failed to fetch shows"), `layout` ("Root layout failed"), `fallback` (the shows fallback, "Fallback failed").

## Input / output
Input: `none` or `<component:n[,component:n]>` followed by `;reset` actions.
Output: the rendered frames joined by ` > ` (initial render, then one per effective reset).
