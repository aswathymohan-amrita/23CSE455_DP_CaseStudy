// Test runner: ./test_runner ../cases.tsv
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include "profile_stores.hpp"

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, sep)) out.push_back(item);
    return out;
}

static std::string join(const std::vector<std::string>& v) {
    if (v.empty()) return "-";
    std::string s = v[0];
    for (size_t i = 1; i < v.size(); i++) s += "," + v[i];
    return s;
}

static std::string run(const std::string& input) {
    auto f = split(input, ';');
    std::map<std::string, std::string> storage;
    std::vector<std::string> log;
    try {
        std::unique_ptr<stores::ProfileStore> store = std::make_unique<stores::BasicStore>();
        if (f[0] != "none") {
            for (auto& name : split(f[0], '+')) {
                if (name == "persist") store = std::make_unique<stores::PersistDecorator>(std::move(store), storage);
                else if (name == "devtools") store = std::make_unique<stores::DevtoolsDecorator>(std::move(store), log);
                else throw std::runtime_error("unknown decorator " + name);
            }
        }
        if (f[1] != "-") {
            for (auto& op : split(f[1], ',')) {
                if (op == "clear") store->clearStorage();
                else {
                    auto kv = split(op, '=');
                    store->set(kv[0], kv[1]);
                }
            }
        }
        auto it = storage.find("test-store");
        return "state=" + store->state() + ";storage=" + (it == storage.end() ? "-" : it->second) + ";log=" + join(log);
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
