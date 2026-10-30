"use strict"
// Facade: TMDB Catalogue Facade (state after the CH02 refactoring), async like the source.

const API = "https://api.themoviedb.org/3"

const showRows = (m) => [
  { key: "trending", path: `trending/${m}/week`, query: "language=en-US" },
  { key: "topRated", path: `${m}/top_rated`, query: "language=en-US" },
  { key: "netflix", path: `discover/${m}`, query: "with_networks=213", premium: true },
  ...[["action", 28], ["comedy", 35], ["horror", 27], ["romance", 10749], ["docs", 99]].map(
    ([key, genre]) => ({ key, path: `discover/${m}`, query: `with_genres=${genre}` })
  ),
]

const NEW_AND_POPULAR = [
  ["popularTvs", "tv/popular"],
  ["popularMovies", "movie/popular"],
  ["trendingTvs", "trending/tv/day"],
  ["trendingMovies", "trending/movie/day"],
].map(([key, path]) => ({ key, path, query: "language=en-US" }))

/** Facade over an injected fetch-like client: http(url) -> Promise<{ok, json()}>. */
function createTmdbCatalogue(http, apiKey) {
  async function fetchRows(rows) {
    const responses = await Promise.all(rows.map((r) => http(`${API}/${r.path}?api_key=${apiKey}&${r.query}`)))
    if (responses.some((res) => !res.ok)) throw new Error("Failed to fetch shows")
    const bodies = await Promise.all(responses.map((res) => res.json()))
    return Object.fromEntries(
      rows.map((r, i) => [r.key, bodies[i].results.map((id) => ({ id, premium: !!r.premium }))])
    )
  }
  return {
    async getShows(m) {
      if (m !== "movie" && m !== "tv") throw new Error("invalid media type")
      return fetchRows(showRows(m))
    },
    getNewAndPopular: () => fetchRows(NEW_AND_POPULAR),
  }
}

module.exports = { createTmdbCatalogue }
