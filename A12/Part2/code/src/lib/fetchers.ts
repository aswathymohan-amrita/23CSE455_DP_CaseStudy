import { env } from "@/env.mjs"
import type { Show } from "@/types"
import type { MEDIA_TYPE } from "@prisma/client"

/*
 * TMDB Catalogue Facade.
 *
 * CH02 refactoring (Duplicate Code / Long Method): getShows and
 * getNewAndPopularShows each repeated one fetch call, one `!res.ok` term, one
 * `.json()` and one return field per row (8 + 4 copies). Rows are now data
 * (ROW_SPECS) and one helper fetches any list of rows. Public signatures, request
 * URLs, their order, result keys and error messages are unchanged (pinned by
 * tests/characterization.test.ts).
 */

const TMDB_API = "https://api.themoviedb.org/3"

type RowRequest<K extends string> = {
  key: K
  url: string
  /** CH01: rows whose titles need a premium plan */
  premium?: boolean
}

function tmdbUrl(path: string, query: string) {
  return `${TMDB_API}/${path}?api_key=${env.NEXT_PUBLIC_TMDB_API_KEY}&${query}`
}

async function fetchRows<K extends string>(
  rows: RowRequest<K>[],
  errorMessage: string
): Promise<Record<K, Show[] | undefined>> {
  const responses = await Promise.all(rows.map((row) => fetch(row.url)))
  if (responses.some((res) => !res.ok)) {
    throw new Error(errorMessage)
  }
  const bodies = (await Promise.all(responses.map((res) => res.json()))) as {
    results: Show[]
  }[]
  return Object.fromEntries(
    rows.map((row, i) => {
      const results = bodies[i]?.results
      return [
        row.key,
        row.premium
          ? results?.map((show) => ({ ...show, isPremium: true }))
          : results,
      ]
    })
  ) as Record<K, Show[] | undefined>
}

const SHOW_ROWS = [
  {
    key: "trending",
    path: (m: MEDIA_TYPE) => `trending/${m}/week`,
    query: "language=en-US",
  },
  {
    key: "topRated",
    path: (m: MEDIA_TYPE) => `${m}/top_rated`,
    query: "language=en-US",
  },
  // originals (TMDB network 213) are premium titles (CH01)
  {
    key: "netflix",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_networks=213",
    premium: true,
  },
  {
    key: "action",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_genres=28",
  },
  {
    key: "comedy",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_genres=35",
  },
  {
    key: "horror",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_genres=27",
  },
  {
    key: "romance",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_genres=10749",
  },
  {
    key: "docs",
    path: (m: MEDIA_TYPE) => `discover/${m}`,
    query: "with_genres=99",
  },
] as const

export type ShowRowKey = (typeof SHOW_ROWS)[number]["key"]

export async function getShows(mediaType: MEDIA_TYPE) {
  return fetchRows<ShowRowKey>(
    SHOW_ROWS.map((row) => ({
      key: row.key,
      url: tmdbUrl(row.path(mediaType), row.query),
      premium: "premium" in row ? row.premium : undefined,
    })),
    "Failed to fetch shows"
  )
}

// The latest endpiont doesn't seem to work.
// API endpoint url: https://api.themoviedb.org/3/movie/latest?api_key=<<api_key>>&language=en-US.
// So taking trending for the day as new shows.
const NEW_AND_POPULAR_ROWS = [
  { key: "popularTvs", path: "tv/popular" },
  { key: "popularMovies", path: "movie/popular" },
  { key: "trendingTvs", path: "trending/tv/day" },
  { key: "trendingMovies", path: "trending/movie/day" },
] as const

export type NewAndPopularRowKey = (typeof NEW_AND_POPULAR_ROWS)[number]["key"]

export async function getNewAndPopularShows() {
  return fetchRows<NewAndPopularRowKey>(
    NEW_AND_POPULAR_ROWS.map((row) => ({
      key: row.key,
      url: tmdbUrl(row.path, "language=en-US"),
    })),
    "Failed to fetch shows"
  )
}

export async function searchShows(query: string) {
  const res = await fetch(
    `https://api.themoviedb.org/3/search/multi?api_key=${
      env.NEXT_PUBLIC_TMDB_API_KEY
    }&query=${encodeURIComponent(query)}`
  )

  if (!res.ok) {
    throw new Error("Failed to find shows")
  }

  const shows = (await res.json()) as { results: Show[] }

  const popularShows = shows.results.sort((a, b) => b.popularity - a.popularity)

  return {
    results: popularShows,
  }
}
