// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "front_controller.hpp"

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
    auto p = split(input, ' ');
    int ctxCount = 0, logged = 0;
    fc::FrontController controller(
        fc::appRouter(),
        [&](const std::optional<std::string>& u) {
            ctxCount++;
            return fc::Context{u, "prisma"};
        },
        [&](const std::string&, const std::string&) { logged++; });
    auto results = controller.handle(opt(p[0]), opt(p[1]));
    std::string joined;
    for (const auto& r : results) joined += (joined.empty() ? "" : "|") + r;
    return joined + ";ctx=" + std::to_string(ctxCount) + ";logged=" + std::to_string(logged);
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
