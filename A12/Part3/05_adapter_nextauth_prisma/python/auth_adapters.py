"""Adapter: NextAuth Prisma Persistence Adapter."""
from __future__ import annotations


class OrmError(Exception):
    pass


class _UserTable:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def create(self, data: dict) -> dict:
        if self.find_unique({"email": data["email"]}):
            raise OrmError("unique email")
        row = {"id": f"u{len(self.rows) + 1}", **data}
        self.rows.append(row)
        return row

    def find_unique(self, where: dict) -> dict | None:
        return next((r for r in self.rows if r["email"] == where["email"]), None)


class _AccountTable:
    def __init__(self, users: _UserTable) -> None:
        self.rows: list[dict] = []
        self._users = users

    def create(self, data: dict) -> dict:
        if not any(u["id"] == data["userId"] for u in self._users.rows):
            raise OrmError("foreign key")
        row = {"id": f"a{len(self.rows) + 1}", **data}
        self.rows.append(row)
        return row


class OrmClient:
    """Adaptee: Prisma-like client (orm.user.create(data), orm.user.find_unique(where))."""

    def __init__(self) -> None:
        self.user = _UserTable()
        self.account = _AccountTable(self.user)


class PrismaAdapter:
    """Adapter implementing the auth library's Target interface on top of OrmClient."""

    def __init__(self, orm: OrmClient) -> None:
        self._orm = orm

    def create_user(self, email: str, name: str) -> dict:
        return self._orm.user.create({"email": email, "name": name})

    def get_user_by_email(self, email: str) -> dict | None:
        return self._orm.user.find_unique({"email": email})

    def link_account(self, user_id: str, provider: str) -> dict:
        return self._orm.account.create({"userId": user_id, "provider": provider})
