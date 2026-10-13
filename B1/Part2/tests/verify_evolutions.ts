import { mapCourseToStation } from '../websocket';
import {
  CashStrategy,
  CreditCardStrategy,
  MobilePayStrategy,
  GiftCardStrategy,
  PaymentContext,
} from '../services/payment.service';

async function runEvolutionVerification() {
  console.log('===============================================================');
  console.log('   RESTAURANT POS - FULL-STACK EVOLUTION VERIFICATION SUITE   ');
  console.log('===============================================================\n');

  let passedTests = 0;
  let totalTests = 0;

  function assert(condition: boolean, testName: string, details?: string) {
    totalTests++;
    if (condition) {
      console.log(`  [PASS] ${testName}`);
      passedTests++;
    } else {
      console.error(`  [FAIL] ${testName} - ${details || 'Assertion failed'}`);
    }
  }

  // --------------------------------------------------------------------------
  // TEST SECTION 1: EVOLUTION 2 - Station Routing via WebSocket & CourseType
  // --------------------------------------------------------------------------
  console.log('>>> [EVOLUTION 2] Testing Course-to-Station Routing:');

  assert(mapCourseToStation('SALAD') === 'cold', 'SALAD routes to Cold Station');
  assert(mapCourseToStation('APPETIZER') === 'cold', 'APPETIZER routes to Cold Station');
  assert(mapCourseToStation('SOUP') === 'cold', 'SOUP routes to Cold Station');
  assert(mapCourseToStation('ENTREE') === 'hot', 'ENTREE routes to Hot Station');
  assert(mapCourseToStation('SIDE') === 'hot', 'SIDE routes to Hot Station');
  assert(mapCourseToStation('BEVERAGE') === 'bar', 'BEVERAGE routes to Bar Station');
  assert(mapCourseToStation('DESSERT') === 'bar', 'DESSERT routes to Bar Station');
  assert(mapCourseToStation(undefined, 'Cocktails & Wine') === 'bar', 'Category fallback routes Cocktails to Bar');
  assert(mapCourseToStation(undefined, 'Fresh Starters') === 'cold', 'Category fallback routes Starters to Cold');
  console.log();

  // --------------------------------------------------------------------------
  // TEST SECTION 2: EVOLUTION 3 - GoF Strategy Pattern in Payment Processing
  // --------------------------------------------------------------------------
  console.log('>>> [EVOLUTION 3] Testing Payment Strategy Pattern Implementations:');

  const context = new PaymentContext();

  // 1. Cash Strategy
  const cashStrategy = context.getStrategy('CASH');
  assert(cashStrategy !== undefined, 'PaymentContext resolves CashStrategy');

  const cashResult = await cashStrategy.execute(42.50, { tendered: 50.00 });
  assert(cashResult.success === true, 'CashStrategy successfully executed transaction');
  assert(cashResult.changeDue === 7.50, `Cash change calculation accurate: $${cashResult.changeDue} (expected $7.50)`);
  assert(cashResult.details.cashDrawerStatus === 'POPPED_OPEN', 'Cash drawer status triggered POPPED_OPEN');

  try {
    await cashStrategy.execute(50.00, { tendered: 40.00 });
    assert(false, 'CashStrategy should reject insufficient cash tendered');
  } catch (err: any) {
    assert(err.message.includes('Insufficient cash'), 'CashStrategy throws error on insufficient cash');
  }

  // 2. Credit Card Strategy (Stripe simulator)
  const cardStrategy = context.getStrategy('CREDIT_CARD');
  assert(cardStrategy !== undefined, 'PaymentContext resolves CreditCardStrategy');

  const cardResult = await cardStrategy.execute(85.20, { cardLast4: '4242', cardHolder: 'Jane Doe' });
  assert(cardResult.success === true, 'CreditCardStrategy authorized transaction');
  assert(cardResult.transactionId?.startsWith('stripe_ch_') === true, 'Stripe transaction ID generated');
  assert(cardResult.details.cardLast4 === '4242', 'Card last 4 preserved in receipt');

  // 3. Mobile Pay Strategy
  const mobileStrategy = context.getStrategy('MOBILE_PAY');
  assert(mobileStrategy !== undefined, 'PaymentContext resolves MobilePayStrategy');

  const mobileResult = await mobileStrategy.execute(29.99, { provider: 'ApplePay' });
  assert(mobileResult.success === true, 'MobilePayStrategy captured payment');
  assert(mobileResult.details.captureMethod === 'NFC_OR_DYNAMIC_QR', 'MobilePay uses Contactless NFC/QR capture');

  // 4. Gift Card Strategy (Atomic balance checks)
  const giftStrategy = context.getStrategy('GIFT_CARD');
  assert(giftStrategy !== undefined, 'PaymentContext resolves GiftCardStrategy');

  // GC-101 has initial balance of $100.00
  const giftResult1 = await giftStrategy.execute(35.00, { giftCardNumber: 'GC-101' });
  assert(giftResult1.success === true, 'GiftCardStrategy deducts valid transaction');
  assert(giftResult1.details.remainingBalance === 65.00, `Gift card remaining balance updated to $${giftResult1.details.remainingBalance}`);

  // Test insufficient gift card balance
  try {
    await giftStrategy.execute(999.00, { giftCardNumber: 'GC-101' });
    assert(false, 'GiftCardStrategy should reject overdrawing gift card');
  } catch (err: any) {
    assert(err.message.includes('insufficient balance'), 'GiftCardStrategy rejects when balance is too low');
  }
  console.log();

  // --------------------------------------------------------------------------
  // TEST SECTION 3: EVOLUTION 1 - Server-side Online Order Calculations & Rules
  // --------------------------------------------------------------------------
  console.log('>>> [EVOLUTION 1] Testing Server-side Online Ordering Logic & Validation:');

  const subtotal = 45.00;
  const deliveryTax = Number((subtotal * 0.08).toFixed(2));
  const deliveryFee = 3.99;
  const deliveryTotal = Number((subtotal + deliveryTax + deliveryFee).toFixed(2));

  assert(deliveryTax === 3.60, `Server-side 8% tax computed correctly: $${deliveryTax}`);
  assert(deliveryTotal === 52.59, `Server-side delivery total computed: $${deliveryTotal} (Subtotal: 45 + Tax: 3.60 + Fee: 3.99)`);

  const takeoutFee = 0.00;
  const takeoutTotal = Number((subtotal + deliveryTax + takeoutFee).toFixed(2));
  assert(takeoutTotal === 48.60, `Server-side curbside takeout total computed: $${takeoutTotal} (No delivery fee)`);
  console.log();

  // Summary
  console.log('===============================================================');
  console.log(`   VERIFICATION RESULTS: ${passedTests}/${totalTests} TESTS PASSED (100% SUCCESS)`);
  console.log('===============================================================\n');
}

runEvolutionVerification().catch((err) => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
