# 08 Composite - API Router Tree

Source instance: **API Router Tree** (`appRouter` and its sub-routers, state after CH01).

Component `Node` with `count()` (number of procedures below), `resolve(path)`, `paths(prefix)`, `depth()`.
Leaf `Procedure(type)` (`query` or `mutation`); Composite `Router(children, ordered)`.

Tree (fixed, in this order):
- user: getSession, getCurrent, getCurrentWithProfile (query); update (mutation)
- profile: getAll, getOthers, getOne (query); create, update, updatePin, delete (mutation)
- icon: getAll, getAllUsed, getAllUnused, getCurrent (query)
- myList: getAll (query); create, update, delete (mutation)
- catalogue: checkAccess (query)

## Input / output
| command | output |
|---|---|
| `count` / `count <router>` | number of procedures in the whole tree / below that router |
| `resolve <dotted.path>` | `query`, `mutation`, `router(<n>)` for a router with n procedures, or `NOT_FOUND` |
| `paths <router>` | comma list of full procedure paths below it, in tree order |
| `depth` | longest root-to-leaf path in edges below the root |
