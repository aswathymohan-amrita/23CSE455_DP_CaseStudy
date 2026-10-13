# PART 3 — Facade Pattern — Python
# Run: python FacadeDemo.py

class PasswordChecker:
    def verify(self, plain: str, stored: str) -> bool:
        return plain == stored

class TokenService:
    def generate(self, email: str, role: str) -> str:
        import base64
        encoded = base64.b64encode(email.encode()).decode()
        return f"tok_{encoded}_{role}"

class UserRepository:
    def __init__(self):
        self._db = {
            "chef@restaurant.com": {"password": "secret123", "role": "KITCHEN"}
        }
    def find_by_email(self, email: str):
        return self._db.get(email)

class AuthFacade:
    def __init__(self):
        self._checker = PasswordChecker()
        self._token   = TokenService()
        self._repo    = UserRepository()

    def login(self, email: str, password: str):
        user = self._repo.find_by_email(email)
        if not user:
            return {"error": "User not found"}
        if not self._checker.verify(password, user["password"]):
            return {"error": "Invalid password"}
        token = self._token.generate(email, user["role"])
        return {"success": True, "user": email, "token": token, "role": user["role"]}

if __name__ == "__main__":
    facade = AuthFacade()
    print("Test 1 - Valid login:   ", facade.login("chef@restaurant.com", "secret123"))
    print("Test 2 - Wrong password:", facade.login("chef@restaurant.com", "wrongpass"))
    print("Test 3 - User not found:", facade.login("nobody@restaurant.com", "secret123"))
