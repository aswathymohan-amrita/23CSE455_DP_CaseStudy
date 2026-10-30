/** CH01 acceptance tests: premium content + new Ultra subscription plan. */
import { afterEach, describe, expect, it, vi } from "vitest"

import { fakePrisma, mockFetch, session } from "./helpers"

vi.mock("@/server/db", () => ({ prisma: {} }))
vi.mock("@/server/auth", () => ({ getServerAuthSession: vi.fn() }))

afterEach(() => {
  vi.unstubAllGlobals()
})

const DAY = 86_400_000
const userWithPlan = (priceId: string | null) => ({
  stripeSubscriptionId: priceId ? "sub_1" : null,
  stripePriceId: priceId,
  stripeCustomerId: "cus_1",
  stripeCurrentPeriodEnd: new Date(Date.now() + 10 * DAY),
})

describe("plan catalogue (single source of truth)", () => {
  it("offers five plans including Ultra with 7 profiles", async () => {
    const { planCatalog } = await import("@/config/plan-catalog")
    expect(planCatalog.map((p) => p.name)).toEqual([
      "Mobile",
      "Basic",
      "Standard",
      "Premium",
      "Ultra",
    ])
    const ultra = planCatalog.at(-1)
    expect(ultra).toMatchObject({
      tier: 5,
      maxProfiles: 7,
      monthlyPrice: 12.99,
    })
  })

  it("UI and server plan lists cannot drift apart", async () => {
    vi.mock("@/components/icons", () => ({
      Icons: new Proxy({}, { get: () => () => null }),
    }))
    const { plansConfig } = await import("@/config/plans")
    const { subscriptionPlans } = await import("@/config/subscriptions")
    const ui = plansConfig.plans.map((p) => [
      p.name,
      p.price,
      p.resolution,
      p.devices.map((d) => d.title).join(", "),
    ])
    const server = subscriptionPlans.map((p) => [
      p.name,
      p.monthlyPrice,
      p.resolution,
      p.devices,
    ])
    expect(ui).toEqual(server)
  })
})

describe("Content Access Rule Chain - PremiumContentRule", () => {
  it.each([
    [0, false],
    [1, false],
    [2, false],
    [3, true],
    [4, true],
    [5, true],
  ])("premium title with plan tier %i -> allowed %s", async (tier, allowed) => {
    const { checkAccess } = await import("@/lib/access/policy")
    const d = checkAccess({ id: 1, isPremium: true }, { planTier: tier, region: "US" })
    expect(d.allowed).toBe(allowed)
    if (!d.allowed)
      expect(d).toMatchObject({
        reason: "PREMIUM_REQUIRED",
        visibility: "locked",
      })
  })

  it("regular titles are always allowed", async () => {
    const { checkAccess } = await import("@/lib/access/policy")
    expect(checkAccess({ id: 1 }, { planTier: 0, region: "US" }).allowed).toBe(true)
  })

  it("an empty chain allows everything", async () => {
    const { buildAccessChain, checkAccess } = await import(
      "@/lib/access/policy"
    )
    expect(
      checkAccess(
        { id: 1, isPremium: true },
        { planTier: 0, region: "US" },
        buildAccessChain([])
      )
    ).toEqual({ allowed: true })
  })
})

describe("tRPC: subscribedProcedure + catalogue.checkAccess", () => {
  it("locks a premium title for a Basic subscriber", async () => {
    const prisma = fakePrisma()
    prisma.user.findFirst.mockResolvedValue(userWithPlan("price_basic"))
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    const d = await caller.catalogue.checkAccess({ id: 7, isPremium: true })
    expect(d).toMatchObject({ allowed: false, reason: "PREMIUM_REQUIRED" })
  })

  it("allows a premium title for a Standard subscriber", async () => {
    const prisma = fakePrisma()
    prisma.user.findFirst.mockResolvedValue(userWithPlan("price_standard"))
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    expect(
      await caller.catalogue.checkAccess({ id: 7, isPremium: true })
    ).toEqual({ allowed: true })
  })

  it("still rejects anonymous callers first", async () => {
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: null,
      prisma: fakePrisma(),
    } as never)
    await expect(caller.catalogue.checkAccess({ id: 7 })).rejects.toMatchObject(
      { code: "UNAUTHORIZED" }
    )
  })
})

describe("profile limit follows the plan", () => {
  const existing = (n: number) =>
    Array.from({ length: n }, (_, i) => ({
      id: `p${i}`,
      name: `P${i}`,
      iconId: `i${i}`,
    }))

  it("Ultra accounts can create a 6th and 7th profile", async () => {
    const prisma = fakePrisma()
    prisma.user.findFirst.mockResolvedValue(userWithPlan("price_ultra"))
    prisma.profile.findMany.mockResolvedValue(existing(6))
    vi.stubEnv("STRIPE_ULTRA_PRICE_ID", "price_ultra")
    vi.resetModules()
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    await expect(
      caller.profile.create({ name: "Seven", iconId: "i9" })
    ).resolves.toMatchObject({ name: "Seven" })
    prisma.profile.findMany.mockResolvedValue(existing(7))
    await expect(
      caller.profile.create({ name: "Eight", iconId: "i8" })
    ).rejects.toThrow("You can only have 7 profiles")
    vi.unstubAllEnvs()
  })

  it("Standard accounts keep the limit of 5", async () => {
    const prisma = fakePrisma()
    prisma.user.findFirst.mockResolvedValue(userWithPlan("price_standard"))
    prisma.profile.findMany.mockResolvedValue(existing(5))
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    await expect(
      caller.profile.create({ name: "Six", iconId: "i9" })
    ).rejects.toThrow("You can only have 5 profiles")
  })
})

describe("TMDB facade tags premium titles", () => {
  it("marks only the originals row as premium", async () => {
    mockFetch()
    const { getShows } = await import("@/lib/fetchers")
    const rows = await getShows("movie")
    expect(rows.netflix?.every((s) => s.isPremium === true)).toBe(true)
    expect(rows.trending?.some((s) => s.isPremium)).toBe(false)
  })
})
