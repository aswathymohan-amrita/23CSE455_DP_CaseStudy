// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "auth_adapters.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auth::OrmClient orm;
    auth::PrismaAdapter adapterImpl(orm);
    auth::AuthAdapter& adapter = adapterImpl;
    std::string out;
    for (auto& cmd : split(input, ';')) {
        auto p = split(cmd, ' ');
        std::string entry;
        try {
            if (p[0] == "create") entry = adapter.createUser(p[1], p[2]).id;
            else if (p[0] == "get") {
                auto u = adapter.getUserByEmail(p[1]);
                entry = u ? u->id + ":" + u->name : "null";
            } else if (p[0] == "link") {
                auto a = adapter.linkAccount(p[1], p[2]);
                entry = a.id + ":" + a.userId + ":" + a.provider;
            } else entry = "ERROR:unknown operation";
        } catch (const std::runtime_error& e) {
            entry = std::string("ERROR:") + e.what();
        }
        out += (out.empty() ? "" : "|") + entry;
    }
    return out;
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
