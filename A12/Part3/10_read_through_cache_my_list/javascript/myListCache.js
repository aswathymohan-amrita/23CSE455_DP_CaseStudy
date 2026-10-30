"use strict"
// Read-Through Cache: My List Query Cache (React Query fetchQuery / invalidate shape).

/** Returns the cached value or loads it once (staleTime = Infinity). */
function createQueryCache() {
  const entries = new Map()
  return {
    fetch(key, loader) {
      if (!entries.has(key)) entries.set(key, loader())
      return entries.get(key)
    },
    invalidate: (key) => entries.delete(key),
  }
}

/** Data source behind the loader (myList router). */
function createMyListStore() {
  const lists = new Map()
  const store = {
    loads: 0,
    getAll(profileId) {
      store.loads++
      return [...(lists.get(profileId) ?? [])]
    },
    add(profileId, showId) {
      const list = lists.get(profileId) ?? []
      if (list.includes(showId)) throw new Error("Show already exists")
      lists.set(profileId, [...list, showId])
    },
    remove(profileId, showId) {
      const list = lists.get(profileId) ?? []
      if (!list.includes(showId)) throw new Error("Show not found")
      lists.set(profileId, list.filter((id) => id !== showId))
    },
  }
  return store
}

module.exports = { createQueryCache, createMyListStore }
