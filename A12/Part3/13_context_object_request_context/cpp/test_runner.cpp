// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "request_context.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::optional<std::string> opt(const std::string& s) {
    return s == "-" ? std::nullopt : std::optional<std::string>(s);
}

static std::string run(const std::string& input) {
    auto p = split(input, '|');
    reqctx::Ctx ctx;
    if (p[0].rfind("inner:", 0) == 0) {
        auto q = split(p[0], ':');
        ctx = reqctx::createInnerContext(opt(q[1]), opt(q[2]));
    } else {
        std::map<std::string, std::string> headers;
        if (p[0] != "-") {
            for (const auto& pair : split(p[0], ',')) {
                auto i = pair.find('=');
                headers[pair.substr(0, i)] = pair.substr(i + 1);
            }
        }
        ctx = reqctx::createContext(headers);
    }
    try {
        return reqctx::call(p[1], ctx);
    } catch (const reqctx::TRPCError& e) {
        return "ERROR:" + e.code;
    }
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
