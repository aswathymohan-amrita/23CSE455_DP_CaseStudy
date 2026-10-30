"use strict"
// Error Boundary: Shows Segment Error Boundary + Root Global Error Boundary (error.tsx / global-error.tsx).

class RenderError extends Error {}

/** A component that throws for its first `fails` renders. */
class Flaky {
  constructor(fails, message, view) {
    Object.assign(this, { fails, message, view, renders: 0 })
  }
  render() {
    this.renders++
    if (this.renders <= this.fails) throw new RenderError(this.message)
    return this.view()
  }
}

/** Catches errors thrown by its children; errors thrown by its own fallback propagate upwards. */
class ErrorBoundary {
  constructor(child, fallback) {
    Object.assign(this, { child, fallback, error: null })
  }
  render() {
    if (this.error === null) {
      try {
        return this.child.render()
      } catch (e) {
        if (!(e instanceof RenderError)) throw e
        this.error = e
      }
    }
    return this.fallback(this.error).render()
  }
  reset() {
    this.error = null
  }
}

/** global boundary > RootLayout[header, shows boundary > page]. */
function buildApp(fails) {
  const page = new Flaky(fails.page ?? 0, "Failed to fetch shows", () => "page")
  const fallbackFails = new Flaky(fails.fallback ?? 0, "Fallback failed", () => "")
  const shows = new ErrorBoundary(page, (e) =>
    new Flaky(0, "", () => {
      fallbackFails.render() // may throw -> caught by the global boundary
      return `shows-error(${e.message})`
    })
  )
  const layout = new Flaky(fails.layout ?? 0, "Root layout failed", () => `root[header,${shows.render()}]`)
  const root = new ErrorBoundary(layout, (e) => new Flaky(0, "", () => `global-error(${e.message})`))
  return { root, shows }
}

/** Retry button: resets the boundary showing its fallback; a reset remounts everything below it. */
function resetNearest({ root, shows }) {
  if (root.error !== null) {
    root.reset()
    shows.reset()
    return true
  }
  if (shows.error !== null) {
    shows.reset()
    return true
  }
  return false
}

module.exports = { buildApp, resetNearest }
