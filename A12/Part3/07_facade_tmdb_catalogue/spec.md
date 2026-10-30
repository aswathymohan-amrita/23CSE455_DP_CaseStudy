# 07 Facade - TMDB Catalogue Facade

Source instance: **TMDB Catalogue Facade** (`Part2/code/src/lib/fetchers.ts`, state after the CH02 refactoring).

Facade `TmdbCatalogue(http, apiKey="k")` with `getShows(mediaType)` and `getNewAndPopular()`.
Subsystem: URL building `https://api.themoviedb.org/3/<path>?api_key=k&<query>`, an `HttpClient`
(injected), response checking and premium tagging.

| getShows rows (in order) | path | query |
|---|---|---|
| trending | `trending/<m>/week` | `language=en-US` |
| topRated | `<m>/top_rated` | `language=en-US` |
| netflix (**premium**) | `discover/<m>` | `with_networks=213` |
| action, comedy, horror, romance, docs | `discover/<m>` | `with_genres=28, 35, 27, 10749, 99` |

getNewAndPopular rows: popularTvs `tv/popular`, popularMovies `movie/popular`,
trendingTvs `trending/tv/day`, trendingMovies `trending/movie/day` (all `language=en-US`).
`<m>` must be `movie` or `tv`.

**All requests of a call are issued, then all responses are checked** (as `Promise.all` + `some(!ok)`).

Test double (shared fixture rule): the HTTP client answers request n (1-based, per call) with
results `[n]`, and fails (`ok=false`) when the URL contains the given fragment.

## Input / output
`mode;failFragment` (`mode` = `movie`, `tv`, `newpopular`; fragment or `-`).
Output `<key>=<id>[P],...;requests=<n>` (`P` = premium) or `ERROR:<message>;requests=<n>`:
`Failed to fetch shows`, or `invalid media type` (no requests made).
