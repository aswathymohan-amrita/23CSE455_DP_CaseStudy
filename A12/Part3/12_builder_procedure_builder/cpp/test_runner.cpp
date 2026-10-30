// Test runner: ./build/test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "procedure_builder.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string join(const std::vector<std::string>& v, const std::string& sep) {
    std::string out;
    for (const auto& s : v) out += (out.empty() ? "" : sep) + s;
    return out;
}

static std::optional<std::string> opt(const std::string& s) {
    return s == "-" ? std::nullopt : std::optional<std::string>(s);
}

static std::string run(const std::string& input) {
    auto p = split(input, ';');
    if (p[0] == "immutable") {
        auto subscribed = builder::protectedProcedure().use("plan", builder::noOp);
        return "base=" + std::to_string(builder::publicProcedure().size()) + ";protected=" +
               std::to_string(builder::protectedProcedure().size()) + ";subscribed=" + std::to_string(subscribed.size());
    }
    std::optional<builder::Procedure> proc;
    try {
        proc = builder::build(split(p[0], ','));
    } catch (const builder::TRPCError& e) {
        return "ERROR:" + e.code;
    }
    try {
        auto r = proc->call(opt(p[1]), opt(p[2]));
        return r.output + ";trace=" + (r.trace.empty() ? "none" : join(r.trace, ">"));
    } catch (const builder::TRPCError& e) {
        return "ERROR:" + e.code + ";trace=" + join(e.trace, ">");
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
