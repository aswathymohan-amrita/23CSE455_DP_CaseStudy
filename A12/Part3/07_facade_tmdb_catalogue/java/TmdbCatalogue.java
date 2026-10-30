import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Facade: TMDB Catalogue Facade (state after the CH02 refactoring). */
public final class TmdbCatalogue {
    /** Subsystem interface: HTTP access. */
    public interface HttpClient {
        Response get(String url);
    }

    public record Response(boolean ok, List<Integer> results) {}

    public record Show(int id, boolean premium) {}

    private record Row(String key, String path, String query, boolean premium) {}

    private static final String API = "https://api.themoviedb.org/3";

    private final HttpClient http;
    private final String apiKey;

    public TmdbCatalogue(HttpClient http, String apiKey) {
        this.http = http;
        this.apiKey = apiKey;
    }

    public Map<String, List<Show>> getShows(String m) {
        if (!m.equals("movie") && !m.equals("tv")) throw new IllegalArgumentException("invalid media type");
        return fetchRows(List.of(
                new Row("trending", "trending/" + m + "/week", "language=en-US", false),
                new Row("topRated", m + "/top_rated", "language=en-US", false),
                new Row("netflix", "discover/" + m, "with_networks=213", true),
                new Row("action", "discover/" + m, "with_genres=28", false),
                new Row("comedy", "discover/" + m, "with_genres=35", false),
                new Row("horror", "discover/" + m, "with_genres=27", false),
                new Row("romance", "discover/" + m, "with_genres=10749", false),
                new Row("docs", "discover/" + m, "with_genres=99", false)));
    }

    public Map<String, List<Show>> getNewAndPopular() {
        return fetchRows(List.of(
                new Row("popularTvs", "tv/popular", "language=en-US", false),
                new Row("popularMovies", "movie/popular", "language=en-US", false),
                new Row("trendingTvs", "trending/tv/day", "language=en-US", false),
                new Row("trendingMovies", "trending/movie/day", "language=en-US", false)));
    }

    private Map<String, List<Show>> fetchRows(List<Row> rows) {
        List<Response> responses = new ArrayList<>();
        for (Row row : rows) responses.add(http.get(API + "/" + row.path() + "?api_key=" + apiKey + "&" + row.query()));
        if (responses.stream().anyMatch(r -> !r.ok())) throw new IllegalStateException("Failed to fetch shows");
        Map<String, List<Show>> out = new LinkedHashMap<>();
        for (int i = 0; i < rows.size(); i++) {
            boolean premium = rows.get(i).premium();
            out.put(rows.get(i).key(), responses.get(i).results().stream().map(id -> new Show(id, premium)).toList());
        }
        return out;
    }
}
