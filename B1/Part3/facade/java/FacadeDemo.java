// PART 3 — Facade Pattern — Java
// Compile: javac FacadeDemo.java
// Run:     java FacadeDemo

import java.util.HashMap;
import java.util.Map;
import java.util.Base64;

// Subsystem 1: PasswordChecker
class PasswordChecker {
    public boolean verify(String plain, String stored) {
        return plain.equals(stored);
    }
}

// Subsystem 2: TokenService
class TokenService {
    public String generate(String email, String role) {
        String encoded = Base64.getEncoder().encodeToString(email.getBytes());
        return "tok_" + encoded + "_" + role;
    }
}

// Subsystem 3: UserRepository
class UserRepository {
    private Map<String, String[]> db = new HashMap<>();
    public UserRepository() {
        db.put("chef@restaurant.com", new String[]{"secret123", "KITCHEN"});
    }
    public String[] findByEmail(String email) { return db.get(email); }
}

// Facade
class AuthFacade {
    private PasswordChecker checker = new PasswordChecker();
    private TokenService tokenService = new TokenService();
    private UserRepository repo = new UserRepository();

    public String login(String email, String password) {
        String[] user = repo.findByEmail(email);
        if (user == null) return "{\"error\": \"User not found\"}";
        if (!checker.verify(password, user[0])) return "{\"error\": \"Invalid password\"}";
        String token = tokenService.generate(email, user[1]);
        return "{\"success\": true, \"user\": \"" + email + "\", \"token\": \"" + token + "\", \"role\": \"" + user[1] + "\"}";
    }
}

// Client
public class FacadeDemo {
    public static void main(String[] args) {
        AuthFacade facade = new AuthFacade();
        System.out.println("Test 1 - Valid login:    " + facade.login("chef@restaurant.com", "secret123"));
        System.out.println("Test 2 - Wrong password: " + facade.login("chef@restaurant.com", "wrongpass"));
        System.out.println("Test 3 - User not found: " + facade.login("nobody@restaurant.com", "secret123"));
    }
}
