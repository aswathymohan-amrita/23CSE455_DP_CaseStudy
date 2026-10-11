#include "observer.hpp"

#include <cassert>
#include <iostream>
#include <string>
#include <vector>

struct Setup {
    Publisher publisher;
    RecordingObserver one;
    RecordingObserver two;
    RecordingObserver three;

    Setup() {
        publisher.subscribe(one);
        publisher.subscribe(two);
        publisher.subscribe(three);
    }
};

void test_all_observers_receive_first_event() {
    Setup setup;
    setup.publisher.publish(Event{"STOCK_LOW"});
    assert(setup.one.received_events.size() == 1);
    assert(setup.two.received_events.size() == 1);
    assert(setup.three.received_events.size() == 1);
}

void test_unsubscribe_excludes_observer_from_second_event() {
    Setup setup;
    setup.publisher.publish(Event{"STOCK_LOW"});
    setup.publisher.unsubscribe(setup.two);
    setup.publisher.publish(Event{"STOCK_REPLENISHED"});
    assert(setup.one.received_events.size() == 2);
    assert(setup.two.received_events.size() == 1);
    assert(setup.three.received_events.size() == 2);
}

void test_event_values_are_preserved() {
    Setup setup;
    setup.publisher.publish(Event{"STOCK_LOW"});
    setup.publisher.unsubscribe(setup.two);
    setup.publisher.publish(Event{"STOCK_REPLENISHED"});
    const auto types = [](const RecordingObserver& observer) {
        std::vector<std::string> values;
        for (const auto& event : observer.received_events) {
            values.push_back(event.type);
        }
        return values;
    };
    assert((types(setup.one) == std::vector<std::string>{"STOCK_LOW", "STOCK_REPLENISHED"}));
    assert((types(setup.two) == std::vector<std::string>{"STOCK_LOW"}));
    assert((types(setup.three) == std::vector<std::string>{"STOCK_LOW", "STOCK_REPLENISHED"}));
}

int main() {
    test_all_observers_receive_first_event();
    test_unsubscribe_excludes_observer_from_second_event();
    test_event_values_are_preserved();
    std::cout << "Observer C++: 3 tests passed\n";
}
