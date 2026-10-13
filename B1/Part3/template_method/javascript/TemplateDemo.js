class OrderProcessingPipeline {
  processOrder(orderId, subtotal) {
    console.log(`Processing Order #${orderId} (Subtotal: $${subtotal.toFixed(2)})`);
    this.validateOrder();
    const total = this.calculateTotal(subtotal);
    this.sendKitchenTicket(orderId);
    this.notifyCustomer(orderId, total);
    console.log(`Order #${orderId} fulfilled successfully.\n`);
  }

  validateOrder() {
    console.log("  Step 1 [Common]: Verified inventory and active kitchen capacity.");
  }

  sendKitchenTicket(orderId) {
    console.log("  Step 3 [Common]: Dispatched ticket to kitchen display.");
  }

  calculateTotal(subtotal) {
    throw new Error("Must implement calculateTotal");
  }

  notifyCustomer(orderId, finalTotal) {
    throw new Error("Must implement notifyCustomer");
  }
}

class DineInPipeline extends OrderProcessingPipeline {
  constructor(tableNumber) {
    super();
    this.tableNumber = tableNumber;
  }
  calculateTotal(subtotal) {
    const tax = subtotal * 0.0825;
    const total = subtotal + tax;
    console.log(`  Step 2 [Dine-In]: Added 8.25% dine-in tax ($${tax.toFixed(2)}) -> Final: $${total.toFixed(2)}`);
    return total;
  }
  notifyCustomer(orderId, finalTotal) {
    console.log(`  Step 4 [Dine-In]: Displayed order on Table #${this.tableNumber} waiter console.`);
  }
}

class OnlineDeliveryPipeline extends OrderProcessingPipeline {
  constructor(deliveryAddress) {
    super();
    this.deliveryAddress = deliveryAddress;
  }
  calculateTotal(subtotal) {
    const tax = subtotal * 0.0825;
    const deliveryFee = 4.99;
    const total = subtotal + tax + deliveryFee;
    console.log(`  Step 2 [Delivery]: Added tax ($${tax.toFixed(2)}) + $4.99 delivery fee -> Final: $${total.toFixed(2)}`);
    return total;
  }
  notifyCustomer(orderId, finalTotal) {
    console.log(`  Step 4 [Delivery]: Sent SMS tracking link to courier en route to ${this.deliveryAddress}`);
  }
}

const dineIn = new DineInPipeline(8);
console.log("--- Test 1: Dine-In Pipeline ---");
dineIn.processOrder("DINE-301", 50.00);

const delivery = new OnlineDeliveryPipeline("450 Elm Street");
console.log("--- Test 2: Online Delivery Pipeline ---");
delivery.processOrder("DELV-902", 50.00);
