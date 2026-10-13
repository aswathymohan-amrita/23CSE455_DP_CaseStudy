# Part 3 — Cross-Language Implementation

**Scenario:** Both patterns model the exact same situation found in the codebase.
- **Façade:** `AuthFacade.login(email, password)` orchestrates password check + token generation + DB lookup
- **Chain of Responsibility:** A request passes through `TokenValidator → RoleChecker → RequestHandler`

**Equivalent input:** `email = "chef@restaurant.com"`, `password = "secret123"`, `role = "KITCHEN"`
**Equivalent output:** `{ success: true, user: "chef@restaurant.com", token: "tok_abc123", role: "KITCHEN" }` or an error message.

---

## Pattern 1 — Façade

---

### Java

```java
// === Subsystem 1: PasswordChecker ===
class PasswordChecker {
    public boolean verify(String plain, String stored) {
        // Simulates bcrypt.compare
        return plain.equals(stored);
    }
}

// === Subsystem 2: TokenService ===
class TokenService {
    public String generate(String email, String role) {
        return "tok_" + email.hashCode() + "_" + role;
    }
}

// === Subsystem 3: UserRepository ===
class UserRepository {
    private java.util.Map<String, String[]> db = new java.util.HashMap<>();
    public UserRepository() {
        db.put("chef@restaurant.com", new String[]{"secret123", "KITCHEN"});
    }
    public String[] findByEmail(String email) { return db.get(email); }
}

// === Facade ===
class AuthFacade {
    private PasswordChecker checker = new PasswordChecker();
    private TokenService tokenService = new TokenService();
    private UserRepository repo = new UserRepository();

    public String login(String email, String password) {
        String[] user = repo.findByEmail(email);
        if (user == null) return "ERROR: User not found";
        if (!checker.verify(password, user[0])) return "ERROR: Invalid password";
        String token = tokenService.generate(email, user[1]);
        return "{ success: true, user: \"" + email + "\", token: \"" + token + "\", role: \"" + user[1] + "\" }";
    }
}

// === Client ===
public class FacadeDemo {
    public static void main(String[] args) {
        AuthFacade facade = new AuthFacade();
        System.out.println(facade.login("chef@restaurant.com", "secret123")); // success
        System.out.println(facade.login("chef@restaurant.com", "wrongpass")); // error
    }
}
```

**Output:**
```
{ success: true, user: "chef@restaurant.com", token: "tok_-1984651840_KITCHEN", role: "KITCHEN" }
ERROR: Invalid password
```

---

### Python

```python
# === Subsystem 1: PasswordChecker ===
class PasswordChecker:
    def verify(self, plain: str, stored: str) -> bool:
        return plain == stored  # simulates bcrypt.compare

# === Subsystem 2: TokenService ===
class TokenService:
    def generate(self, email: str, role: str) -> str:
        return f"tok_{hash(email)}_{role}"

# === Subsystem 3: UserRepository ===
class UserRepository:
    def __init__(self):
        self._db = {"chef@restaurant.com": {"password": "secret123", "role": "KITCHEN"}}

    def find_by_email(self, email: str):
        return self._db.get(email)

# === Facade ===
class AuthFacade:
    def __init__(self):
        self._checker = PasswordChecker()
        self._token   = TokenService()
        self._repo    = UserRepository()

    def login(self, email: str, password: str) -> str:
        user = self._repo.find_by_email(email)
        if not user:
            return "ERROR: User not found"
        if not self._checker.verify(password, user["password"]):
            return "ERROR: Invalid password"
        token = self._token.generate(email, user["role"])
        return f'{{ "success": true, "user": "{email}", "token": "{token}", "role": "{user["role"]}" }}'

# === Client ===
if __name__ == "__main__":
    facade = AuthFacade()
    print(facade.login("chef@restaurant.com", "secret123"))  # success
    print(facade.login("chef@restaurant.com", "wrongpass"))  # error
```

**Output:**
```
{ "success": true, "user": "chef@restaurant.com", "token": "tok_<hash>_KITCHEN", "role": "KITCHEN" }
ERROR: Invalid password
```

---

### JavaScript (Node.js)

```js
// === Subsystem 1: PasswordChecker ===
class PasswordChecker {
  verify(plain, stored) { return plain === stored; } // simulates bcrypt.compareSync
}

// === Subsystem 2: TokenService ===
class TokenService {
  generate(email, role) { return `tok_${Buffer.from(email).toString('base64')}_${role}`; }
}

// === Subsystem 3: UserRepository ===
class UserRepository {
  constructor() {
    this.db = { "chef@restaurant.com": { password: "secret123", role: "KITCHEN" } };
  }
  findByEmail(email) { return this.db[email] || null; }
}

// === Facade ===
class AuthFacade {
  constructor() {
    this.checker = new PasswordChecker();
    this.tokenService = new TokenService();
    this.repo = new UserRepository();
  }
  login(email, password) {
    const user = this.repo.findByEmail(email);
    if (!user) return "ERROR: User not found";
    if (!this.checker.verify(password, user.password)) return "ERROR: Invalid password";
    const token = this.tokenService.generate(email, user.role);
    return JSON.stringify({ success: true, user: email, token, role: user.role });
  }
}

// === Client ===
const facade = new AuthFacade();
console.log(facade.login("chef@restaurant.com", "secret123")); // success
console.log(facade.login("chef@restaurant.com", "wrongpass")); // error
```

**Output:**
```
{"success":true,"user":"chef@restaurant.com","token":"tok_Y2hlZkByZXN0YXVyYW50LmNvbQ==_KITCHEN","role":"KITCHEN"}
ERROR: Invalid password
```

---

### C++

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

// === Subsystem 1: PasswordChecker ===
class PasswordChecker {
public:
    bool verify(const string& plain, const string& stored) { return plain == stored; }
};

// === Subsystem 2: TokenService ===
class TokenService {
public:
    string generate(const string& email, const string& role) {
        return "tok_" + to_string(hash<string>{}(email)) + "_" + role;
    }
};

// === Subsystem 3: UserRepository ===
struct UserRecord { string password; string role; };
class UserRepository {
    map<string, UserRecord> db;
public:
    UserRepository() { db["chef@restaurant.com"] = {"secret123", "KITCHEN"}; }
    UserRecord* findByEmail(const string& email) {
        auto it = db.find(email);
        return (it != db.end()) ? &it->second : nullptr;
    }
};

// === Facade ===
class AuthFacade {
    PasswordChecker checker;
    TokenService    tokenService;
    UserRepository  repo;
public:
    string login(const string& email, const string& password) {
        UserRecord* user = repo.findByEmail(email);
        if (!user) return "ERROR: User not found";
        if (!checker.verify(password, user->password)) return "ERROR: Invalid password";
        string token = tokenService.generate(email, user->role);
        return "{ success: true, user: \"" + email + "\", token: \"" + token + "\", role: \"" + user->role + "\" }";
    }
};

// === Client ===
int main() {
    AuthFacade facade;
    cout << facade.login("chef@restaurant.com", "secret123") << endl; // success
    cout << facade.login("chef@restaurant.com", "wrongpass")  << endl; // error
    return 0;
}
```

**Output:**
```
{ success: true, user: "chef@restaurant.com", token: "tok_<hash>_KITCHEN", role: "KITCHEN" }
ERROR: Invalid password
```

---

## Pattern 2 — Chain of Responsibility

---

### Java

```java
// === Abstract Handler ===
abstract class RequestHandler {
    protected RequestHandler next;
    public RequestHandler setNext(RequestHandler next) { this.next = next; return next; }
    public abstract String handle(java.util.Map<String,String> request);
}

// === Handler 1: TokenValidator ===
class TokenValidator extends RequestHandler {
    public String handle(java.util.Map<String,String> req) {
        if (!req.containsKey("token") || req.get("token").isEmpty())
            return "401: Authentication required — no token";
        System.out.println("[TokenValidator] Token OK: " + req.get("token"));
        return next != null ? next.handle(req) : "OK";
    }
}

// === Handler 2: RoleChecker ===
class RoleChecker extends RequestHandler {
    private String requiredRole;
    public RoleChecker(String requiredRole) { this.requiredRole = requiredRole; }
    public String handle(java.util.Map<String,String> req) {
        if (!requiredRole.equals(req.get("role")))
            return "403: Forbidden — requires " + requiredRole + ", got " + req.get("role");
        System.out.println("[RoleChecker] Role OK: " + req.get("role"));
        return next != null ? next.handle(req) : "OK";
    }
}

// === Handler 3: RequestHandler (final) ===
class OrderRequestHandler extends RequestHandler {
    public String handle(java.util.Map<String,String> req) {
        return "200: Order created for " + req.get("user");
    }
}

// === Client ===
public class CoRDemo {
    public static void main(String[] args) {
        TokenValidator validator = new TokenValidator();
        RoleChecker roleChecker = new RoleChecker("MANAGER");
        OrderRequestHandler handler = new OrderRequestHandler();
        validator.setNext(roleChecker).setNext(handler); // assemble chain

        java.util.Map<String,String> req1 = new java.util.HashMap<>();
        req1.put("token", "tok_abc"); req1.put("role", "MANAGER"); req1.put("user", "mgr@rest.com");
        System.out.println(validator.handle(req1)); // success

        java.util.Map<String,String> req2 = new java.util.HashMap<>();
        req2.put("token", "tok_abc"); req2.put("role", "SERVER"); req2.put("user", "srv@rest.com");
        System.out.println(validator.handle(req2)); // 403

        java.util.Map<String,String> req3 = new java.util.HashMap<>();
        req3.put("role", "MANAGER"); // no token
        System.out.println(validator.handle(req3)); // 401
    }
}
```

**Output:**
```
[TokenValidator] Token OK: tok_abc
[RoleChecker] Role OK: MANAGER
200: Order created for mgr@rest.com
[TokenValidator] Token OK: tok_abc
403: Forbidden — requires MANAGER, got SERVER
401: Authentication required — no token
```

---

### Python

```python
from abc import ABC, abstractmethod
from typing import Optional

# === Abstract Handler ===
class RequestHandler(ABC):
    def __init__(self):
        self._next: Optional["RequestHandler"] = None

    def set_next(self, handler: "RequestHandler") -> "RequestHandler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: dict) -> str: ...

# === Handler 1: TokenValidator ===
class TokenValidator(RequestHandler):
    def handle(self, request: dict) -> str:
        if not request.get("token"):
            return "401: Authentication required — no token"
        print(f"[TokenValidator] Token OK: {request['token']}")
        return self._next.handle(request) if self._next else "OK"

# === Handler 2: RoleChecker ===
class RoleChecker(RequestHandler):
    def __init__(self, required_role: str):
        super().__init__()
        self._required = required_role

    def handle(self, request: dict) -> str:
        if request.get("role") != self._required:
            return f"403: Forbidden — requires {self._required}, got {request.get('role')}"
        print(f"[RoleChecker] Role OK: {request['role']}")
        return self._next.handle(request) if self._next else "OK"

# === Handler 3: Final handler ===
class OrderRequestHandler(RequestHandler):
    def handle(self, request: dict) -> str:
        return f"200: Order created for {request.get('user')}"

# === Client ===
if __name__ == "__main__":
    validator = TokenValidator()
    role_check = RoleChecker("MANAGER")
    order_handler = OrderRequestHandler()
    validator.set_next(role_check).set_next(order_handler)

    print(validator.handle({"token": "tok_abc", "role": "MANAGER", "user": "mgr@rest.com"}))
    print(validator.handle({"token": "tok_abc", "role": "SERVER",  "user": "srv@rest.com"}))
    print(validator.handle({"role": "MANAGER"}))  # no token
```

**Output:**
```
[TokenValidator] Token OK: tok_abc
[RoleChecker] Role OK: MANAGER
200: Order created for mgr@rest.com
[TokenValidator] Token OK: tok_abc
403: Forbidden — requires MANAGER, got SERVER
401: Authentication required — no token
```

---

### JavaScript (Node.js)

```js
// === Handler base ===
class Handler {
  setNext(handler) { this.next = handler; return handler; }
  handle(request) { return this.next ? this.next.handle(request) : "OK"; }
}

// === Handler 1: TokenValidator ===
class TokenValidator extends Handler {
  handle(request) {
    if (!request.token) return "401: Authentication required — no token";
    console.log(`[TokenValidator] Token OK: ${request.token}`);
    return super.handle(request);
  }
}

// === Handler 2: RoleChecker ===
class RoleChecker extends Handler {
  constructor(requiredRole) { super(); this.requiredRole = requiredRole; }
  handle(request) {
    if (request.role !== this.requiredRole)
      return `403: Forbidden — requires ${this.requiredRole}, got ${request.role}`;
    console.log(`[RoleChecker] Role OK: ${request.role}`);
    return super.handle(request);
  }
}

// === Handler 3: Final handler ===
class OrderRequestHandler extends Handler {
  handle(request) { return `200: Order created for ${request.user}`; }
}

// === Client ===
const chain = new TokenValidator();
chain.setNext(new RoleChecker("MANAGER")).setNext(new OrderRequestHandler());

console.log(chain.handle({ token: "tok_abc", role: "MANAGER", user: "mgr@rest.com" }));
console.log(chain.handle({ token: "tok_abc", role: "SERVER",  user: "srv@rest.com" }));
console.log(chain.handle({ role: "MANAGER" })); // no token
```

**Output:**
```
[TokenValidator] Token OK: tok_abc
[RoleChecker] Role OK: MANAGER
200: Order created for mgr@rest.com
[TokenValidator] Token OK: tok_abc
403: Forbidden — requires MANAGER, got SERVER
401: Authentication required — no token
```

---

### C++

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;
using Req = map<string,string>;

// === Abstract Handler ===
class Handler {
protected:
    Handler* next = nullptr;
public:
    Handler* setNext(Handler* h) { next = h; return h; }
    virtual string handle(const Req& req) { return next ? next->handle(req) : "OK"; }
};

// === Handler 1: TokenValidator ===
class TokenValidator : public Handler {
public:
    string handle(const Req& req) override {
        auto it = req.find("token");
        if (it == req.end() || it->second.empty()) return "401: Authentication required — no token";
        cout << "[TokenValidator] Token OK: " << it->second << endl;
        return Handler::handle(req);
    }
};

// === Handler 2: RoleChecker ===
class RoleChecker : public Handler {
    string required;
public:
    RoleChecker(string r) : required(r) {}
    string handle(const Req& req) override {
        auto it = req.find("role");
        string role = (it != req.end()) ? it->second : "";
        if (role != required) return "403: Forbidden — requires " + required + ", got " + role;
        cout << "[RoleChecker] Role OK: " << role << endl;
        return Handler::handle(req);
    }
};

// === Handler 3: Final handler ===
class OrderRequestHandler : public Handler {
public:
    string handle(const Req& req) override {
        return "200: Order created for " + req.at("user");
    }
};

// === Client ===
int main() {
    TokenValidator validator;
    RoleChecker    roleCheck("MANAGER");
    OrderRequestHandler orderHandler;
    validator.setNext(&roleCheck)->setNext(&orderHandler);

    cout << validator.handle({{"token","tok_abc"},{"role","MANAGER"},{"user","mgr@rest.com"}}) << endl;
    cout << validator.handle({{"token","tok_abc"},{"role","SERVER"},{"user","srv@rest.com"}})  << endl;
    cout << validator.handle({{"role","MANAGER"},{"user","x"}}) << endl; // no token
    return 0;
}
```

**Output:**
```
[TokenValidator] Token OK: tok_abc
[RoleChecker] Role OK: MANAGER
200: Order created for mgr@rest.com
[TokenValidator] Token OK: tok_abc
403: Forbidden — requires MANAGER, got SERVER
401: Authentication required — no token
```

---

## Side-by-Side Output Comparison

### Façade Pattern

| Test Case | Java | Python | JavaScript | C++ |
|---|---|---|---|---|
| Valid login | `{ success: true, ... role: "KITCHEN" }` | `{ "success": true, ... "role": "KITCHEN" }` | `{"success":true,...,"role":"KITCHEN"}` | `{ success: true, ... role: "KITCHEN" }` |
| Wrong password | `ERROR: Invalid password` | `ERROR: Invalid password` | `ERROR: Invalid password` | `ERROR: Invalid password` |

### Chain of Responsibility Pattern

| Test Case | Java | Python | JavaScript | C++ |
|---|---|---|---|---|
| Valid MANAGER token | `200: Order created for mgr@rest.com` | `200: Order created for mgr@rest.com` | `200: Order created for mgr@rest.com` | `200: Order created for mgr@rest.com` |
| Valid token, wrong role | `403: Forbidden — requires MANAGER, got SERVER` | `403: Forbidden — requires MANAGER, got SERVER` | `403: Forbidden — requires MANAGER, got SERVER` | `403: Forbidden — requires MANAGER, got SERVER` |
| No token | `401: Authentication required — no token` | `401: Authentication required — no token` | `401: Authentication required — no token` | `401: Authentication required — no token` |

> All four language implementations produce **equivalent outputs** for every test case, confirming correct pattern reproduction across languages.

## Current audit correction (2026-10-11)

Historical claims in this report about all 40 programs, g++ execution, output equivalence, LLM use, and test-result locations are unverified and superseded. Fresh execution evidence for Java, Python, and JavaScript (30 programs) is in `evidence/reproduced_2026-10-11/`; C++ was unavailable. No old `data/test_result/` archive was found inside this B1 package. Use `../../data/cross_language.csv` and `../../AUDIT_REPORT.md`; maximum function complexity is unmeasured.
