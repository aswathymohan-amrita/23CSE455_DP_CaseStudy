"use strict"
// Builder: tRPC Procedure Builder (immutable fluent builder; query()/mutation() build the product).

class TRPCError extends Error {
  constructor(code, trace = []) {
    super(code)
    this.code = code
    this.trace = trace // middlewares that ran before the call stopped
  }
}

/** Product: a frozen definition that can be called. */
class Procedure {
  constructor(kind, middlewares, resolver) {
    this.kind = kind
    this.middlewares = middlewares
    this.resolver = resolver
    Object.freeze(this)
  }

  call(user, input) {
    const ctx = { user, input }
    const trace = []
    for (const [name, mw] of this.middlewares) {
      trace.push(name)
      try {
        mw(ctx)
      } catch (e) {
        e.trace = trace
        throw e
      }
    }
    return { result: `${this.kind}:${this.resolver(ctx)}`, trace }
  }
}

/** Every step returns a NEW builder; the receiver is never changed (like createNewBuilder). */
class ProcedureBuilder {
  constructor(middlewares = []) {
    this.middlewares = Object.freeze([...middlewares])
  }
  use(name, mw) {
    return new ProcedureBuilder([...this.middlewares, [name, mw]])
  }
  input(parser) {
    return this.use("input", parser)
  }
  query(resolver) {
    return new Procedure("query", this.middlewares, resolver)
  }
  mutation(resolver) {
    return new Procedure("mutation", this.middlewares, resolver)
  }
}

const enforceUserIsAuthed = (ctx) => {
  if (ctx.user === null) throw new TRPCError("UNAUTHORIZED")
}
const stringInput = (ctx) => {
  if (ctx.input === null) throw new TRPCError("BAD_REQUEST")
}
const numberInput = (ctx) => {
  if (ctx.input === null || !/^-?\d+$/.test(ctx.input)) throw new TRPCError("BAD_REQUEST")
  ctx.input = String(parseInt(ctx.input, 10))
}
const noOp = () => {}

const publicProcedure = new ProcedureBuilder() // t.procedure
const protectedProcedure = publicProcedure.use("auth", enforceUserIsAuthed)
const RESOLVERS = {
  echo: (ctx) => ctx.input ?? "none",
  whoami: (ctx) => ctx.user ?? "anonymous",
}
const STEPS = {
  "use:log": (b) => b.use("log", noOp),
  "use:timing": (b) => b.use("timing", noOp),
  "input:string": (b) => b.input(stringInput),
  "input:number": (b) => b.input(numberInput),
}

/** Director: applies the step names in order to a base builder. */
function build(steps) {
  let current = { public: publicProcedure, protected: protectedProcedure }[steps[0]]
  for (const step of steps.slice(1)) {
    if (current instanceof Procedure) throw new TRPCError("ALREADY_BUILT")
    const [kind, name] = step.split(":")
    current = kind === "query" || kind === "mutation" ? current[kind](RESOLVERS[name]) : STEPS[step](current)
  }
  if (!(current instanceof Procedure)) throw new TRPCError("NOT_BUILT")
  return current
}

module.exports = { TRPCError, build, noOp, publicProcedure, protectedProcedure }
