#include <cassert>
#include <map>
#include <string>
struct Source {
    int calls=0;
    std::string fetch(const std::string&p) {
        ++calls;
        return p;
    }
};
struct Proxy {
    Source& source;
    std::map<std::string,std::string> cache;
    std::string fetch(const std::string&p) {
        auto it=cache.find(p);
        if(it!=cache.end())return it->second;
        return cache[p]=source.fetch(p);
    }
    void invalidate(const std::string&p) {
        cache.erase(p);
    }
};
int main() {
    Source s;
    Proxy p{s};
    p.fetch("P1");
    p.fetch("P1");
    assert(s.calls==1);
    p.invalidate("P1");
    p.fetch("P1");
    assert(s.calls==2);
}
