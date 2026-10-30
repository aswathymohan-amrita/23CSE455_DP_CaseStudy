// Observer: Active Profile Selection (profile store notifies subscribed views).
#pragma once
#include <algorithm>
#include <optional>
#include <string>
#include <vector>

namespace profiles {

struct State {
    std::string profile = "-";
    std::string maturity = "NONE";
    bool pinForm = false;
};

class Observer {
public:
    virtual ~Observer() = default;
    // Returns this observer's output for the new state, or nullopt if it does not react.
    virtual std::optional<std::string> notify(const State& s) const = 0;
};

// ConcreteSubject: the profile store. Observers are not owned.
class ProfileStore {
public:
    void subscribe(const Observer* o) {
        if (std::find(observers_.begin(), observers_.end(), o) == observers_.end()) observers_.push_back(o);
    }
    void unsubscribe(const Observer* o) {
        observers_.erase(std::remove(observers_.begin(), observers_.end(), o), observers_.end());
    }
    void setState(State next, std::vector<std::string>& out) {
        state_ = std::move(next);
        for (const Observer* o : observers_)
            if (auto reaction = o->notify(state_)) out.push_back(*reaction);
    }

private:
    std::vector<const Observer*> observers_;
    State state_;
};

class Hero : public Observer {
public:
    std::optional<std::string> notify(const State& s) const override { return "Hero:" + s.maturity; }
};

class ShowsContainer : public Observer {
public:
    std::optional<std::string> notify(const State& s) const override {
        return "Rows:" + s.profile + "/" + s.maturity;
    }
};

class PinForm : public Observer {
public:
    std::optional<std::string> notify(const State& s) const override {
        if (!s.pinForm) return std::nullopt;
        return "Pin:" + s.profile;
    }
};

}  // namespace profiles
