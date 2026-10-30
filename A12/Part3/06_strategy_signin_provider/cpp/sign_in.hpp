// Strategy: Sign-in Provider Strategy (NextAuth providers).
#pragma once
#include <algorithm>
#include <cctype>
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

namespace signin {

// Strategy.
class Provider {
public:
    virtual ~Provider() = default;
    virtual std::optional<std::string> authorize(const std::string& credential) const = 0;
};

class GoogleProvider : public Provider {
public:
    std::optional<std::string> authorize(const std::string& c) const override {
        if (c.rfind("g-", 0) == 0) return "google:" + c.substr(2);
        return std::nullopt;
    }
};

class GithubProvider : public Provider {
public:
    std::optional<std::string> authorize(const std::string& c) const override {
        if (c.rfind("gh-", 0) == 0) return "github:" + c.substr(3);
        return std::nullopt;
    }
};

class EmailProvider : public Provider {
public:
    std::optional<std::string> authorize(const std::string& c) const override {
        static const std::regex pattern(R"([^@\s]+@[^@\s]+\.[^@\s]+)");
        if (!std::regex_match(c, pattern)) return std::nullopt;
        std::string lower = c;
        std::transform(lower.begin(), lower.end(), lower.begin(), [](unsigned char ch) { return std::tolower(ch); });
        return "email:" + lower;
    }
};

// Context.
class NextAuth {
public:
    explicit NextAuth(const std::vector<std::string>& providerIds) {
        static const std::map<std::string, std::function<std::unique_ptr<Provider>()>> registry{
            {"google", [] { return std::make_unique<GoogleProvider>(); }},
            {"github", [] { return std::make_unique<GithubProvider>(); }},
            {"email", [] { return std::make_unique<EmailProvider>(); }}};
        for (const auto& id : providerIds) {
            auto it = registry.find(id);
            if (it == registry.end()) throw std::invalid_argument("unsupported provider " + id);
            providers_[id] = it->second();
        }
    }
    std::string signIn(const std::string& providerId, const std::string& credential) const {
        auto it = providers_.find(providerId);
        if (it == providers_.end()) return "ERR:unknown provider";
        auto profile = it->second->authorize(credential);
        return profile ? "OK:" + *profile : "ERR:invalid credentials";
    }

private:
    std::map<std::string, std::unique_ptr<Provider>> providers_;
};

}  // namespace signin
