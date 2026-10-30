"use strict"
// Front Controller: tRPC API Front Controller (/api/trpc/[trpc] -> createNextApiHandler -> appRouter).

class TRPCError extends Error {
  constructor(code) {
    super(code)
    this.code = code
  }
}

/** A command registered in the router. */
const procedure = (resolver, { isProtected = true, needsInput = false } = {}) => ({
  resolver,
  isProtected,
  needsInput,
})

/** Command registry: dotted procedure path -> procedure (state after CH01). */
function appRouter() {
  return new Map([
    ["user.getCurrent", procedure((ctx) => `user(${ctx.user})`)],
    ["profile.getAll", procedure((ctx) => `profiles(${ctx.user})`)],
    ["profile.getOne", procedure((ctx, v) => `profile(${v})`, { needsInput: true })],
    ["icon.getAll", procedure(() => "icons", { isProtected: false })],
    [
      "myList.getAll",
      procedure(
        (ctx, v) => {
          if (v === "boom") throw new Error("database unavailable")
          return `list(${v})`
        },
        { needsInput: true }
      ),
    ],
    ["catalogue.checkAccess", procedure((ctx, v) => `access(${v})`, { needsInput: true })],
  ])
}

/** Single entry point: shared context creation, dispatch by path, one error policy. */
class FrontController {
  constructor(router, createContext, onError) {
    this.router = router
    this.createContext = createContext
    this.onError = onError
  }

  handle(user, path) {
    if (path === null) return ["ERROR:INTERNAL_SERVER_ERROR"] // no [trpc] segment: nothing dispatched
    const ctx = this.createContext(user) // once per HTTP request, shared by a batch
    return path.split(",").map((call) => this.dispatch(call, ctx))
  }

  dispatch(call, ctx) {
    const [name, value = ""] = call.split("=")
    try {
      const proc = this.router.get(name)
      if (!proc) throw new TRPCError("NOT_FOUND")
      if (proc.isProtected && ctx.user === null) throw new TRPCError("UNAUTHORIZED")
      if (proc.needsInput && !value) throw new TRPCError("BAD_REQUEST")
      return "OK:" + proc.resolver(ctx, value || null)
    } catch (e) {
      const code = e instanceof TRPCError ? e.code : "INTERNAL_SERVER_ERROR"
      this.onError(name, code)
      return "ERROR:" + code
    }
  }
}

module.exports = { FrontController, appRouter, TRPCError }
