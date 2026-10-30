"""Strategy: Sign-in Provider Strategy (NextAuth providers)."""
from __future__ import annotations

import re


class GoogleProvider:
    id = "google"

    def authorize(self, credential: str) -> str | None:
        return f"google:{credential[2:]}" if credential.startswith("g-") else None


class GithubProvider:
    id = "github"

    def authorize(self, credential: str) -> str | None:
        return f"github:{credential[3:]}" if credential.startswith("gh-") else None


class EmailProvider:
    id = "email"
    _PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    def authorize(self, credential: str) -> str | None:
        return f"email:{credential.lower()}" if self._PATTERN.fullmatch(credential) else None


REGISTRY = {cls.id: cls for cls in (GoogleProvider, GithubProvider, EmailProvider)}


class NextAuth:
    """Context: holds the configured strategies and delegates sign-in to one of them."""

    def __init__(self, provider_ids: list[str]) -> None:
        self._providers = {}
        for pid in provider_ids:
            if pid not in REGISTRY:
                raise ValueError(f"unsupported provider {pid}")
            self._providers[pid] = REGISTRY[pid]()

    def sign_in(self, provider_id: str, credential: str) -> str:
        provider = self._providers.get(provider_id)
        if provider is None:
            return "ERR:unknown provider"
        profile = provider.authorize(credential)
        return f"OK:{profile}" if profile else "ERR:invalid credentials"
