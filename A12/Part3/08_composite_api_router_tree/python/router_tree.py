"""Composite: API Router Tree (appRouter with sub-routers and procedures, after CH01)."""
from __future__ import annotations


class Procedure:
    """Leaf."""

    def __init__(self, kind: str) -> None:
        self.kind = kind

    def count(self) -> int:
        return 1

    def resolve(self, parts: list[str]):
        return self if not parts else None

    def paths(self, prefix: str) -> list[str]:
        return [prefix]

    def depth(self) -> int:
        return 0


class Router:
    """Composite."""

    def __init__(self, **children) -> None:
        self.children = dict(children)  # keyword order = tree order

    def count(self) -> int:
        return sum(child.count() for child in self.children.values())

    def resolve(self, parts: list[str]):
        if not parts:
            return self
        child = self.children.get(parts[0])
        return child.resolve(parts[1:]) if child else None

    def paths(self, prefix: str) -> list[str]:
        return [p for name, child in self.children.items()
                for p in child.paths(f"{prefix}.{name}" if prefix else name)]

    def depth(self) -> int:
        return 1 + max((child.depth() for child in self.children.values()), default=-1)


def app_router() -> Router:
    q, m = Procedure("query"), Procedure("mutation")
    return Router(
        user=Router(getSession=q, getCurrent=q, getCurrentWithProfile=q, update=m),
        profile=Router(getAll=q, getOthers=q, getOne=q, create=m, update=m, updatePin=m, delete=m),
        icon=Router(getAll=q, getAllUsed=q, getAllUnused=q, getCurrent=q),
        myList=Router(getAll=q, create=m, update=m, delete=m),
        catalogue=Router(checkAccess=q),
    )
