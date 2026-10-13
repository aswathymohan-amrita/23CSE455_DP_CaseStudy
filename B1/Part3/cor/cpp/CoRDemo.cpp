// PART 3 — Chain of Responsibility Pattern — C++
// Compile: g++ CoRDemo.cpp -o CoRDemo
// Run:     ./CoRDemo   (Linux/Mac) or CoRDemo.exe (Windows)

#include <iostream>
#include <map>
#include <string>
using namespace std;
using Req = map<string, string>;

// Abstract Handler
class Handler {
protected:
    Handler* next = nullptr;
public:
    Handler* setNext(Handler* h) { next = h; return h; }
    virtual string handle(const Req& req) {
        return next ? next->handle(req) : "OK";
    }
};

// Handler 1: Token Validator
class TokenValidator : public Handler {
public:
    string handle(const Req& req) override {
        auto it = req.find("token");
        string token = (it != req.end()) ? it->second : "";
        if (token.empty() || token.rfind("tok_", 0) != 0)
            return "401: Authentication required — no valid token";
        cout << "  [TokenValidator] Token OK: " << token << endl;
        return Handler::handle(req);
    }
};

// Handler 2: Role Checker
class RoleChecker : public Handler {
    string required;
public:
    RoleChecker(string r) : required(r) {}
    string handle(const Req& req) override {
        auto it = req.find("role");
        string role = (it != req.end()) ? it->second : "";
        if (role != required)
            return "403: Forbidden — requires " + required + ", got " + role;
        cout << "  [RoleChecker]   Role OK: " << role << endl;
        return Handler::handle(req);
    }
};

// Handler 3: Final handler
class OrderHandler : public Handler {
public:
    string handle(const Req& req) override {
        auto it = req.find("user");
        string user = (it != req.end()) ? it->second : "unknown";
        return "200: Order created for " + user;
    }
};

int main() {
    TokenValidator validator;
    RoleChecker    roleChecker("MANAGER");
    OrderHandler   orderHandler;
    validator.setNext(&roleChecker)->setNext(&orderHandler);

    cout << "Test 1 - Valid MANAGER:" << endl;
    cout << "  " << validator.handle({{"token","tok_abc"},{"role","MANAGER"},{"user","mgr@rest.com"}}) << endl;
    cout << "Test 2 - Wrong role (SERVER):" << endl;
    cout << "  " << validator.handle({{"token","tok_abc"},{"role","SERVER"},{"user","srv@rest.com"}}) << endl;
    cout << "Test 3 - No token:" << endl;
    cout << "  " << validator.handle({{"token",""},{"role","MANAGER"},{"user","x@rest.com"}}) << endl;
    return 0;
}
