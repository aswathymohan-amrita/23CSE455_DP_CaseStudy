"""Send saved auth events to a listener and support unsubscribe."""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any


class Subscription:
    def __init__(self, unsubscribe_action: Callable[[], None]) -> None:
        self._unsubscribe_action = unsubscribe_action

    def unsubscribe(self) -> None:
        self._unsubscribe_action()


class AuthSubject:
    def __init__(self) -> None:
        self._listeners: list[Callable[[dict[str, Any]], None]] = []

    def subscribe(self, listener: Callable[[dict[str, Any]], None]) -> Subscription:
        self._listeners.append(listener)
        return Subscription(lambda: self._listeners.remove(listener) if listener in self._listeners else None)

    def publish(self, event: dict[str, Any]) -> None:
        for listener in tuple(self._listeners):
            listener(event)


class AuthStateObserver:
    def __init__(self) -> None:
        self.user_id: str | None = None
        self.observed_users: list[str | None] = []

    def on_auth_change(self, event: dict[str, Any]) -> None:
        self.user_id = None if event["event"] == "SIGNED_OUT" else event["user_id"]
        self.observed_users.append(self.user_id)


def run(input_data: Any) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        return {"error": "input must be an object"}
    events = input_data.get("events")
    if not isinstance(events, list):
        return {"error": "events must be an array"}
    unsubscribe_after = input_data.get("unsubscribe_after")
    if unsubscribe_after is not None and (
        isinstance(unsubscribe_after, bool)
        or not isinstance(unsubscribe_after, (int, float))
        or unsubscribe_after < 0
        or unsubscribe_after > 9007199254740991
        or not math.isfinite(unsubscribe_after)
        or not float(unsubscribe_after).is_integer()
    ):
        return {"error": "unsubscribe_after must be a non-negative integer or null"}
    if unsubscribe_after is not None:
        unsubscribe_after = int(unsubscribe_after)
    for event in events:
        if not isinstance(event, dict):
            return {"error": "each event must be an object"}
        event_type = event.get("event")
        if event_type not in ("SIGNED_IN", "TOKEN_REFRESHED", "SIGNED_OUT"):
            return {"error": "unsupported auth event"}
        if event_type == "SIGNED_OUT":
            if event.get("user_id") is not None:
                return {"error": "SIGNED_OUT user_id must be null or absent"}
        elif not isinstance(event.get("user_id"), str) or not event["user_id"]:
            return {"error": "user_id must be a non-empty string"}

    subject = AuthSubject()
    observer = AuthStateObserver()
    subscription = subject.subscribe(observer.on_auth_change)
    for index, event in enumerate(events):
        if unsubscribe_after is not None and index == unsubscribe_after:
            subscription.unsubscribe()
        subject.publish(event)
    return {
        "observed_users": observer.observed_users,
        "final_user_id": observer.user_id,
        "notification_count": len(observer.observed_users),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python implementation.py INPUT_JSON")
    with Path(sys.argv[1]).open(encoding="utf-8") as source:
        print(json.dumps(run(json.load(source)), ensure_ascii=False))
