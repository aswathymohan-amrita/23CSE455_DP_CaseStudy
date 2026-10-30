// Facade: TMDB Catalogue Facade (state after the CH02 refactoring).
#pragma once
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace tmdb {

struct Response {
    bool ok;
    std::vector<int> results;
};

// Subsystem interface: HTTP access.
class HttpClient {
public:
    virtual ~HttpClient() = default;
    virtual Response get(const std::string& url) = 0;
};

struct Show {
    int id;
    bool premium;
};

using Rows = std::vector<std::pair<std::string, std::vector<Show>>>;

class TmdbCatalogue {
public:
    TmdbCatalogue(HttpClient& http, std::string apiKey) : http_(http), key_(std::move(apiKey)) {}

    Rows getShows(const std::string& m) {
        if (m != "movie" && m != "tv") throw std::invalid_argument("invalid media type");
        std::vector<Row> rows{{"trending", "trending/" + m + "/week", "language=en-US", false},
                              {"topRated", m + "/top_rated", "language=en-US", false},
                              {"netflix", "discover/" + m, "with_networks=213", true}};
        const std::vector<std::pair<std::string, int>> genres{
            {"action", 28}, {"comedy", 35}, {"horror", 27}, {"romance", 10749}, {"docs", 99}};
        for (const auto& [key, genre] : genres)
            rows.push_back({key, "discover/" + m, "with_genres=" + std::to_string(genre), false});
        return fetchRows(rows);
    }

    Rows getNewAndPopular() {
        return fetchRows({{"popularTvs", "tv/popular", "language=en-US", false},
                          {"popularMovies", "movie/popular", "language=en-US", false},
                          {"trendingTvs", "trending/tv/day", "language=en-US", false},
                          {"trendingMovies", "trending/movie/day", "language=en-US", false}});
    }

private:
    struct Row {
        std::string key, path, query;
        bool premium;
    };

    Rows fetchRows(const std::vector<Row>& rows) {
        std::vector<Response> responses;
        for (const auto& r : rows)
            responses.push_back(http_.get("https://api.themoviedb.org/3/" + r.path + "?api_key=" + key_ + "&" + r.query));
        for (const auto& res : responses)
            if (!res.ok) throw std::runtime_error("Failed to fetch shows");
        Rows out;
        for (size_t i = 0; i < rows.size(); i++) {
            std::vector<Show> shows;
            for (int id : responses[i].results) shows.push_back({id, rows[i].premium});
            out.emplace_back(rows[i].key, shows);
        }
        return out;
    }

    HttpClient& http_;
    std::string key_;
};

}  // namespace tmdb
