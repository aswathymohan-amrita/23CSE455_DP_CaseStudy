# PART 3 — Chain of Responsibility Pattern — Python
# Run: python CoRDemo.py

from abc import ABC, abstractmethod
from typing import Optional

class Handler(ABC):
    def __init__(self):
        self._next: Optional["Handler"] = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: dict) -> str: ...

class TokenValidator(Handler):
    def handle(self, request: dict) -> str:
        token = request.get("token", "")
        if not token or not token.startswith("tok_"):
            return "401: Authentication required — no valid token"
        print(f"  [TokenValidator] Token OK: {token}")
        return self._next.handle(request) if self._next else "OK"

class RoleChecker(Handler):
    def __init__(self, required_role: str):
        super().__init__()
        self._required = required_role

    def handle(self, request: dict) -> str:
        if request.get("role") != self._required:
            return f"403: Forbidden — requires {self._required}, got {request.get('role')}"
        print(f"  [RoleChecker]   Role OK: {request['role']}")
        return self._next.handle(request) if self._next else "OK"

class OrderRequestHandler(Handler):
    def handle(self, request: dict) -> str:
        return f"200: Order created for {request.get('user')}"

if __name__ == "__main__":
    # Assemble chain
    validator = TokenValidator()
    role_checker = RoleChecker("MANAGER")
    order_handler = OrderRequestHandler()
    validator.set_next(role_checker).set_next(order_handler)

    print("Test 1 - Valid MANAGER:")
    print(" ", validator.handle({"token": "tok_abc", "role": "MANAGER", "user": "mgr@rest.com"}))
    print("Test 2 - Wrong role (SERVER):")
    print(" ", validator.handle({"token": "tok_abc", "role": "SERVER",  "user": "srv@rest.com"}))
    print("Test 3 - No token:")
    print(" ", validator.handle({"token": "",         "role": "MANAGER", "user": "x@rest.com"}))
