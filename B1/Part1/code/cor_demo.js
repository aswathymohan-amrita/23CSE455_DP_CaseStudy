/**
 * PART 1 — CHAIN OF RESPONSIBILITY DEMO
 * Mirrors the exact structure found in:
 *   src/middleware/auth.ts  (authenticate + authorize)
 *   src/index.ts            (app.use chain assembly)
 *
 * Run: node cor_demo.js
 */

// ─────────────────────────────────────────
// Abstract Handler base
// ─────────────────────────────────────────
class Handler {
  setNext(handler) { this._next = handler; return handler; }
  handle(req) { return this._next ? this._next.handle(req) : null; }
}

// ─────────────────────────────────────────
// HANDLER 1 — TokenValidator  (≈ authenticate middleware)
// ─────────────────────────────────────────
class TokenValidator extends Handler {
  handle(req) {
    if (!req.token || req.token.trim() === '') {
      return { status: 401, body: { error: 'Authentication required — no token provided' } };
    }
    // Simulate jwt.verify — accept any token starting with 'tok_'
    if (!req.token.startsWith('tok_')) {
      return { status: 401, body: { error: 'Invalid or expired token' } };
    }
    console.log('  [authenticate] Token verified ✓');
    req.user = { email: req.email, role: req.role };  // attach user to request
    return super.handle(req);
  }
}

// ─────────────────────────────────────────
// HANDLER 2 — RoleChecker  (≈ authorize middleware)
// ─────────────────────────────────────────
class RoleChecker extends Handler {
  constructor(allowedRoles) { super(); this._allowed = allowedRoles; }
  handle(req) {
    if (!req.user || !this._allowed.includes(req.user.role)) {
      return {
        status: 403,
        body: { error: `Forbidden — requires one of [${this._allowed}], got ${req.user?.role}` }
      };
    }
    console.log(`  [authorize]   Role '${req.user.role}' is permitted ✓`);
    return super.handle(req);
  }
}

// ─────────────────────────────────────────
// HANDLER 3 — Final route handler
// ─────────────────────────────────────────
class OrderRouteHandler extends Handler {
  handle(req) {
    console.log(`  [route]       Processing order for ${req.user.email} ✓`);
    return { status: 200, body: { message: `Order created for ${req.user.email}` } };
  }
}

// ─────────────────────────────────────────
// Assemble the Chain  (≈ index.ts app.use)
//   authenticate → authorize(['MANAGER','ADMIN']) → orderRoutes
// ─────────────────────────────────────────
function buildChain(allowedRoles) {
  const tokenValidator = new TokenValidator();
  const roleChecker    = new RoleChecker(allowedRoles);
  const orderHandler   = new OrderRouteHandler();
  tokenValidator.setNext(roleChecker).setNext(orderHandler);
  return tokenValidator;
}

// ─────────────────────────────────────────
// CLIENT — simulate HTTP requests hitting the chain
// ─────────────────────────────────────────
const chain = buildChain(['MANAGER', 'ADMIN']);

const testCases = [
  { label: 'Valid MANAGER with token',    token: 'tok_mgr_abc', role: 'MANAGER', email: 'mgr@rest.com' },
  { label: 'Valid SERVER — wrong role',   token: 'tok_srv_xyz', role: 'SERVER',  email: 'srv@rest.com' },
  { label: 'No token at all',             token: '',            role: 'MANAGER', email: 'x@rest.com'   },
  { label: 'Malformed / invalid token',   token: 'BADTOKEN',    role: 'ADMIN',   email: 'a@rest.com'   },
];

console.log('\n===== CHAIN OF RESPONSIBILITY DEMO (mirrors middleware/auth.ts) =====\n');

for (const tc of testCases) {
  console.log(`[${tc.label}]`);
  const response = chain.handle(tc);
  console.log(`  Response: HTTP ${response.status} →`, response.body);
  console.log();
}
