// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <vector>

#include "shared_db_client.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auto f = split(input, ';');
    db::ProcessGlobals process;
    std::set<const db::DatabaseClient*> seen;
    try {
        db::DbModule module(process, f[0]);
        if (f[1] != "-") {
            for (auto& op : split(f[1], ',')) {
                if (op == "reload") module = db::DbModule(process, f[0]);
                else seen.insert(module.prisma().get());
            }
        }
    } catch (const std::invalid_argument& e) {
        return std::string("ERROR:") + e.what();
    }
    return "constructed=" + std::to_string(process.constructed) + ";distinct=" + std::to_string(seen.size());
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
