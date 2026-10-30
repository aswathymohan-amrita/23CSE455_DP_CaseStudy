"use strict"
// Composite: API Router Tree (appRouter with sub-routers and procedures, after CH01).

/** Leaf. */
const procedure = (type) => ({
  type,
  count: () => 1,
  resolve(parts) {
    return parts.length === 0 ? this : null
  },
  paths: (prefix) => [prefix],
  depth: () => 0,
})

/** Composite: a record of procedures and/or routers, like tRPC's createTRPCRouter({...}). */
const router = (record) => {
  const children = new Map(Object.entries(record))
  return {
    count: () => [...children.values()].reduce((n, c) => n + c.count(), 0),
    resolve(parts) {
      if (parts.length === 0) return this
      const child = children.get(parts[0])
      return child ? child.resolve(parts.slice(1)) : null
    },
    paths: (prefix) =>
      [...children].flatMap(([name, child]) => child.paths(prefix ? `${prefix}.${name}` : name)),
    depth: () => 1 + Math.max(-1, ...[...children.values()].map((c) => c.depth())),
  }
}

function appRouter() {
  const q = procedure("query")
  const m = procedure("mutation")
  return router({
    user: router({ getSession: q, getCurrent: q, getCurrentWithProfile: q, update: m }),
    profile: router({ getAll: q, getOthers: q, getOne: q, create: m, update: m, updatePin: m, delete: m }),
    icon: router({ getAll: q, getAllUsed: q, getAllUnused: q, getCurrent: q }),
    myList: router({ getAll: q, create: m, update: m, delete: m }),
    catalogue: router({ checkAccess: q }),
  })
}

module.exports = { procedure, router, appRouter }
