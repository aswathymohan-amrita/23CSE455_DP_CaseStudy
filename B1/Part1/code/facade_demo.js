/**
 * PART 1 — FACADE PATTERN DEMO
 * Mirrors the exact structure found in:
 *   src/services/auth.service.ts  (AuthService.login)
 *   src/routes/auth.routes.ts     (POST /login)
 *
 * Run: node facade_demo.js
 */

// ─────────────────────────────────────────
// SUBSYSTEM 1 — PasswordChecker  (≈ bcrypt)
// ─────────────────────────────────────────
class PasswordChecker {
  /** Simulates bcrypt.compare() */
  verify(plain, stored) {
    return plain === stored;
  }
}

// ─────────────────────────────────────────
// SUBSYSTEM 2 — TokenService  (≈ jsonwebtoken)
// ─────────────────────────────────────────
class TokenService {
  generate(email, role) {
    const payload = Buffer.from(`${email}:${role}`).toString('base64');
    return `eyJ.${payload}.tok`;   // simulated JWT
  }
}

// ─────────────────────────────────────────
// SUBSYSTEM 3 — UserRepository  (≈ PrismaClient)
// ─────────────────────────────────────────
class UserRepository {
  constructor() {
    this._db = {
      'mgr@restaurant.com':   { password: 'mgr123',    role: 'MANAGER' },
      'chef@restaurant.com':  { password: 'chef123',   role: 'KITCHEN' },
      'server@restaurant.com':{ password: 'serve123',  role: 'SERVER'  },
    };
  }
  findByEmail(email) { return this._db[email] || null; }
}

// ─────────────────────────────────────────
// FACADE — AuthService
// The route only calls this. It knows nothing about the subsystems.
// ─────────────────────────────────────────
class AuthService {
  constructor() {
    this._checker   = new PasswordChecker();
    this._tokenSvc  = new TokenService();
    this._userRepo  = new UserRepository();
  }

  login(email, password) {
    const user = this._userRepo.findByEmail(email);
    if (!user) return { error: 'User not found' };

    if (!this._checker.verify(password, user.password))
      return { error: 'Invalid password' };

    const token = this._tokenSvc.generate(email, user.role);
    return { success: true, user: email, role: user.role, token };
  }
}

// ─────────────────────────────────────────
// CLIENT — Express Route equivalent
// ─────────────────────────────────────────
const authService = new AuthService();   // ← single facade instance

console.log('\n===== FACADE PATTERN DEMO (mirrors auth.service.ts) =====\n');

const testCases = [
  { email: 'mgr@restaurant.com',    password: 'mgr123',   label: 'Valid MANAGER login' },
  { email: 'chef@restaurant.com',   password: 'wrongpass', label: 'Wrong password'      },
  { email: 'nobody@restaurant.com', password: 'pass',      label: 'User not found'      },
];

for (const tc of testCases) {
  const result = authService.login(tc.email, tc.password);
  console.log(`[${tc.label}]`);
  console.log('  Input :', { email: tc.email, password: tc.password });
  console.log('  Output:', result);
  console.log();
}
