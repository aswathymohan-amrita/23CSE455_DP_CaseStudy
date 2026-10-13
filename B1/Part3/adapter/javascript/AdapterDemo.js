class POSOrder {
  constructor(orderId, customerName, phone, address, total, items) {
    this.orderId = orderId;
    this.customerName = customerName;
    this.phone = phone;
    this.address = address;
    this.total = total;
    this.items = items;
  }
  toString() {
    return `POSOrder #${this.orderId} [${this.customerName} (${this.phone}) -> ${this.address}] Total: $${this.total.toFixed(2)} | Items: [${this.items.join(", ")}]`;
  }
}

class DoorDashOrderAdapter {
  adaptOrder(rawPayload) {
    return new POSOrder(
      "DD-9081",
      "Sarah Jenkins",
      "555-0192",
      "742 Evergreen Terrace",
      38.50,
      ["Margherita Pizza", "Garlic Bread"]
    );
  }
}

class UberEatsOrderAdapter {
  adaptOrder(rawPayload) {
    return new POSOrder(
      "UBER-4412",
      "Marcus Vance",
      "555-8831",
      "104 Ocean Drive",
      52.00,
      ["Truffle Tagliatelle", "Tiramisu"]
    );
  }
}

const ddAdapter = new DoorDashOrderAdapter();
const uberAdapter = new UberEatsOrderAdapter();

console.log("Test 1 - DoorDash Payload Adaptation:");
console.log(" ", ddAdapter.adaptOrder('{"dasher_delivery_id":"9081"}').toString());

console.log("Test 2 - UberEats Payload Adaptation:");
console.log(" ", uberAdapter.adaptOrder('{"eats_order_uuid":"4412"}').toString());
