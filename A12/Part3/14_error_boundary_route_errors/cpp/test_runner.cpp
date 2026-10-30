// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "error_boundary.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auto p = split(input, ';');
    std::map<std::string, int> fails;
    if (p[0] != "none") {
        for (const auto& pair : split(p[0], ',')) {
            auto kv = split(pair, ':');
            fails[kv[0]] = std::stoi(kv[1]);
        }
    }
    boundary::App app(fails);
    std::string frames = app.root.render();
    for (std::size_t i = 1; i < p.size(); i++) {
        if (p[i] == "reset" && app.resetNearest()) frames += " > " + app.root.render();
    }
    return frames;
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
