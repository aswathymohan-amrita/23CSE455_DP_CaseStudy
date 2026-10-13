// PART 3 — Chain of Responsibility Pattern — JavaScript
// Run: node CoRDemo.js

class Handler {
  setNext(h) { this._next = h; return h; }
  handle(req) { return this._next ? this._next.handle(req) : "OK"; }
}

class TokenValidator extends Handler {
  handle(req) {
    if (!req.token || !req.token.startsWith("tok_"))
      return "401: Authentication required — no valid token";
    console.log(`  [TokenValidator] Token OK: ${req.token}`);
    return super.handle(req);
  }
}

class RoleChecker extends Handler {
  constructor(requiredRole) { super(); this.requiredRole = requiredRole; }
  handle(req) {
    if (req.role !== this.requiredRole)
      return `403: Forbidden — requires ${this.requiredRole}, got ${req.role}`;
    console.log(`  [RoleChecker]   Role OK: ${req.role}`);
    return super.handle(req);
  }
}

class OrderRequestHandler extends Handler {
  handle(req) { return `200: Order created for ${req.user}`; }
}

// Assemble chain
const chain = new TokenValidator();
chain.setNext(new RoleChecker("MANAGER")).setNext(new OrderRequestHandler());

console.log("Test 1 - Valid MANAGER:");
console.log(" ", chain.handle({ token: "tok_abc", role: "MANAGER", user: "mgr@rest.com" }));
console.log("Test 2 - Wrong role (SERVER):");
console.log(" ", chain.handle({ token: "tok_abc", role: "SERVER",  user: "srv@rest.com" }));
console.log("Test 3 - No token:");
console.log(" ", chain.handle({ token: "",         role: "MANAGER", user: "x@rest.com"  }));
