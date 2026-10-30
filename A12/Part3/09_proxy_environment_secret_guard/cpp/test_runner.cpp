// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "env_guard.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    static const envguard::RealEnv real({{"DATABASE_URL", "mysql://db"},
                                         {"STRIPE_API_KEY", "sk_test_123"},
                                         {"NEXT_PUBLIC_TMDB_API_KEY", "tmdb_abc"},
                                         {"NEXT_PUBLIC_APP_URL", "http://localhost:3000"}});
    auto f = split(input, ';');
    envguard::EnvGuard env(real, f[0] == "server", f[0] == "client-prod");
    const envguard::Env& subject = env;
    try {
        auto value = subject.get(f[1]);
        return value ? *value : "undefined";
    } catch (const std::runtime_error& e) {
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
