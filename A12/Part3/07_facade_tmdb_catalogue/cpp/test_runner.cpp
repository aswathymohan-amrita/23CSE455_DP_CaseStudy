// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "tmdb_catalogue.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

// Test double: request n answers [n]; fails when the URL contains the fragment.
class FakeHttp : public tmdb::HttpClient {
public:
    explicit FakeHttp(std::string fail) : fail_(std::move(fail)) {}
    tmdb::Response get(const std::string& url) override {
        requests++;
        return {fail_ == "-" || url.find(fail_) == std::string::npos, {requests}};
    }
    int requests = 0;

private:
    std::string fail_;
};

static std::string run(const std::string& input) {
    auto cut = input.find(';');
    std::string mode = input.substr(0, cut), fail = input.substr(cut + 1);
    FakeHttp http(fail);
    tmdb::TmdbCatalogue facade(http, "k");
    try {
        auto rows = mode == "newpopular" ? facade.getNewAndPopular() : facade.getShows(mode);
        std::string out;
        for (const auto& [key, shows] : rows)
            out += (out.empty() ? "" : ",") + key + "=" + std::to_string(shows[0].id) + (shows[0].premium ? "P" : "");
        return out + ";requests=" + std::to_string(http.requests);
    } catch (const std::exception& e) {
        return std::string("ERROR:") + e.what() + ";requests=" + std::to_string(http.requests);
    }
}

int main(int argc, char** argv) {
    std::ifstream in(argv[1]);
    std::string line;
    int passed = 0, total = 0;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto c = split(line, '\t');
        auto got = run(c[1]);
        total++;
        if (got == c[2]) passed++;
        else std::cout << "FAIL " << c[0] << " expected=" << c[2] << " got=" << got << "\n";
    }
    std::cout << passed << "/" << total << " passed\n";
    return passed == total ? 0 : 1;
}
