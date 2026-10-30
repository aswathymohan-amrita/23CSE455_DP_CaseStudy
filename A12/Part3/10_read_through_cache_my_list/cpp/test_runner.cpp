// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "my_list_cache.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    mylist::QueryCache<std::vector<int>> cache;
    mylist::MyListStore store;
    std::vector<std::string> out;
    for (auto& cmd : split(input, ';')) {
        auto p = split(cmd, ' ');
        try {
            if (p[0] == "get") {
                const auto& ids = cache.fetch(p[1], [&] { return store.getAll(p[1]); });
                std::string s = p[1] + "=[";
                for (size_t i = 0; i < ids.size(); i++) s += (i ? "," : "") + std::to_string(ids[i]);
                out.push_back(s + "]");
            } else if (p[0] == "add") store.add(p[1], std::stoi(p[2]));
            else if (p[0] == "remove") store.remove(p[1], std::stoi(p[2]));
            else cache.invalidate(p[1]);
        } catch (const std::runtime_error& e) {
            out.push_back(std::string("ERROR:") + e.what());
        }
    }
    out.push_back("loads=" + std::to_string(store.loads));
    std::string joined;
    for (const auto& s : out) joined += (joined.empty() ? "" : "|") + s;
    return joined;
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
