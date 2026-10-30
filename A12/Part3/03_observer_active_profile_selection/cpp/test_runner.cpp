// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>

#include "profile_selection.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string run(const std::string& input) {
    profiles::ProfileStore store;
    profiles::Hero hero;
    profiles::ShowsContainer rows;
    profiles::PinForm pin;
    const std::map<std::string, const profiles::Observer*> views{
        {"Hero", &hero}, {"ShowsContainer", &rows}, {"PinForm", &pin}};
    std::vector<std::string> out;
    for (auto& cmd : split(input, ';')) {
        auto space = cmd.find(' ');
        std::string op = cmd.substr(0, space);
        std::string arg = space == std::string::npos ? "" : cmd.substr(space + 1);
        if (op == "sub" || op == "unsub") {
            auto it = views.find(arg);
            if (it == views.end()) return "ERROR:unknown observer";
            if (op == "sub") store.subscribe(it->second);
            else store.unsubscribe(it->second);
        } else if (op == "select") {
            auto s = split(arg, ':');
            store.setState({s[0], s[1], s.size() > 2}, out);
        } else {
            store.setState({}, out);
        }
    }
    if (out.empty()) return "-";
    std::string joined = out[0];
    for (size_t i = 1; i < out.size(); i++) joined += "|" + out[i];
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
