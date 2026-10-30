import type { CategorizedShows, Show } from "@/types"

import { visibleShows } from "@/lib/access/policy"
import type { AccessContext } from "@/lib/access/types"
import type { NewAndPopularRowKey, ShowRowKey } from "@/lib/fetchers"

/*
 * CH02 refactoring (Duplicate Code): Home, Movies and TV pages each contained the same
 * 7-entry title/row array (the TV page even kept "Scary Movies"). The layout is now
 * declared once, and region filtering is applied in one place instead of three.
 */

export type RowLayout<K extends string> = { title: string; key: K }[]

export const GENRE_ROWS: RowLayout<ShowRowKey> = [
  { title: "Trending Now", key: "trending" },
  { title: "Top Rated", key: "topRated" },
  { title: "Action Thrillers", key: "action" },
  { title: "Comedies", key: "comedy" },
  { title: "Scary Movies", key: "horror" },
  { title: "Romance Movies", key: "romance" },
  { title: "Documentaries", key: "docs" },
]

export const NEW_AND_POPULAR_LAYOUT: RowLayout<NewAndPopularRowKey> = [
  { title: "New TV Shows", key: "trendingTvs" },
  { title: "New Movies", key: "trendingMovies" },
  { title: "Popular TV Shows", key: "popularTvs" },
  { title: "Popular Movies", key: "popularMovies" },
]

/**
 * Context used when building rows on the server. Rows only need to know what to
 * HIDE (region); premium titles stay visible and are locked per viewer by
 * catalogue.checkAccess, so the plan tier is not needed here.
 */
export function rowContext(region: string): AccessContext {
  return { planTier: 0, region }
}

export function toCategories<K extends string>(
  rows: Record<K, Show[] | undefined>,
  layout: RowLayout<K>,
  ctx: AccessContext
): CategorizedShows[] {
  return layout.map(({ title, key }) => {
    const shows = rows[key]
    return { title, shows: shows ? visibleShows(shows, ctx) : shows }
  })
}
