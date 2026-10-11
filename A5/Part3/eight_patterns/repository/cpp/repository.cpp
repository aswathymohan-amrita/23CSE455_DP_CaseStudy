#include <cassert>
#include <map>
#include <string>
struct Patient {
    std::string id,name;
};
struct Repo {
    std::map<std::string,Patient> rows;
    void save(Patient p) {
        rows[p.id]=p;
    }
    const Patient* find(const std::string&id)const {
        auto it=rows.find(id);
        return it==rows.end()?nullptr:&it->second;
    }
};
struct Registry {
    Repo& repo;
    void add(Patient p) {
        repo.save(p);
    }
    const Patient* lookup(const std::string&id) {
        return repo.find(id);
    }
};
int main() {
    Repo r;
    Registry reg{r};
    reg.add({"P1","Demo"});
    assert(reg.lookup("P1")->name=="Demo"&&reg.lookup("none")==nullptr);
}
