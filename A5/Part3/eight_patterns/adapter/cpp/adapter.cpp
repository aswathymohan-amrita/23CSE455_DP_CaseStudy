#include <cassert>
#include <string>
struct Vendor {
    std::string submit(const std::string&patient,const std::string&test) {
        assert(patient=="P1"&&test=="CBC");
        return "LAB-1";
    }
};
struct Gateway {
    virtual std::string order(const std::string&,const std::string&)=0;
    virtual ~Gateway()=default;
};
struct Adapter:Gateway {
    Vendor& vendor;
    explicit Adapter(Vendor& v):vendor(v) {
    }
    std::string order(const std::string&p,const std::string&t)override {
        assert(!p.empty()&&!t.empty());
        return vendor.submit(p,t);
    }
};
int main() {
    Vendor v;
    Adapter a{v};
    assert(a.order("P1","CBC")=="LAB-1");
}
