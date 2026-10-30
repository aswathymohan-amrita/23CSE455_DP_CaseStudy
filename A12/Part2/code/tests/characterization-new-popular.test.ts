/** Characterization of getNewAndPopularShows; verified against 676e5dd before CH02. */
import { afterEach, describe, expect, it, vi } from "vitest"

import { mockFetch } from "./helpers"

afterEach(() => {
  vi.unstubAllGlobals()
})

describe("getNewAndPopularShows", () => {
  it("requests the four lists in the same order and keys", async () => {
    const urls = mockFetch()
    const { getNewAndPopularShows } = await import("@/lib/fetchers")
    const rows = await getNewAndPopularShows()
    expect(urls).toEqual([
      "https://api.themoviedb.org/3/tv/popular?api_key=test-key&language=en-US",
      "https://api.themoviedb.org/3/movie/popular?api_key=test-key&language=en-US",
      "https://api.themoviedb.org/3/trending/tv/day?api_key=test-key&language=en-US",
      "https://api.themoviedb.org/3/trending/movie/day?api_key=test-key&language=en-US",
    ])
    expect(Object.keys(rows)).toEqual([
      "popularTvs",
      "popularMovies",
      "trendingTvs",
      "trendingMovies",
    ])
    expect(rows.trendingMovies?.[0]?.id).toBe(4)
  })

  it("throws one error when any request fails", async () => {
    mockFetch(true)
    const { getNewAndPopularShows } = await import("@/lib/fetchers")
    await expect(getNewAndPopularShows()).rejects.toThrow(
      "Failed to fetch shows"
    )
  })
})
