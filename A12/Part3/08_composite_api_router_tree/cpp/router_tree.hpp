// Composite: API Router Tree (appRouter with sub-routers and procedures, after CH01).
#pragma once
#include <algorithm>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace routers {

// Component.
class Node {
public:
    virtual ~Node() = default;
    virtual int count() const = 0;
    virtual const Node* resolve(const std::vector<std::string>& parts, size_t from) const = 0;
    virtual void paths(const std::string& prefix, std::vector<std::string>& out) const = 0;
    virtual int depth() const = 0;
};

// Leaf.
class Procedure : public Node {
public:
    explicit Procedure(std::string type) : type(std::move(type)) {}
    int count() const override { return 1; }
    const Node* resolve(const std::vector<std::string>& parts, size_t from) const override {
        return from == parts.size() ? this : nullptr;
    }
    void paths(const std::string& prefix, std::vector<std::string>& out) const override { out.push_back(prefix); }
    int depth() const override { return 0; }
    const std::string type;
};

// Composite.
class Router : public Node {
public:
    Router& add(std::string name, std::unique_ptr<Node> child) {
        children_.emplace_back(std::move(name), std::move(child));
        return *this;
    }
    int count() const override {
        int n = 0;
        for (const auto& [_, child] : children_) n += child->count();
        return n;
    }
    const Node* resolve(const std::vector<std::string>& parts, size_t from) const override {
        if (from == parts.size()) return this;
        for (const auto& [name, child] : children_)
            if (name == parts[from]) return child->resolve(parts, from + 1);
        return nullptr;
    }
    void paths(const std::string& prefix, std::vector<std::string>& out) const override {
        for (const auto& [name, child] : children_) child->paths(prefix.empty() ? name : prefix + "." + name, out);
    }
    int depth() const override {
        int deepest = -1;
        for (const auto& [_, child] : children_) deepest = std::max(deepest, child->depth());
        return 1 + deepest;
    }

private:
    std::vector<std::pair<std::string, std::unique_ptr<Node>>> children_;
};

inline std::unique_ptr<Router> makeRouter(const std::vector<std::pair<std::string, std::string>>& procs) {
    auto r = std::make_unique<Router>();
    for (const auto& [name, type] : procs) r->add(name, std::make_unique<Procedure>(type));
    return r;
}

inline std::unique_ptr<Router> appRouter() {
    const std::string q = "query", m = "mutation";
    auto root = std::make_unique<Router>();
    root->add("user", makeRouter({{"getSession", q}, {"getCurrent", q}, {"getCurrentWithProfile", q}, {"update", m}}));
    root->add("profile", makeRouter({{"getAll", q}, {"getOthers", q}, {"getOne", q}, {"create", m},
                                     {"update", m}, {"updatePin", m}, {"delete", m}}));
    root->add("icon", makeRouter({{"getAll", q}, {"getAllUsed", q}, {"getAllUnused", q}, {"getCurrent", q}}));
    root->add("myList", makeRouter({{"getAll", q}, {"create", m}, {"update", m}, {"delete", m}}));
    root->add("catalogue", makeRouter({{"checkAccess", q}}));
    return root;
}

}  // namespace routers
