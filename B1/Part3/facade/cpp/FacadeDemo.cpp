// PART 3 — Facade Pattern — C++
// Compile: g++ FacadeDemo.cpp -o FacadeDemo
// Run:     ./FacadeDemo   (Linux/Mac) or FacadeDemo.exe (Windows)

#include <iostream>
#include <map>
#include <string>
#include <functional>
using namespace std;

// Subsystem 1: PasswordChecker
class PasswordChecker {
public:
    bool verify(const string& plain, const string& stored) { return plain == stored; }
};

// Subsystem 2: TokenService
class TokenService {
public:
    string generate(const string& email, const string& role) {
        // Simple base64-like encoding (hash for demo)
        return "tok_" + to_string(hash<string>{}(email)) + "_" + role;
    }
};

// Subsystem 3: UserRepository
struct UserRecord { string password; string role; };
class UserRepository {
    map<string, UserRecord> db;
public:
    UserRepository() {
        db["chef@restaurant.com"] = {"secret123", "KITCHEN"};
    }
    UserRecord* findByEmail(const string& email) {
        auto it = db.find(email);
        return (it != db.end()) ? &it->second : nullptr;
    }
};

// Facade
class AuthFacade {
    PasswordChecker checker;
    TokenService    tokenService;
    UserRepository  repo;
public:
    string login(const string& email, const string& password) {
        UserRecord* user = repo.findByEmail(email);
        if (!user) return "{\"error\": \"User not found\"}";
        if (!checker.verify(password, user->password)) return "{\"error\": \"Invalid password\"}";
        string token = tokenService.generate(email, user->role);
        return "{\"success\": true, \"user\": \"" + email + "\", \"token\": \"" + token + "\", \"role\": \"" + user->role + "\"}";
    }
};

// Client
int main() {
    AuthFacade facade;
    cout << "Test 1 - Valid login:    " << facade.login("chef@restaurant.com", "secret123") << endl;
    cout << "Test 2 - Wrong password: " << facade.login("chef@restaurant.com", "wrongpass")  << endl;
    cout << "Test 3 - User not found: " << facade.login("nobody@restaurant.com", "secret123") << endl;
    return 0;
}
