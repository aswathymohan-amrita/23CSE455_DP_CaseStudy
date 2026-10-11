#pragma once

#include <algorithm>
#include <string>
#include <vector>

struct Event {
    std::string type;
};

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const Event& event) = 0;
};

class EventSubject {
public:
    virtual ~EventSubject() = default;
    virtual void subscribe(Observer& observer) = 0;
    virtual void unsubscribe(Observer& observer) = 0;
    virtual void publish(const Event& event) = 0;
};

class Publisher final : public EventSubject {
public:
    void subscribe(Observer& observer) override {
        if (std::find(observers_.begin(), observers_.end(), &observer) == observers_.end()) {
            observers_.push_back(&observer);
        }
    }

    void unsubscribe(Observer& observer) override {
        std::erase(observers_, &observer);
    }

    void publish(const Event& event) override {
        const auto subscribers = observers_;
        for (auto* observer : subscribers) {
            observer->update(event);
        }
    }

private:
    std::vector<Observer*> observers_;
};

class RecordingObserver final : public Observer {
public:
    void update(const Event& event) override {
        received_events.push_back(event);
    }

    std::vector<Event> received_events;
};
