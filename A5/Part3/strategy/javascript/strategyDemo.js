// Part 3 - Strategy demonstration (JavaScript).
// Stripe and PayPal are simulated. This file does not call a network.

class StripePayment {
  processPayment(amount, reference) {
    return { provider: "stripe", reference, amount, status: "paid" };
  }
}

class PayPalPayment {
  processPayment(amount, reference) {
    return { provider: "paypal", reference, amount, status: "paid" };
  }
}

class BillingService {
  constructor(strategy) {
    this.strategy = strategy;
  }

  charge(amount, reference) {
    return this.strategy.processPayment(amount, reference);
  }
}

const stripeResult = new BillingService(new StripePayment()).charge(1200.0, "DX-1001");
const paypalResult = new BillingService(new PayPalPayment()).charge(850.5, "DX-1002");
console.log(stripeResult);
console.log(paypalResult);

if (stripeResult.provider !== "stripe" || paypalResult.provider !== "paypal") {
  process.exit(1);
}
