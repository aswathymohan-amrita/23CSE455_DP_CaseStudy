/** CH03 acceptance tests: parental control. */
import { describe, expect, it, vi } from "vitest"

import type { Maturity } from "@/config/maturity"
import type { AccessCheckedShow } from "@/lib/access/types"
import { fakePrisma, session } from "./helpers"

vi.mock("@/server/db", () => ({ prisma: {} }))
vi.mock("@/server/auth", () => ({ getServerAuthSession: vi.fn() }))

const HORROR = 27,
  THRILLER = 53,
  ANIMATION = 16,
  FAMILY = 10751

describe("MaturityRule", () => {
  const cases: [Maturity | undefined, Partial<AccessCheckedShow>, boolean][] = [
    ["KIDS", { genre_ids: [ANIMATION, FAMILY] }, true],
    ["KIDS", { genre_ids: [HORROR] }, false],
    ["KIDS", { genre_ids: [THRILLER] }, false],
    ["KIDS", { adult: true }, false],
    ["TEEN", { genre_ids: [THRILLER] }, true],
    ["TEEN", { genre_ids: [HORROR] }, false],
    ["TEEN", { adult: true }, false],
    ["ADULT", { genre_ids: [HORROR], adult: true }, true],
    [undefined, { genre_ids: [HORROR] }, true],
  ]
  it.each(cases)(
    "%s profile, %j -> allowed %s",
    async (maturity, signals, allowed) => {
      const { checkAccess } = await import("@/lib/access/policy")
      const d = checkAccess(
        { id: 1, ...signals },
        { planTier: 5, region: "US", maturity }
      )
      expect(d.allowed).toBe(allowed)
      if (!d.allowed)
        expect(d).toMatchObject({
          reason: "MATURITY_BLOCKED",
          visibility: "hidden",
        })
    }
  )

  it("chain order is region -> maturity -> premium", async () => {
    const { checkAccess } = await import("@/lib/access/policy")
    const horrorPremium = { id: 1, isPremium: true, genre_ids: [HORROR] }
    expect(
      checkAccess(horrorPremium, {
        planTier: 0,
        region: "US",
        maturity: "KIDS",
      })
    ).toMatchObject({ reason: "MATURITY_BLOCKED" })
    expect(
      checkAccess(
        { ...horrorPremium, id: 550 },
        { planTier: 0, region: "CN", maturity: "KIDS" }
      )
    ).toMatchObject({ reason: "REGION_BLOCKED" })
    expect(
      checkAccess(horrorPremium, {
        planTier: 0,
        region: "US",
        maturity: "ADULT",
      })
    ).toMatchObject({ reason: "PREMIUM_REQUIRED" })
  })

  it("profileVisibleShows filters rows for restricted profiles only", async () => {
    const { profileVisibleShows } = await import("@/lib/access/policy")
    const rows = [
      { id: 1, genre_ids: [HORROR] },
      { id: 2, genre_ids: [ANIMATION] },
      { id: 3, isPremium: true },
    ]
    expect(profileVisibleShows(rows, "ADULT")).toBe(rows)
    expect(profileVisibleShows(rows, undefined)).toBe(rows)
    expect(profileVisibleShows(rows, "KIDS").map((s) => s.id)).toEqual([2, 3])
  })
})

describe("catalogue.checkAccess with a profile", () => {
  async function caller(profile: unknown) {
    const prisma = fakePrisma()
    prisma.profile.findUnique.mockResolvedValue(profile)
    const { appRouter } = await import("@/server/api/root")
    return appRouter.createCaller({ session: session("u1"), prisma } as never)
  }

  it("applies the profile's maturity rating", async () => {
    const c = await caller({ userId: "u1", maturityLevel: "KIDS" })
    expect(
      await c.catalogue.checkAccess({
        id: 9,
        genre_ids: [HORROR],
        profileId: "kid",
      })
    ).toMatchObject({ allowed: false, reason: "MATURITY_BLOCKED" })
    expect(
      await c.catalogue.checkAccess({
        id: 9,
        genre_ids: [ANIMATION],
        profileId: "kid",
      })
    ).toEqual({ allowed: true })
  })

  it("refuses another account's profile", async () => {
    const c = await caller({ userId: "someone-else", maturityLevel: "ADULT" })
    await expect(
      c.catalogue.checkAccess({ id: 9, profileId: "p" })
    ).rejects.toMatchObject({ code: "FORBIDDEN" })
  })
})

describe("My List respects parental control", () => {
  const show = {
    id: 42,
    profileId: "kid",
    name: "N",
    title: "T",
    original_language: "en",
    media_type: "movie" as const,
    popularity: 1,
    vote_average: 7,
    vote_count: 3,
  }

  it("a Kids profile cannot save a horror title", async () => {
    const prisma = fakePrisma()
    prisma.profile.findUnique.mockResolvedValue({
      id: "kid",
      maturityLevel: "KIDS",
      myList: [],
    })
    const { appRouter } = await import("@/server/api/root")
    const c = appRouter.createCaller({ session: session(), prisma } as never)
    await expect(
      c.myList.create({ ...show, genre_ids: [HORROR] })
    ).rejects.toMatchObject({
      code: "FORBIDDEN",
      message: "This title is not available on this profile.",
    })
    expect(prisma.myShow.create).not.toHaveBeenCalled()
  })

  it("allowed titles are saved without the genre list", async () => {
    const prisma = fakePrisma()
    prisma.profile.findUnique.mockResolvedValue({
      id: "kid",
      maturityLevel: "KIDS",
      myList: [],
    })
    const { appRouter } = await import("@/server/api/root")
    const c = appRouter.createCaller({ session: session(), prisma } as never)
    await c.myList.create({ ...show, genre_ids: [ANIMATION] })
    const data = prisma.myShow.create.mock.calls[0]?.[0]?.data as Record<
      string,
      unknown
    >
    expect(data).not.toHaveProperty("genre_ids")
    expect(data).toMatchObject({ id: 42, profileId: "kid" })
  })
})

describe("profile.update stores the maturity level", () => {
  it("passes maturityLevel to the database", async () => {
    const prisma = fakePrisma()
    const { appRouter } = await import("@/server/api/root")
    const c = appRouter.createCaller({ session: session(), prisma } as never)
    await c.profile.update({
      id: "p1",
      name: "Kid",
      iconId: "i1",
      language: "ENGLISH",
      maturityLevel: "KIDS",
    })
    expect(prisma.profile.update.mock.calls[0]?.[0]).toMatchObject({
      data: { maturityLevel: "KIDS" },
    })
  })
})
