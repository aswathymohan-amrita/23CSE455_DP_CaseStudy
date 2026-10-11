#include <cassert>
#include <string>
#include <vector>
struct Store {
    int count=0;
    int save(const std::string&,const std::string&) {
        return ++count;
    }
};
struct Notice {
    int sent=0;
    void send(const std::string&,const std::string&) {
        ++sent;
    }
};
struct Facade {
    Store& s;
    Notice& n;
    int book(const std::string&p,const std::string&d) {
        assert(!p.empty()&&!d.empty());
        int id=s.save(p,d);
        n.send(p,std::to_string(id));
        return id;
    }
};
int main() {
    Store s;
    Notice n;
    Facade f{s,n};
    assert(f.book("P1","D1")==1&&n.sent==1);
}
