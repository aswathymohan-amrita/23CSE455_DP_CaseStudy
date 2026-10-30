// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "router_tree.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    auto root = routers::appRouter();
    auto p = split(input, ' ');
    if (p[0] == "depth") return std::to_string(root->depth());
    const routers::Node* node = p.size() > 1 ? root->resolve(split(p[1], '.'), 0) : root.get();
    if (!node) return "NOT_FOUND";
    if (p[0] == "count") return std::to_string(node->count());
    if (p[0] == "paths") {
        std::vector<std::string> out;
        node->paths(p[1], out);
        std::string joined;
        for (const auto& s : out) joined += (joined.empty() ? "" : ",") + s;
        return joined;
    }
    if (auto proc = dynamic_cast<const routers::Procedure*>(node)) return proc->type;
    return "router(" + std::to_string(node->count()) + ")";
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
