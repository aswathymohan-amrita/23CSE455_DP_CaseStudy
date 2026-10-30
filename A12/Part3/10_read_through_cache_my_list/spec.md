# 10 Read-Through Cache - My List Query Cache

Source instance: **My List Query Cache** (React Query `QueryClient` with `staleTime: Infinity`,
readers `ShowsContainer` / `ShowModal`, invalidation after mutations, loader `myList.getAll`).

`QueryCache.fetch(key, loader)` returns the cached value for `key`; on a miss (or after
`invalidate(key)`) it calls `loader()` once, stores and returns the result. Entries never become
stale on their own. The loader reads a backend `MyListStore` (profile -> ordered list of show ids)
whose `add` / `remove` follow `myList.create` / `myList.delete`: duplicate add -> `Show already exists`,
removing a missing show -> `Show not found`. Mutations do **not** update the cache by themselves.

## Input
Commands separated by `;`: `get <profile>`, `add <profile> <id>`, `remove <profile> <id>`, `invalidate <profile>`.

## Output
One entry per `get` (`<profile>=[id,id,...]`) and per failing mutation (`ERROR:<message>`),
then `loads=<loader calls>`, all joined by `|`.
