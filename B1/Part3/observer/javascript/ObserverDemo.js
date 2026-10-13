class ColdStationDisplay {
  onOrderEvent(eventType, orderId, item, station) {
    if (["COLD", "ALL"].includes(station.toUpperCase())) {
      console.log(`[Cold Station] Received ${eventType} for Order #${orderId}: ${item}`);
    }
  }
}

class HotStationDisplay {
  onOrderEvent(eventType, orderId, item, station) {
    if (["HOT", "ALL"].includes(station.toUpperCase())) {
      console.log(`[Hot Station] Received ${eventType} for Order #${orderId}: ${item}`);
    }
  }
}

class WaiterTerminal {
  onOrderEvent(eventType, orderId, item, station) {
    if (eventType.toUpperCase() === "ITEM_READY") {
      console.log(`[Waiter Terminal] Ready to serve Order #${orderId} (${item} from ${station})`);
    }
  }
}

class KitchenSubject {
  constructor() {
    this.observers = [];
  }
  subscribe(observer) {
    this.observers.push(observer);
  }
  notifyAll(eventType, orderId, item, station) {
    for (const obs of this.observers) {
      obs.onOrderEvent(eventType, orderId, item, station);
    }
  }
}

const kitchen = new KitchenSubject();
kitchen.subscribe(new ColdStationDisplay());
kitchen.subscribe(new HotStationDisplay());
kitchen.subscribe(new WaiterTerminal());

console.log("Test 1 - Dispatch New Salad (COLD):");
kitchen.notifyAll("NEW_ORDER", "101", "Classic Caesar Salad", "COLD");

console.log("Test 2 - Dispatch New Steak (HOT):");
kitchen.notifyAll("NEW_ORDER", "102", "Prime Ribeye Steak", "HOT");

console.log("Test 3 - Mark Steak Ready:");
kitchen.notifyAll("ITEM_READY", "102", "Prime Ribeye Steak", "HOT");
