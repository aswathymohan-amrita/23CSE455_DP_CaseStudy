// Decorator: Persisted Profile Store (devtools(persist(creator))).
#pragma once
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace stores {

// Component.
class ProfileStore {
public:
    virtual ~ProfileStore() = default;
    virtual void set(const std::string& field, const std::string& value) = 0;
    virtual std::string state() const = 0;
    virtual void clearStorage() = 0;
};

// ConcreteComponent.
class BasicStore : public ProfileStore {
public:
    void set(const std::string& field, const std::string& value) override {
        if (!fields_.count(field)) throw std::runtime_error("unknown field " + field);
        fields_[field] = value;
    }
    std::string state() const override {
        return "profile=" + fields_.at("profile") + "&pinForm=" + fields_.at("pinForm");
    }
    void clearStorage() override { throw std::runtime_error("clearStorage not available"); }

private:
    std::map<std::string, std::string> fields_{{"profile", "null"}, {"pinForm", "false"}};
};

// Base Decorator: owns and forwards to the wrapped store.
class StoreDecorator : public ProfileStore {
public:
    explicit StoreDecorator(std::unique_ptr<ProfileStore> inner) : inner_(std::move(inner)) {}
    void set(const std::string& field, const std::string& value) override { inner_->set(field, value); }
    std::string state() const override { return inner_->state(); }
    void clearStorage() override { inner_->clearStorage(); }

private:
    std::unique_ptr<ProfileStore> inner_;
};

class PersistDecorator : public StoreDecorator {
public:
    PersistDecorator(std::unique_ptr<ProfileStore> inner, std::map<std::string, std::string>& storage)
        : StoreDecorator(std::move(inner)), storage_(storage) {}
    void set(const std::string& field, const std::string& value) override {
        StoreDecorator::set(field, value);
        storage_["test-store"] = state();
    }
    void clearStorage() override { storage_.erase("test-store"); }

private:
    std::map<std::string, std::string>& storage_;
};

class DevtoolsDecorator : public StoreDecorator {
public:
    DevtoolsDecorator(std::unique_ptr<ProfileStore> inner, std::vector<std::string>& log)
        : StoreDecorator(std::move(inner)), log_(log) {}
    void set(const std::string& field, const std::string& value) override {
        StoreDecorator::set(field, value);
        log_.push_back("set " + field + "=" + value);
    }

private:
    std::vector<std::string>& log_;
};

}  // namespace stores
