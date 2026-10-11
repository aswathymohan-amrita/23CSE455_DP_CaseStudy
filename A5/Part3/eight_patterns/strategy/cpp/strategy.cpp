#include <cassert>
#include <string>
struct Payment {
    virtual std::string pay(int,const std::string&)=0;
    virtual ~Payment()=default;
};
struct Card:Payment {
    std::string pay(int a,const std::string&r)override {
        assert(a>0&&!r.empty());
        return "card";
    }
};
struct Wallet:Payment {
    std::string pay(int a,const std::string&r)override {
        assert(a>0&&!r.empty());
        return "wallet";
    }
};
struct Billing {
    Payment& strategy;
    std::string checkout(int a,const std::string&r) {
        return strategy.pay(a,r);
    }
};
int main() {
    Card c;
    Wallet w;
    Billing b{c};
    assert(b.checkout(100,"B1")=="card");
    Billing d{w};
    assert(d.checkout(100,"B1")=="wallet");
}
