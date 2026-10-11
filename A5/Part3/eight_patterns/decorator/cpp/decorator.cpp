#include <cassert>
#include <string>
struct Reader {
    virtual std::string read(const std::string&)=0;
    virtual ~Reader()=default;
};
struct BaseReader:Reader {
    std::string read(const std::string&p)override {
        return p;
    }
};
struct AuditedReader:Reader {
    Reader& inner;
    int count=0;
    explicit AuditedReader(Reader& r):inner(r) {
    }
    std::string read(const std::string&p)override {
        auto r=inner.read(p);
        ++count;
        return r;
    }
};
int main() {
    BaseReader b;
    AuditedReader a{b};
    assert(a.read("P1")=="P1"&&a.count==1);
}
