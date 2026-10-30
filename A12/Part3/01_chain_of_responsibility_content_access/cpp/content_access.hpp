// Chain of Responsibility: Content Access Rule Chain (Region -> Maturity -> Premium).
#pragma once
#include <map>
#include <memory>
#include <optional>
#include <set>
#include <stdexcept>
#include <string>

namespace access {

struct Show {
    int id;
    bool premium;
    bool adult;
    std::set<int> genres;
};

struct Viewer {
    int planTier;
    std::string region;
    std::string maturity;
};

struct Decision {
    bool allowed;
    std::string reason;
    std::string visibility;
    std::string str() const { return allowed ? "ALLOW" : "DENY:" + reason + ":" + visibility; }
};

// Handler. check() is also a template method; evaluate() is the primitive step.
class AccessRule {
public:
    virtual ~AccessRule() = default;
    AccessRule* setNext(std::unique_ptr<AccessRule> rule) {
        next_ = std::move(rule);
        return next_.get();
    }
    Decision check(const Show& show, const Viewer& viewer) const {
        if (auto denial = evaluate(show, viewer)) return *denial;
        return next_ ? next_->check(show, viewer) : Decision{true, "", ""};
    }

protected:
    virtual std::optional<Decision> evaluate(const Show&, const Viewer&) const = 0;

private:
    std::unique_ptr<AccessRule> next_;
};

class RegionRule : public AccessRule {
protected:
    std::optional<Decision> evaluate(const Show& show, const Viewer& viewer) const override {
        static const std::map<int, std::set<std::string>> blocked{{550, {"CN"}}};
        static const std::map<int, std::set<std::string>> allowed{{1399, {"US", "GB", "IN"}}};
        auto a = allowed.find(show.id);
        auto b = blocked.find(show.id);
        bool denied = (a != allowed.end() && !a->second.count(viewer.region)) ||
                      (b != blocked.end() && b->second.count(viewer.region));
        if (denied) return Decision{false, "REGION_BLOCKED", "hidden"};
        return std::nullopt;
    }
};

class MaturityRule : public AccessRule {
protected:
    std::optional<Decision> evaluate(const Show& show, const Viewer& viewer) const override {
        struct Policy {
            bool allowAdult;
            std::set<int> blocked;
        };
        static const std::map<std::string, Policy> policies{
            {"KIDS", {false, {27, 53, 80, 10752}}},
            {"TEEN", {false, {27}}},
            {"ADULT", {true, {}}},
            {"NONE", {true, {}}}};
        auto it = policies.find(viewer.maturity);
        if (it == policies.end()) throw std::invalid_argument("unknown maturity");
        bool denied = show.adult && !it->second.allowAdult;
        for (int g : show.genres) denied = denied || it->second.blocked.count(g);
        if (denied) return Decision{false, "MATURITY_BLOCKED", "hidden"};
        return std::nullopt;
    }
};

class PremiumContentRule : public AccessRule {
protected:
    std::optional<Decision> evaluate(const Show& show, const Viewer& viewer) const override {
        if (show.premium && viewer.planTier < 3) return Decision{false, "PREMIUM_REQUIRED", "locked"};
        return std::nullopt;
    }
};

inline std::unique_ptr<AccessRule> contentAccessChain() {
    auto head = std::make_unique<RegionRule>();
    head->setNext(std::make_unique<MaturityRule>())->setNext(std::make_unique<PremiumContentRule>());
    return head;
}

}  // namespace access
