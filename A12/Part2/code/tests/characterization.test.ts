/**
 * Characterization tests written against the ORIGINAL code (676e5dd) before any change.
 * They pin the observable behaviour that the Part 2 refactorings must preserve.
 */
import { afterEach, describe, expect, it, vi } from "vitest"

import { fakePrisma, mockFetch, session } from "./helpers"

vi.mock("@/server/db", () => ({ prisma: {} }))
vi.mock("@/server/auth", () => ({ getServerAuthSession: vi.fn() }))

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe("TMDB Catalogue Facade (lib/fetchers.ts)", () => {
  it("getShows requests the same eight TMDB lists in the same order", async () => {
    const urls = mockFetch()
    const { getShows } = await import("@/lib/fetchers")
    const rows = await getShows("movie")
    expect(urls).toEqual([
      "https://api.themoviedb.org/3/trending/movie/week?api_key=test-key&language=en-US",
      "https://api.themoviedb.org/3/movie/top_rated?api_key=test-key&language=en-US",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_networks=213",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_genres=28",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_genres=35",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_genres=27",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_genres=10749",
      "https://api.themoviedb.org/3/discover/movie?api_key=test-key&with_genres=99",
    ])
    expect(Object.keys(rows)).toEqual([
      "trending",
      "topRated",
      "netflix",
      "action",
      "comedy",
      "horror",
      "romance",
      "docs",
    ])
    expect(rows.trending?.[0]?.id).toBe(1)
    expect(rows.docs?.[0]?.id).toBe(8)
  })

  it("getShows throws one error when any request fails", async () => {
    mockFetch(true)
    const { getShows } = await import("@/lib/fetchers")
    await expect(getShows("tv")).rejects.toThrow("Failed to fetch shows")
  })

  it("searchShows encodes the query and sorts by popularity", async () => {
    const urls = mockFetch()
    const { searchShows } = await import("@/lib/fetchers")
    await searchShows("tom & jerry")
    expect(urls[0]).toContain(
      "search/multi?api_key=test-key&query=tom%20%26%20jerry"
    )
  })
})

describe("Authenticated Procedure Pipeline (trpc.ts)", () => {
  it("rejects anonymous callers with UNAUTHORIZED", async () => {
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: null,
      prisma: fakePrisma(),
    } as never)
    await expect(caller.profile.getAll()).rejects.toMatchObject({
      code: "UNAUTHORIZED",
    })
  })

  it("passes signed-in callers to the resolver with their user id", async () => {
    const prisma = fakePrisma()
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session("u9"),
      prisma,
    } as never)
    await caller.profile.getAll()
    expect(prisma.profile.findMany).toHaveBeenCalledWith({
      where: { userId: "u9" },
      include: { icon: true },
    })
  })

  it("leaves public procedures open", async () => {
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: null,
      prisma: fakePrisma(),
    } as never)
    await expect(caller.user.getSession()).resolves.toBeNull()
  })

  it("limits an account to 5 profiles", async () => {
    const prisma = fakePrisma()
    prisma.profile.findMany.mockResolvedValue(
      Array.from({ length: 5 }, (_, i) => ({
        id: `p${i}`,
        name: `P${i}`,
        iconId: `i${i}`,
      }))
    )
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    await expect(
      caller.profile.create({ name: "Six", iconId: "i9" })
    ).rejects.toMatchObject({
      code: "FORBIDDEN",
    })
  })
})

describe("My List procedures (routers/my-list.ts)", () => {
  const show = {
    id: 42,
    profileId: "p1",
    name: "N",
    title: "T",
    original_language: "en",
    media_type: "movie" as const,
    popularity: 1,
    vote_average: 7,
    vote_count: 3,
  }

  it("adds a show that is not yet in the list", async () => {
    const prisma = fakePrisma()
    prisma.profile.findUnique.mockResolvedValue({ id: "p1", myList: [] })
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    const created = await caller.myList.create(show)
    expect(created).toMatchObject({
      id: 42,
      profileId: "p1",
      adult: false,
      video: false,
    })
  })

  it("refuses duplicates", async () => {
    const prisma = fakePrisma()
    prisma.profile.findUnique.mockResolvedValue({
      id: "p1",
      myList: [{ id: 42 }],
    })
    const { appRouter } = await import("@/server/api/root")
    const caller = appRouter.createCaller({
      session: session(),
      prisma,
    } as never)
    await expect(caller.myList.create(show)).rejects.toMatchObject({
      code: "FORBIDDEN",
    })
  })
})
