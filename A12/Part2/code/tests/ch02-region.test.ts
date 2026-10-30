/** CH02 acceptance tests: regional restrictions. */
import { describe, expect, it, vi } from "vitest"

import { fakePrisma, session } from "./helpers"

vi.mock("@/server/db", () => ({ prisma: {} }))
vi.mock("@/server/auth", () => ({
  getServerAuthSession: vi.fn().mockResolvedValue(null),
}))

const FIGHT_CLUB = 550 // blocked in CN
const GOT = 1399 // only US, GB, IN

describe("region resolution", () => {
  it("normalises codes and falls back to US", async () => {
    const { normaliseRegion } = await import("@/config/regions")
    expect(normaliseRegion(" in ")).toBe("IN")
    expect(normaliseRegion("xx1")).toBe("US")
    expect(normaliseRegion(undefined)).toBe("US")
  })

  it("prefers the Vercel header over Cloudflare", async () => {
    const { regionFromHeaders } = await import("@/lib/region")
    const h: Record<string, string> = {
      "x-vercel-ip-country": "gb",
      "cf-ipcountry": "DE",
    }
    expect(regionFromHeaders((n) => h[n])).toBe("GB")
    expect(regionFromHeaders((n) => (n === "cf-ipcountry" ? "DE" : null))).toBe(
      "DE"
    )
  })

  it("tRPC context reads the viewer's country from the request", async () => {
    const { createTRPCContext } = await import("@/server/api/trpc")
    const ctx = await createTRPCContext({
      req: { headers: { "x-vercel-ip-country": "in" } },
      res: {},
    } as never)
    expect(ctx.region).toBe("IN")
  })
})

describe("RegionRule in the Content Access Rule Chain", () => {
  it.each([
    [FIGHT_CLUB, "CN", false],
    [FIGHT_CLUB, "US", true],
    [GOT, "IN", true],
    [GOT, "DE", false],
    [12345, "CN", true],
  ])("title %i in %s -> allowed %s", async (id, region, allowed) => {
    const { checkAccess } = await import("@/lib/access/policy")
    const d = checkAccess({ id }, { planTier: 5, region })
    expect(d.allowed).toBe(allowed)
    if (!d.allowed)
      expect(d).toMatchObject({
        reason: "REGION_BLOCKED",
        visibility: "hidden",
      })
  })

  it("region runs before premium: a blocked premium title is hidden, not upsold", async () => {
    const { checkAccess } = await import("@/lib/access/policy")
    const d = checkAccess(
      { id: FIGHT_CLUB, isPremium: true },
      { planTier: 0, region: "CN" }
    )
    expect(d).toMatchObject({ allowed: false, reason: "REGION_BLOCKED" })
  })

  it("visibleShows keeps locked titles but drops hidden ones", async () => {
    const { visibleShows } = await import("@/lib/access/policy")
    const shows = [{ id: FIGHT_CLUB }, { id: 2, isPremium: true }, { id: 3 }]
    expect(
      visibleShows(shows, { planTier: 0, region: "CN" }).map((s) => s.id)
    ).toEqual([2, 3])
    expect(
      visibleShows(shows, { planTier: 0, region: "US" }).map((s) => s.id)
    ).toEqual([FIGHT_CLUB, 2, 3])
  })
})

describe("shared row layout", () => {
  it("keeps the exact baseline titles and order", async () => {
    const { GENRE_ROWS, NEW_AND_POPULAR_LAYOUT } = await import(
      "@/lib/catalogue"
    )
    expect(GENRE_ROWS.map((r) => r.title)).toEqual([
      "Trending Now",
      "Top Rated",
      "Action Thrillers",
      "Comedies",
      "Scary Movies",
      "Romance Movies",
      "Documentaries",
    ])
    expect(NEW_AND_POPULAR_LAYOUT.map((r) => r.title)).toEqual([
      "New TV Shows",
      "New Movies",
      "Popular TV Shows",
      "Popular Movies",
    ])
  })

  it("filters every row for the viewer's region", async () => {
    const { GENRE_ROWS, rowContext, toCategories } = await import(
      "@/lib/catalogue"
    )
    const rows = {
      trending: [{ id: FIGHT_CLUB }, { id: 1 }],
      topRated: [{ id: GOT }],
      action: undefined,
      comedy: [],
      horror: [],
      romance: [],
      docs: [],
      netflix: [],
    } as never
    const cn = toCategories(rows, GENRE_ROWS, rowContext("CN"))
    expect(cn[0]?.shows?.map((s) => s.id)).toEqual([1])
    expect(cn[1]?.shows).toEqual([])
    expect(cn[2]?.shows).toBeUndefined()
  })
})

describe("catalogue.checkAccess uses the request region", () => {
  it("denies a region-blocked title", async () => {
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma: fakePrisma(),
      region: "CN",
    } as never)
    expect(
      await caller.catalogue.checkAccess({ id: FIGHT_CLUB })
    ).toMatchObject({ reason: "REGION_BLOCKED" })
  })

  it("defaults to US when no region is known", async () => {
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma: fakePrisma(),
    } as never)
    expect(await caller.catalogue.checkAccess({ id: FIGHT_CLUB })).toEqual({
      allowed: true,
    })
  })
})
