class AvailableState {
  occupy(ctx) {
    console.log("  Action: Seating party -> Transition to OCCUPIED");
    ctx.state = new OccupiedState();
  }
  placeOrder(ctx) {
    console.log("  Error: Cannot place order on empty table!");
  }
  requestBill(ctx) {
    console.log("  Error: No bill on empty table!");
  }
  settleAndClean(ctx) {
    console.log("  Note: Table is already available.");
  }
  getStatusName() { return "AVAILABLE"; }
}

class OccupiedState {
  occupy(ctx) {
    console.log("  Error: Table is already occupied!");
  }
  placeOrder(ctx) {
    console.log("  Action: Waiter sent order to kitchen -> Transition to ORDER_PLACED");
    ctx.state = new OrderPlacedState();
  }
  requestBill(ctx) {
    console.log("  Error: Order must be placed before requesting bill!");
  }
  settleAndClean(ctx) {
    console.log("  Action: Guests left before ordering -> Transition to AVAILABLE");
    ctx.state = new AvailableState();
  }
  getStatusName() { return "OCCUPIED"; }
}

class OrderPlacedState {
  occupy(ctx) {
    console.log("  Error: Table is already occupied with an active order!");
  }
  placeOrder(ctx) {
    console.log("  Action: Added more items to existing order.");
  }
  requestBill(ctx) {
    console.log("  Action: Printed guest bill -> Transition to BILLED");
    ctx.state = new BilledState();
  }
  settleAndClean(ctx) {
    console.log("  Error: Must pay bill before cleaning!");
  }
  getStatusName() { return "ORDER_PLACED"; }
}

class BilledState {
  occupy(ctx) {
    console.log("  Error: Table is currently in payment phase!");
  }
  placeOrder(ctx) {
    console.log("  Error: Bill already printed; re-open order first.");
  }
  requestBill(ctx) {
    console.log("  Action: Re-printed bill receipt.");
  }
  settleAndClean(ctx) {
    console.log("  Action: Payment received, table sanitized -> Transition to AVAILABLE");
    ctx.state = new AvailableState();
  }
  getStatusName() { return "BILLED"; }
}

class TableContext {
  constructor(tableNumber) {
    this.tableNumber = tableNumber;
    this.state = new AvailableState();
  }
  getStatus() { return this.state.getStatusName(); }
  occupy() { this.state.occupy(this); }
  placeOrder() { this.state.placeOrder(this); }
  requestBill() { this.state.requestBill(this); }
  settleAndClean() { this.state.settleAndClean(this); }
}

const table = new TableContext(5);
console.log(`Initial State: Table #5 is ${table.getStatus()}`);

console.log("Test 1: Seating guests");
table.occupy();
console.log("State:", table.getStatus());

console.log("Test 2: Placing order");
table.placeOrder();
console.log("State:", table.getStatus());

console.log("Test 3: Requesting bill");
table.requestBill();
console.log("State:", table.getStatus());

console.log("Test 4: Settling bill and cleaning");
table.settleAndClean();
console.log(`Final State: Table #5 is ${table.getStatus()}`);
