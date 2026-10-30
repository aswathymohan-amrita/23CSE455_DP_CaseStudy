"""Read-Through Cache: My List Query Cache."""
from __future__ import annotations

from typing import Callable


class QueryCache:
    """Returns the cached value or loads it once (staleTime = infinity)."""

    def __init__(self) -> None:
        self._entries: dict = {}

    def fetch(self, key, loader: Callable):
        if key not in self._entries:
            self._entries[key] = loader()
        return self._entries[key]

    def invalidate(self, key) -> None:
        self._entries.pop(key, None)


class MyListStore:
    """Data source behind the loader (myList router)."""

    def __init__(self) -> None:
        self._lists: dict[str, list[int]] = {}
        self.loads = 0

    def get_all(self, profile_id: str) -> tuple[int, ...]:
        self.loads += 1
        return tuple(self._lists.get(profile_id, []))

    def add(self, profile_id: str, show_id: int) -> None:
        items = self._lists.setdefault(profile_id, [])
        if show_id in items:
            raise LookupError("Show already exists")
        items.append(show_id)

    def remove(self, profile_id: str, show_id: int) -> None:
        items = self._lists.get(profile_id, [])
        if show_id not in items:
            raise LookupError("Show not found")
        items.remove(show_id)
