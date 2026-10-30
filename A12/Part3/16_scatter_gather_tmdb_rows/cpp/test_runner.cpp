// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "scatter_gather.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    std::vector<sg::Row> rows;
    if (input != "-") {
        for (const auto& item : split(input, ',')) {
            auto f = split(item, ':');
            rows.push_back({f[0], std::stoi(f[1]), f[2] == "ok", std::stoi(f[3])});
        }
    }
    auto out = sg::fetchRows(rows, "Failed to fetch shows");
    std::string head;
    if (out.error) head = "ERROR:" + *out.error;
    else {
        for (const auto& [k, v] : out.rows) head += (head.empty() ? "" : ",") + k + "=" + std::to_string(v);
        if (head.empty()) head = "none";
    }
    return head + ";elapsed=" + std::to_string(out.elapsed) + ";sequential=" + std::to_string(sg::sequentialCost(rows));
}

int main(int argc, char** argv) {
    std::ifstream in(argv[1]);
    std::string line;
    int passed = 0, total = 0;
    while (std::getline(in, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
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
