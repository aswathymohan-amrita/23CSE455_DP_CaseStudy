// Adapter: NextAuth Prisma Persistence Adapter.
#pragma once
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

namespace auth {

struct User {
    std::string id, email, name;
};

struct Account {
    std::string id, userId, provider;
};

using Fields = std::map<std::string, std::string>;

// Target: what the auth library calls.
class AuthAdapter {
public:
    virtual ~AuthAdapter() = default;
    virtual User createUser(const std::string& email, const std::string& name) = 0;
    virtual std::optional<User> getUserByEmail(const std::string& email) = 0;
    virtual Account linkAccount(const std::string& userId, const std::string& provider) = 0;
};

// Adaptee: Prisma-like client with a different interface (data/where maps).
class OrmClient {
public:
    User userCreate(const Fields& data) {
        if (userFindUnique({{"email", data.at("email")}})) throw std::runtime_error("unique email");
        users_.push_back({"u" + std::to_string(users_.size() + 1), data.at("email"), data.at("name")});
        return users_.back();
    }
    std::optional<User> userFindUnique(const Fields& where) const {
        for (const auto& u : users_)
            if (u.email == where.at("email")) return u;
        return std::nullopt;
    }
    Account accountCreate(const Fields& data) {
        bool exists = false;
        for (const auto& u : users_) exists = exists || u.id == data.at("userId");
        if (!exists) throw std::runtime_error("foreign key");
        accounts_.push_back({"a" + std::to_string(accounts_.size() + 1), data.at("userId"), data.at("provider")});
        return accounts_.back();
    }

private:
    std::vector<User> users_;
    std::vector<Account> accounts_;
};

// Adapter.
class PrismaAdapter : public AuthAdapter {
public:
    explicit PrismaAdapter(OrmClient& orm) : orm_(orm) {}
    User createUser(const std::string& email, const std::string& name) override {
        return orm_.userCreate({{"email", email}, {"name", name}});
    }
    std::optional<User> getUserByEmail(const std::string& email) override {
        return orm_.userFindUnique({{"email", email}});
    }
    Account linkAccount(const std::string& userId, const std::string& provider) override {
        return orm_.accountCreate({{"userId", userId}, {"provider", provider}});
    }

private:
    OrmClient& orm_;
};

}  // namespace auth
