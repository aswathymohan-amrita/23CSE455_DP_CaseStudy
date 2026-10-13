/**
 * PART 2 — EVOLUTION 1: ONLINE ORDERING DEMO
 *
 * Shows how the Facade (OrderService) and Chain of Responsibility
 * are EXTENDED to support public online orders alongside in-house orders.
 *
 * Run: node evolution1_online_ordering.js
 */

// ─────────────────────────────────────────
// BEFORE: In-house only (requires authenticated user)
// ─────────────────────────────────────────

class AuthenticateMiddleware {
  setNext(h) { this._next = h; return h; }
  handle(req) {
    if (!req.token) return { status: 401, body: { error: 'Token required' } };
    console.log('  [authenticate] Token verified ✓');
    req.user = { email: req.staffEmail, role: req.role };
    return this._next?.handle(req) ?? null;
  }
}

class AuthorizeMiddleware {
  constructor(roles) { this._roles = roles; }
  setNext(h) { this._next = h; return h; }
  handle(req) {
    if (!this._roles.includes(req.user?.role))
      return { status: 403, body: { error: `Role ${req.user?.role} not authorized` } };
    console.log(`  [authorize]   Role ${req.user.role} allowed ✓`);
    return this._next?.handle(req) ?? null;
  }
}

// ─────────────────────────────────────────
// FACADE — BEFORE (staff-only)
// ─────────────────────────────────────────
class OrderServiceBefore {
  createOrder(data) {
    console.log(`  [OrderService] STAFF order created → table ${data.tableId}`);
    return { id: `ord_${Date.now()}`, source: 'IN_HOUSE', ...data };
  }
}

// ─────────────────────────────────────────
// EXTENDED FACADE — AFTER (+ online path)
// ─────────────────────────────────────────
class OrderServiceAfter {
  createOrder(data) {                        // unchanged — staff path
    console.log(`  [OrderService] STAFF order created → table ${data.tableId}`);
    return { id: `ord_${Date.now()}`, source: 'IN_HOUSE', ...data };
  }
  createOnlineOrder(data) {                  // NEW — public path
    if (!data.customerEmail) return { error: 'customerEmail required' };
    if (!data.items?.length) return { error: 'items required' };
    console.log(`  [OrderService] ONLINE order created → customer ${data.customerEmail}`);
    return { id: `ord_${Date.now()}`, source: 'ONLINE', status: 'PENDING', ...data };
  }
}

// ─────────────────────────────────────────
// NEW HANDLER — validateOnlineOrder (replaces auth chain for public path)
// ─────────────────────────────────────────
class ValidateOnlineOrderHandler {
  setNext(h) { this._next = h; return h; }
  handle(req) {
    if (!req.customerEmail) return { status: 400, body: { error: 'customerEmail required' } };
    if (!req.items?.length) return { status: 400, body: { error: 'items are required' } };
    console.log(`  [validateOnlineOrder] Input valid ✓`);
    return this._next?.handle(req) ?? null;
  }
}

class OnlineOrderRouteHandler {
  constructor(svc) { this._svc = svc; }
  setNext(h) { return h; }
  handle(req) {
    const order = this._svc.createOnlineOrder(req);
    return { status: 201, body: order };
  }
}

class StaffOrderRouteHandler {
  constructor(svc) { this._svc = svc; }
  setNext(h) { return h; }
  handle(req) {
    const order = this._svc.createOrder(req);
    return { status: 201, body: order };
  }
}

// ─────────────────────────────────────────
// Demo
// ─────────────────────────────────────────
console.log('\n===== EVOLUTION 1: ONLINE ORDERING =====\n');

const orderSvc = new OrderServiceAfter();

// ── BEFORE: Staff chain ──────────────────
const auth     = new AuthenticateMiddleware();
const authorize = new AuthorizeMiddleware(['SERVER','MANAGER']);
const staffHandler = new StaffOrderRouteHandler(orderSvc);
auth.setNext(authorize).setNext(staffHandler);

console.log('--- BEFORE: In-house staff order ---');
let res = auth.handle({ token: 'tok_abc', staffEmail: 'alice@rest.com', role: 'SERVER', tableId: 'tbl_3', items: ['Pasta'] });
console.log('  Result:', res, '\n');

// ── AFTER: Online chain ──────────────────
const validate    = new ValidateOnlineOrderHandler();
const onlineRoute = new OnlineOrderRouteHandler(orderSvc);
validate.setNext(onlineRoute);

console.log('--- AFTER: Public online order ---');
res = validate.handle({ customerEmail: 'john@gmail.com', items: ['Burger','Fries'], deliveryAddress: '12 Main St' });
console.log('  Result:', res, '\n');

console.log('--- AFTER: Online order with missing email ---');
res = validate.handle({ items: ['Pizza'] });
console.log('  Result:', res);
