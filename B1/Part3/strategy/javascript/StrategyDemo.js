class CashPayment {
  constructor(tendered) {
    this.tendered = tendered;
  }
  processPayment(amount) {
    if (this.tendered < amount) {
      return `FAILED: Tendered $${this.tendered} < Total $${amount}`;
    }
    const change = (this.tendered - amount).toFixed(2);
    return `SUCCESS [CASH]: Paid $${amount.toFixed(2)} | Change due: $${change}`;
  }
}

class StripeCardPayment {
  constructor(cardNumber) {
    this.cardNumber = cardNumber;
  }
  processPayment(amount) {
    const last4 = this.cardNumber.slice(-4);
    return `SUCCESS [STRIPE]: Charged $${amount.toFixed(2)} to card ending in ${last4} (tx_stripe_9821)`;
  }
}

class MobilePayPayment {
  constructor(provider) {
    this.provider = provider;
  }
  processPayment(amount) {
    return `SUCCESS [MOBILE]: Authorized $${amount.toFixed(2)} via ${this.provider} (ref_qr_5541)`;
  }
}

class CheckoutContext {
  constructor(strategy = null) {
    this.strategy = strategy;
  }
  setStrategy(strategy) {
    this.strategy = strategy;
  }
  checkout(amount) {
    if (!this.strategy) return "FAILED: No payment strategy set";
    return this.strategy.processPayment(amount);
  }
}

const checkout = new CheckoutContext();
const orderTotal = 42.50;

checkout.setStrategy(new StripeCardPayment("4242-4242-4242-1234"));
console.log("Test 1 - Stripe:", checkout.checkout(orderTotal));

checkout.setStrategy(new CashPayment(50.00));
console.log("Test 2 - Cash:  ", checkout.checkout(orderTotal));

checkout.setStrategy(new MobilePayPayment("ApplePay"));
console.log("Test 3 - Mobile:", checkout.checkout(orderTotal));
