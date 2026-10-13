class CartReceiver {
  constructor() {
    this.items = [];
    this.discountPercent = 0.0;
  }
  addItem(item) { this.items.push(item); }
  removeItem(item) {
    const idx = this.items.indexOf(item);
    if (idx !== -1) this.items.splice(idx, 1);
  }
  setDiscount(pct) { this.discountPercent = pct; }
  printCart() {
    console.log(`  Cart Items: [${this.items.join(", ")}] | Discount: ${(this.discountPercent * 100).toFixed(0)}%`);
  }
}

class AddItemCommand {
  constructor(cart, item) {
    this.cart = cart;
    this.item = item;
  }
  execute() {
    console.log(`Execute: Add ${this.item}`);
    this.cart.addItem(this.item);
  }
  undo() {
    console.log(`Undo: Remove ${this.item}`);
    this.cart.removeItem(this.item);
  }
}

class ApplyDiscountCommand {
  constructor(cart, newDiscount) {
    this.cart = cart;
    this.newDiscount = newDiscount;
    this.prevDiscount = 0.0;
  }
  execute() {
    this.prevDiscount = this.cart.discountPercent;
    console.log(`Execute: Apply ${(this.newDiscount * 100).toFixed(0)}% Discount`);
    this.cart.setDiscount(this.newDiscount);
  }
  undo() {
    console.log(`Undo: Revert discount back to ${(this.prevDiscount * 100).toFixed(0)}%`);
    this.cart.setDiscount(this.prevDiscount);
  }
}

class POSTerminalInvoker {
  constructor() {
    this.history = [];
  }
  runCommand(cmd) {
    cmd.execute();
    this.history.push(cmd);
  }
  undoLast() {
    if (this.history.length > 0) {
      const cmd = this.history.pop();
      cmd.undo();
    } else {
      console.log("Nothing to undo!");
    }
  }
}

const cart = new CartReceiver();
const pos = new POSTerminalInvoker();

console.log("Step 1: Adding Burger and Fries");
pos.runCommand(new AddItemCommand(cart, "Classic Burger"));
pos.runCommand(new AddItemCommand(cart, "Truffle Fries"));
cart.printCart();

console.log("Step 2: Applying 15% VIP Discount");
pos.runCommand(new ApplyDiscountCommand(cart, 0.15));
cart.printCart();

console.log("Step 3: Cashier pressed Undo (reverting discount)");
pos.undoLast();
cart.printCart();

console.log("Step 4: Cashier pressed Undo (reverting Truffle Fries)");
pos.undoLast();
cart.printCart();
