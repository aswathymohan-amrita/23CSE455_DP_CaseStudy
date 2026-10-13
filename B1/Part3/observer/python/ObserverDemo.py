from abc import ABC, abstractmethod
from typing import List

class KitchenObserver(ABC):
    @abstractmethod
    def on_order_event(self, event_type: str, order_id: str, item: str, station: str):
        pass

class ColdStationDisplay(KitchenObserver):
    def on_order_event(self, event_type: str, order_id: str, item: str, station: str):
        if station.upper() in ("COLD", "ALL"):
            print(f"[Cold Station] Received {event_type} for Order #{order_id}: {item}")

class HotStationDisplay(KitchenObserver):
    def on_order_event(self, event_type: str, order_id: str, item: str, station: str):
        if station.upper() in ("HOT", "ALL"):
            print(f"[Hot Station] Received {event_type} for Order #{order_id}: {item}")

class WaiterTerminal(KitchenObserver):
    def on_order_event(self, event_type: str, order_id: str, item: str, station: str):
        if event_type.upper() == "ITEM_READY":
            print(f"[Waiter Terminal] Ready to serve Order #{order_id} ({item} from {station})")

class KitchenSubject:
    def __init__(self):
        self._observers: List[KitchenObserver] = []

    def subscribe(self, observer: KitchenObserver):
        self._observers.append(observer)

    def notify_all(self, event_type: str, order_id: str, item: str, station: str):
        for obs in self._observers:
            obs.on_order_event(event_type, order_id, item, station)

if __name__ == "__main__":
    kitchen = KitchenSubject()
    kitchen.subscribe(ColdStationDisplay())
    kitchen.subscribe(HotStationDisplay())
    kitchen.subscribe(WaiterTerminal())

    print("Test 1 - Dispatch New Salad (COLD):")
    kitchen.notify_all("NEW_ORDER", "101", "Classic Caesar Salad", "COLD")

    print("Test 2 - Dispatch New Steak (HOT):")
    kitchen.notify_all("NEW_ORDER", "102", "Prime Ribeye Steak", "HOT")

    print("Test 3 - Mark Steak Ready:")
    kitchen.notify_all("ITEM_READY", "102", "Prime Ribeye Steak", "HOT")
