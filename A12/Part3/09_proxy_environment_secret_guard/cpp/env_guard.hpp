// Proxy (protection): Environment Secret Guard.
#pragma once
#include <map>
#include <optional>
#include <stdexcept>
#include <string>

namespace envguard {

// Subject.
class Env {
public:
    virtual ~Env() = default;
    virtual std::optional<std::string> get(const std::string& name) const = 0;
};

// RealSubject: validated variables.
class RealEnv : public Env {
public:
    explicit RealEnv(std::map<std::string, std::string> vars) : vars_(std::move(vars)) {}
    std::optional<std::string> get(const std::string& name) const override {
        auto it = vars_.find(name);
        if (it == vars_.end()) return std::nullopt;
        return it->second;
    }

private:
    std::map<std::string, std::string> vars_;
};

// Proxy: same interface, refuses server-only variables on the client.
class EnvGuard : public Env {
public:
    EnvGuard(const Env& real, bool isServer, bool production)
        : real_(real), isServer_(isServer), production_(production) {}
    std::optional<std::string> get(const std::string& name) const override {
        if (!isServer_ && name.rfind("NEXT_PUBLIC_", 0) != 0) {
            throw std::runtime_error(
                production_ ? "Attempted to access a server-side environment variable on the client"
                            : "Attempted to access server-side environment variable '" + name + "' on the client");
        }
        return real_.get(name);
    }

private:
    const Env& real_;
    bool isServer_;
    bool production_;
};

}  // namespace envguard
