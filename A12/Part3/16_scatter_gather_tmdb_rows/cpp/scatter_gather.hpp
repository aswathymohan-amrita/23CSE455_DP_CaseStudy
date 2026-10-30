// Scatter-Gather: TMDB Row Scatter-Gather (Promise.all fan-out over row requests, all-or-nothing gather).
#pragma once
#include <algorithm>
#include <future>
#include <numeric>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace sg {

struct Row {
    std::string key;
    int ms;
    bool ok;
    int count;
};

struct Response {
    bool ok;
    int ms;
    std::vector<std::string> results;
};

struct Outcome {
    std::vector<std::pair<std::string, int>> rows;  // request order
    std::optional<std::string> error;
    int elapsed;
};

/** One TMDB endpoint; latency is simulated (reported, not slept). */
inline Response recipient(const Row& row) {
    return {row.ok, row.ms, std::vector<std::string>(row.count, "show")};
}

inline Outcome fetchRows(const std::vector<Row>& rows, const std::string& errorMessage) {
    std::vector<std::future<Response>> futures;  // scatter
    for (const auto& row : rows) futures.push_back(std::async(std::launch::async, recipient, row));
    std::vector<Response> responses;  // gather in request order
    for (auto& f : futures) responses.push_back(f.get());
    int elapsed = 0;  // concurrent: slowest reply
    for (const auto& r : responses) elapsed = std::max(elapsed, r.ms);
    if (std::any_of(responses.begin(), responses.end(), [](const Response& r) { return !r.ok; }))
        return {{}, errorMessage, elapsed};
    Outcome out{{}, std::nullopt, elapsed};
    for (std::size_t i = 0; i < rows.size(); i++)
        out.rows.emplace_back(rows[i].key, static_cast<int>(responses[i].results.size()));
    return out;
}

/** What the same requests would cost one after another. */
inline int sequentialCost(const std::vector<Row>& rows) {
    return std::accumulate(rows.begin(), rows.end(), 0, [](int s, const Row& r) { return s + r.ms; });
}

}  // namespace sg
