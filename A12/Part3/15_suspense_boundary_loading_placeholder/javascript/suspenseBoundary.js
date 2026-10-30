"use strict"
// Suspense Boundary: Shows Loading Placeholder ((shows)/loading.tsx as the Suspense fallback of async pages).

/** Thrown by a child that is still waiting for data (React's suspend signal). */
class Pending extends Error {}
class FetchError extends Error {}

/** Async server page: awaits all its fetches (Promise.all) before it can render. */
class AsyncPage {
  constructor(deps) {
    this.deps = deps
  }
  render(t) {
    if (this.deps.some((d) => d.ms > t)) throw new Pending()
    const failed = this.deps.find((d) => d.fails)
    if (failed) throw new FetchError(failed.name)
    return `page(rows=${this.deps.length})`
  }
}

/** Renders the fallback while the child suspends; other errors pass through. */
class SuspenseBoundary {
  constructor(child, fallback) {
    this.child = child
    this.fallback = fallback
  }
  render(t) {
    try {
      return this.child.render(t)
    } catch (e) {
      if (e instanceof Pending) return this.fallback()
      throw e
    }
  }
}

/** Next.js LoadingBoundary: Suspense only if the segment has loading.tsx. */
const segment = (page, hasLoading) => (hasLoading ? new SuspenseBoundary(page, () => "loading") : page)

/** Server streaming: render at every point in time where something can change; emit changed frames. */
function stream(root, deps) {
  const frames = []
  let last = null
  const times = [...new Set([0, ...deps.map((d) => d.ms)])].sort((a, b) => a - b)
  for (const t of times) {
    let view
    try {
      view = root.render(t)
    } catch (e) {
      if (e instanceof Pending) continue // no boundary: nothing can be sent yet
      if (!(e instanceof FetchError)) throw e
      view = `error(${e.message})` // handled by the segment error boundary
    }
    if (view !== last) {
      frames.push(`t=${t}:${view}`)
      last = view
    }
    if (view !== "loading") break // final frame sent
  }
  return frames
}

module.exports = { AsyncPage, segment, stream }
