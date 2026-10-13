/**
 * PART 2 — EVOLUTION 3: MULTIPLE PAYMENT METHODS (Strategy Pattern)
 *
 * Shows how a new STRATEGY pattern is introduced into the Facade-based
 * PaymentService to handle Stripe, Cash, and MobilePay differently.
 *
 * Run: node evolution3_payment_strategy.js
 */

// ─────────────────────────────────────────
// BEFORE — PaymentService (no strategy, same code for all methods)
// ─────────────────────────────────────────
class PaymentServiceBefore {
  createPayment(data) {
    // ⚠ Same code path regardless of payment method
    console.log(`  [PaymentService-BEFORE] Saving payment — method: ${data.method}, amount: $${data.amount}`);
    return { id: `pay_${Date.now()}`, method: data.method, amount: data.amount, status: 'COMPLETED' };
  }
}

// ─────────────────────────────────────────
// AFTER — Strategy Interface + Concrete Strategies
// ─────────────────────────────────────────

// ── Strategy Interface (implicit in JS) ──
class CashStrategy {
  process(amount) {
    console.log(`    [CashStrategy]    Opening cash drawer. Collecting $${amount} cash...`);
    return { transactionId: `cash_${Date.now()}`, method: 'CASH', amount, status: 'COMPLETED' };
  }
  refund(transactionId) {
    console.log(`    [CashStrategy]    Cash refund for ${transactionId} — issue from drawer`);
    return { refunded: true };
  }
}

class StripeCardStrategy {
  process(amount, details) {
    console.log(`    [StripeStrategy]  Calling Stripe API for card ****${details.last4 || '4242'}...`);
    // In real code: await stripe.paymentIntents.create(...)
    return { transactionId: `stripe_pi_${Date.now()}`, method: 'CREDIT_CARD', amount, status: 'COMPLETED' };
  }
  refund(transactionId) {
    console.log(`    [StripeStrategy]  Calling Stripe API refund for ${transactionId}...`);
    return { refunded: true };
  }
}

class MobilePayStrategy {
  process(amount) {
    const qrCode = `QR_${Math.random().toString(36).substring(7).toUpperCase()}`;
    console.log(`    [MobilePayStrategy] Generating QR code: ${qrCode} for $${amount}...`);
    return { transactionId: `mpay_${Date.now()}`, method: 'MOBILE_PAY', amount, status: 'COMPLETED', qrCode };
  }
  refund(transactionId) {
    console.log(`    [MobilePayStrategy] Reversing mobile payment ${transactionId}...`);
    return { refunded: true };
  }
}

class GiftCardStrategy {
  constructor() {
    this._cards = { 'GC-001': 150.00, 'GC-002': 50.00 }; // mock gift card balances
  }
  process(amount, details) {
    const balance = this._cards[details.giftCardId] ?? 0;
    if (balance < amount) {
      console.log(`    [GiftCardStrategy] Insufficient gift card balance: $${balance} < $${amount}`);
      return { error: 'Insufficient gift card balance', status: 'FAILED' };
    }
    this._cards[details.giftCardId] -= amount;
    console.log(`    [GiftCardStrategy] Gift card ${details.giftCardId} charged $${amount}. Remaining: $${this._cards[details.giftCardId]}`);
    return { transactionId: `gc_${Date.now()}`, method: 'GIFT_CARD', amount, status: 'COMPLETED' };
  }
  refund(transactionId) {
    console.log(`    [GiftCardStrategy] Crediting gift card for ${transactionId}...`);
    return { refunded: true };
  }
}

// ─────────────────────────────────────────
// AFTER — PaymentService (Strategy-based Facade)
// ─────────────────────────────────────────
class PaymentServiceAfter {
  constructor() {
    this._strategies = {
      'CASH':        new CashStrategy(),
      'CREDIT_CARD': new StripeCardStrategy(),
      'DEBIT_CARD':  new StripeCardStrategy(),   // same Stripe strategy
      'MOBILE_PAY':  new MobilePayStrategy(),
      'GIFT_CARD':   new GiftCardStrategy(),
    };
  }

  createPayment(data) {
    const strategy = this._strategies[data.method];
    if (!strategy) return { error: `Unknown payment method: ${data.method}` };

    console.log(`  [PaymentService-AFTER] Delegating $${data.amount} to ${data.method} strategy...`);
    const result = strategy.process(data.amount, data);
    if (result.error) return result;
    // In real code: await prisma.payment.create({ data: { ...data, transactionId: result.transactionId } })
    return { id: `pay_${Date.now()}`, ...result };
  }
}

// ─────────────────────────────────────────
// Demo
// ─────────────────────────────────────────
console.log('\n===== EVOLUTION 3: MULTIPLE PAYMENT METHODS (Strategy Pattern) =====\n');

const beforeSvc = new PaymentServiceBefore();
const afterSvc  = new PaymentServiceAfter();

console.log('--- BEFORE: All methods use same code path ---');
console.log('Cash payment:');
console.log(' ', beforeSvc.createPayment({ method: 'CASH', amount: 45.50 }));
console.log('Card payment:');
console.log(' ', beforeSvc.createPayment({ method: 'CREDIT_CARD', amount: 45.50 }));

console.log('\n--- AFTER: Each method delegates to its own Strategy ---\n');

const payments = [
  { method: 'CASH',        amount: 45.50 },
  { method: 'CREDIT_CARD', amount: 128.00, last4: '4242' },
  { method: 'MOBILE_PAY',  amount: 32.75 },
  { method: 'GIFT_CARD',   amount: 60.00, giftCardId: 'GC-001' },
  { method: 'GIFT_CARD',   amount: 200.00, giftCardId: 'GC-002' }, // insufficient
];

for (const p of payments) {
  console.log(`Payment — method: ${p.method}, amount: $${p.amount}`);
  const result = afterSvc.createPayment(p);
  console.log('  Result:', result, '\n');
}
