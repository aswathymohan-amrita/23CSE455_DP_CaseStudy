"""Facade: TMDB Catalogue Facade (state after the CH02 refactoring)."""
from __future__ import annotations

API = "https://api.themoviedb.org/3"


class TmdbCatalogue:
    """Facade over an injected HTTP client: http.get(url) -> (ok, results)."""

    def __init__(self, http, api_key: str) -> None:
        self._http = http
        self._key = api_key

    def get_shows(self, m: str) -> dict:
        if m not in ("movie", "tv"):
            raise ValueError("invalid media type")
        rows = [("trending", f"trending/{m}/week", "language=en-US", False),
                ("topRated", f"{m}/top_rated", "language=en-US", False),
                ("netflix", f"discover/{m}", "with_networks=213", True)]
        rows += [(key, f"discover/{m}", f"with_genres={genre}", False)
                 for key, genre in (("action", 28), ("comedy", 35), ("horror", 27), ("romance", 10749), ("docs", 99))]
        return self._fetch_rows(rows)

    def get_new_and_popular(self) -> dict:
        return self._fetch_rows([(key, path, "language=en-US", False) for key, path in (
            ("popularTvs", "tv/popular"), ("popularMovies", "movie/popular"),
            ("trendingTvs", "trending/tv/day"), ("trendingMovies", "trending/movie/day"))])

    def _fetch_rows(self, rows: list) -> dict:
        responses = [self._http.get(f"{API}/{path}?api_key={self._key}&{query}") for _, path, query, _ in rows]
        if any(not ok for ok, _ in responses):
            raise RuntimeError("Failed to fetch shows")
        return {key: [(show_id, premium) for show_id in results]
                for (key, _, _, premium), (_, results) in zip(rows, responses)}
