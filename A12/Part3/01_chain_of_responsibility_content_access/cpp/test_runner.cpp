// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "content_access.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auto f = split(input, ';');
    access::Show show{std::stoi(f[0]), f[1] == "1", f[2] == "1", {}};
    if (f[3] != "-")
        for (auto& g : split(f[3], ',')) show.genres.insert(std::stoi(g));
    access::Viewer viewer{std::stoi(f[4]), f[5], f[6]};
    try {
        return access::contentAccessChain()->check(show, viewer).str();
    } catch (const std::invalid_argument& e) {
        return std::string("ERROR:") + e.what();
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
