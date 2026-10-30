// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "suspense_boundary.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auto p = split(input, ' ');
    std::vector<suspense::Dependency> deps;
    if (p[1] != "-") {
        for (const auto& item : split(p[1], ',')) {
            auto nm = split(item, ':');
            bool fails = nm[1][0] == '!';
            deps.push_back({nm[0], std::stoi(fails ? nm[1].substr(1) : nm[1]), fails});
        }
    }
    auto root = suspense::segment(std::make_shared<suspense::AsyncPage>(deps), p[0] == "yes");
    std::string out;
    for (const auto& f : suspense::stream(*root, deps)) out += (out.empty() ? "" : " | ") + f;
    return out;
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
