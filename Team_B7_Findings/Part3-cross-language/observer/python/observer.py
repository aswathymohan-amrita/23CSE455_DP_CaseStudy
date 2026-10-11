from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Event:
    type: str


class Observer(ABC):
    @abstractmethod
    def update(self, event: Event) -> None:
        raise NotImplementedError


class EventSubject(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def publish(self, event: Event) -> None:
        raise NotImplementedError


class Publisher(EventSubject):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, event: Event) -> None:
        for observer in tuple(self._observers):
            observer.update(event)


class RecordingObserver(Observer):
    def __init__(self) -> None:
        self.received_events: list[Event] = []

    def update(self, event: Event) -> None:
        self.received_events.append(event)
