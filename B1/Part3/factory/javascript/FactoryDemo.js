class DineInTicket {
  constructor(tableNumber, serverName) {
    this.tableNumber = tableNumber;
    this.serverName = serverName;
  }
  formatTicket(orderId, items) {
    return `[DINE-IN TICKET #${orderId}] Table: ${this.tableNumber} | Server: ${this.serverName} | Priority: NORMAL | Items: [${items.join(", ")}]`;
  }
}

class TakeoutTicket {
  constructor(pickupName) {
    this.pickupName = pickupName;
  }
  formatTicket(orderId, items) {
    return `[TAKEOUT TICKET #${orderId}] Customer: ${this.pickupName} | Packaging: BAG & UTENSILS | Items: [${items.join(", ")}]`;
  }
}

class DeliveryTicket {
  constructor(courier, address) {
    this.courier = courier;
    this.address = address;
  }
  formatTicket(orderId, items) {
    return `[DELIVERY TICKET #${orderId}] Courier: ${this.courier} | Address: ${this.address} | SEAL REQUIRED | Items: [${items.join(", ")}]`;
  }
}

class TicketFactory {
  static createDineInTicket(tableNumber, server) {
    return new DineInTicket(tableNumber, server);
  }
  static createTakeoutTicket(customer) {
    return new TakeoutTicket(customer);
  }
  static createDeliveryTicket(courier, address) {
    return new DeliveryTicket(courier, address);
  }
}

const items = ["Burger", "Fries", "Coke"];

const t1 = TicketFactory.createDineInTicket(4, "Alex");
console.log("Test 1:", t1.formatTicket("101", items));

const t2 = TicketFactory.createTakeoutTicket("Emily R.");
console.log("Test 2:", t2.formatTicket("102", items));

const t3 = TicketFactory.createDeliveryTicket("DoorDash", "12 Maple St");
console.log("Test 3:", t3.formatTicket("103", items));
