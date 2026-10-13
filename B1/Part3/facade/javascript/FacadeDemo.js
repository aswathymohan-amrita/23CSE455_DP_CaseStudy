// PART 3 — Facade Pattern — JavaScript
// Run: node FacadeDemo.js

class PasswordChecker {
  verify(plain, stored) { return plain === stored; }
}
class TokenService {
  generate(email, role) { return `tok_${Buffer.from(email).toString('base64')}_${role}`; }
}
class UserRepository {
  constructor() {
    this.db = { "chef@restaurant.com": { password: "secret123", role: "KITCHEN" } };
  }
  findByEmail(email) { return this.db[email] || null; }
}
class AuthFacade {
  constructor() {
    this.checker = new PasswordChecker();
    this.tokenService = new TokenService();
    this.repo = new UserRepository();
  }
  login(email, password) {
    const user = this.repo.findByEmail(email);
    if (!user) return { error: "User not found" };
    if (!this.checker.verify(password, user.password)) return { error: "Invalid password" };
    const token = this.tokenService.generate(email, user.role);
    return { success: true, user: email, token, role: user.role };
  }
}

const facade = new AuthFacade();
console.log("Test 1 - Valid login:   ", facade.login("chef@restaurant.com", "secret123"));
console.log("Test 2 - Wrong password:", facade.login("chef@restaurant.com", "wrongpass"));
console.log("Test 3 - User not found:", facade.login("nobody@restaurant.com", "secret123"));
