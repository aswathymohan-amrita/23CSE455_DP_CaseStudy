#include <cassert>
#include <algorithm>
#include <string>
#include <vector>
struct Observer {
    std::vector<std::string> events;
    void update(const std::string&e) {
        events.push_back(e);
    }
};
struct Publisher {
    std::vector<Observer*> subs;
    void subscribe(Observer&o) {
        subs.push_back(&o);
    }
    void unsubscribe(Observer&o) {
        subs.erase(std::remove(subs.begin(),subs.end(),&o),subs.end());
    }
    void publish(const std::string&e) {
        for(auto*o:subs)o->update(e);
    }
};
int main() {
    Publisher p;
    Observer o;
    p.subscribe(o);
    p.publish("lab.ready");
    p.unsubscribe(o);
    p.publish("other");
    assert(o.events.size()==1&&o.events[0]=="lab.ready");
}
