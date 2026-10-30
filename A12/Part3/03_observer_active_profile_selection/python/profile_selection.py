"""Observer: Active Profile Selection (profile store notifies subscribed views)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    profile: str = "-"
    maturity: str = "NONE"
    pin_form: bool = False


class ProfileStore:
    """ConcreteSubject: the profile store."""

    def __init__(self) -> None:
        self._observers: dict = {}  # insertion-ordered set
        self.state = State()

    def subscribe(self, observer) -> None:
        self._observers[observer] = None

    def unsubscribe(self, observer) -> None:
        self._observers.pop(observer, None)

    def set_state(self, state: State, out: list[str]) -> None:
        self.state = state
        for observer in self._observers:
            reaction = observer.notify(state)
            if reaction is not None:
                out.append(reaction)


class Hero:
    def notify(self, s: State) -> str:
        return f"Hero:{s.maturity}"


class ShowsContainer:
    def notify(self, s: State) -> str:
        return f"Rows:{s.profile}/{s.maturity}"


class PinForm:
    def notify(self, s: State) -> str | None:
        return f"Pin:{s.profile}" if s.pin_form else None
