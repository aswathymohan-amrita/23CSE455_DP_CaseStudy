#pragma once

#include <algorithm>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Component {
public:
    virtual ~Component() = default;
    virtual const std::string& getName() const = 0;
    virtual void addChild(std::shared_ptr<Component> child) = 0;
    virtual bool removeChild(const std::shared_ptr<Component>& child) = 0;
    virtual std::vector<std::shared_ptr<Component>> getChildren() const = 0;
    virtual std::vector<std::string> traverse() const = 0;
};

class Leaf final : public Component {
public:
    explicit Leaf(std::string name) : name_(std::move(name)) {}

    const std::string& getName() const override {
        return name_;
    }

    void addChild(std::shared_ptr<Component>) override {
        throw std::logic_error("A location leaf cannot contain children");
    }

    bool removeChild(const std::shared_ptr<Component>&) override {
        return false;
    }

    std::vector<std::shared_ptr<Component>> getChildren() const override {
        return {};
    }

    std::vector<std::string> traverse() const override {
        return {name_};
    }

private:
    std::string name_;
};

class Container final : public Component {
public:
    explicit Container(std::string name) : name_(std::move(name)) {}

    const std::string& getName() const override {
        return name_;
    }

    void addChild(std::shared_ptr<Component> child) override {
        children_.push_back(std::move(child));
    }

    bool removeChild(const std::shared_ptr<Component>& child) override {
        const auto found = std::find(children_.begin(), children_.end(), child);
        if (found == children_.end()) {
            return false;
        }
        children_.erase(found);
        return true;
    }

    std::vector<std::shared_ptr<Component>> getChildren() const override {
        return children_;
    }

    std::vector<std::string> traverse() const override {
        std::vector<std::string> names{name_};
        for (const auto& child : children_) {
            auto child_names = child->traverse();
            names.insert(names.end(), child_names.begin(), child_names.end());
        }
        return names;
    }

private:
    std::string name_;
    std::vector<std::shared_ptr<Component>> children_;
};
