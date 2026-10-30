"""Chain of Responsibility: Content Access Rule Chain (Region -> Maturity -> Premium)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Show:
    id: int
    premium: bool
    adult: bool
    genres: frozenset[int]


@dataclass(frozen=True)
class Viewer:
    plan_tier: int
    region: str
    maturity: str


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str | None = None
    visibility: str | None = None

    def __str__(self) -> str:
        return "ALLOW" if self.allowed else f"DENY:{self.reason}:{self.visibility}"


ALLOW = Decision(True)


class AccessRule(ABC):
    """Handler. check() is also a template method; evaluate() is the primitive step."""

    def __init__(self) -> None:
        self._next: AccessRule | None = None

    def set_next(self, rule: AccessRule) -> AccessRule:
        self._next = rule
        return rule

    def check(self, show: Show, viewer: Viewer) -> Decision:
        denial = self.evaluate(show, viewer)
        if denial is not None:
            return denial
        return self._next.check(show, viewer) if self._next else ALLOW

    @abstractmethod
    def evaluate(self, show: Show, viewer: Viewer) -> Decision | None: ...


class RegionRule(AccessRule):
    BLOCKED = {550: {"CN"}}
    ALLOWED = {1399: {"US", "GB", "IN"}}

    def evaluate(self, show, viewer):
        allowed = self.ALLOWED.get(show.id)
        blocked = self.BLOCKED.get(show.id)
        denied = (allowed is not None and viewer.region not in allowed) or (
            blocked is not None and viewer.region in blocked
        )
        return Decision(False, "REGION_BLOCKED", "hidden") if denied else None


class MaturityRule(AccessRule):
    POLICIES = {
        "KIDS": (False, {27, 53, 80, 10752}),
        "TEEN": (False, {27}),
        "ADULT": (True, set()),
        "NONE": (True, set()),
    }

    def evaluate(self, show, viewer):
        if viewer.maturity not in self.POLICIES:
            raise ValueError("unknown maturity")
        allow_adult, blocked = self.POLICIES[viewer.maturity]
        denied = (show.adult and not allow_adult) or bool(show.genres & blocked)
        return Decision(False, "MATURITY_BLOCKED", "hidden") if denied else None


class PremiumContentRule(AccessRule):
    MIN_TIER = 3

    def evaluate(self, show, viewer):
        if show.premium and viewer.plan_tier < self.MIN_TIER:
            return Decision(False, "PREMIUM_REQUIRED", "locked")
        return None


def content_access_chain() -> AccessRule:
    head = RegionRule()
    head.set_next(MaturityRule()).set_next(PremiumContentRule())
    return head
