// PART 3 — Chain of Responsibility Pattern — Java
// Compile: javac CoRDemo.java
// Run:     java CoRDemo

import java.util.Map;

// Abstract handler
abstract class RequestHandler {
    protected RequestHandler next;
    public RequestHandler setNext(RequestHandler next) { this.next = next; return next; }
    public abstract String handle(Map<String, String> request);
}

// Handler 1: Token Validator
class TokenValidator extends RequestHandler {
    public String handle(Map<String, String> req) {
        String token = req.getOrDefault("token", "");
        if (token.isEmpty() || !token.startsWith("tok_"))
            return "401: Authentication required — no valid token";
        System.out.println("  [TokenValidator] Token OK: " + token);
        return next != null ? next.handle(req) : "OK";
    }
}

// Handler 2: Role Checker
class RoleChecker extends RequestHandler {
    private final String requiredRole;
    public RoleChecker(String requiredRole) { this.requiredRole = requiredRole; }
    public String handle(Map<String, String> req) {
        String role = req.getOrDefault("role", "");
        if (!requiredRole.equals(role))
            return "403: Forbidden — requires " + requiredRole + ", got " + role;
        System.out.println("  [RoleChecker]   Role OK: " + role);
        return next != null ? next.handle(req) : "OK";
    }
}

// Handler 3: Final handler
class OrderHandler extends RequestHandler {
    public String handle(Map<String, String> req) {
        return "200: Order created for " + req.getOrDefault("user", "unknown");
    }
}

public class CoRDemo {
    public static void main(String[] args) {
        // Assemble chain
        TokenValidator validator = new TokenValidator();
        RoleChecker roleChecker = new RoleChecker("MANAGER");
        OrderHandler orderHandler = new OrderHandler();
        validator.setNext(roleChecker).setNext(orderHandler);

        System.out.println("Test 1 - Valid MANAGER:");
        System.out.println("  " + validator.handle(Map.of("token", "tok_abc", "role", "MANAGER", "user", "mgr@rest.com")));
        System.out.println("Test 2 - Wrong role (SERVER):");
        System.out.println("  " + validator.handle(Map.of("token", "tok_abc", "role", "SERVER",  "user", "srv@rest.com")));
        System.out.println("Test 3 - No token:");
        System.out.println("  " + validator.handle(Map.of("token", "",         "role", "MANAGER", "user", "x@rest.com")));
    }
}
