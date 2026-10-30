"use strict"
// Context Object: tRPC Request Context (createTRPCContext -> createInnerTRPCContext -> middleware refinement).

const DEFAULT_REGION = "US"
const REGION_HEADERS = ["x-vercel-ip-country", "cf-ipcountry"]
const DEFAULT_MAX_PROFILES = 5
const PLANS = new Map([
  ["u1", { name: "Premium", tier: 3, maxProfiles: 5 }],
  ["u2", { name: "Mobile", tier: 1, maxProfiles: 2 }],
]) // fake database

class TRPCError extends Error {
  constructor(code) {
    super(code)
    this.code = code
  }
}

function normaliseRegion(code) {
  const value = (code ?? "").trim().toUpperCase()
  return /^[A-Z]{2}$/.test(value) ? value : DEFAULT_REGION
}

function regionFromHeaders(headers) {
  for (const name of REGION_HEADERS) {
    if (headers[name]) return normaliseRegion(headers[name])
  }
  return normaliseRegion(null)
}

/** Protocol-independent context (also used by tests without HTTP). */
const createInnerContext = (session, region) => ({ session, db: PLANS, region: normaliseRegion(region) })

/** Per-request factory: extracts session and region from the HTTP request once. */
const createContext = (headers) => createInnerContext(headers.session ?? null, regionFromHeaders(headers))

const enforceUserIsAuthed = (ctx) => {
  if (!ctx.session) throw new TRPCError("UNAUTHORIZED")
  return { ...ctx, session: ctx.session } // narrowed copy, original untouched
}

const attachSubscription = (ctx) => {
  const plan = ctx.db.get(ctx.session)
  return {
    ...ctx,
    subscription: plan?.name ?? null,
    planTier: plan?.tier ?? 0,
    maxProfiles: plan?.maxProfiles ?? DEFAULT_MAX_PROFILES,
  }
}

const PROCEDURES = {
  whoami: [[enforceUserIsAuthed], (ctx) => ctx.session],
  region: [[], (ctx) => ctx.region],
  plan: [[enforceUserIsAuthed, attachSubscription], (ctx) => `tier=${ctx.planTier},max=${ctx.maxProfiles}`],
}

function call(name, ctx) {
  const [middlewares, resolver] = PROCEDURES[name]
  const finalCtx = middlewares.reduce((c, mw) => mw(c), ctx)
  return `${resolver(finalCtx)};keys=${Object.keys(finalCtx).sort().join(",")}`
}

module.exports = { TRPCError, call, createContext, createInnerContext }
