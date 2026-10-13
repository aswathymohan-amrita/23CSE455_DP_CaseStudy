import { PrismaClient, PaymentMethod, PaymentStatus } from '@prisma/client';
import { getIO } from '../websocket';

const prisma = new PrismaClient();

// ============================================================================
// Evolution 3: GoF Strategy Pattern for Payment Processing
// ============================================================================

export interface PaymentExecutionResult {
  success: boolean;
  method: PaymentMethod;
  amount: number;
  transactionId?: string;
  changeDue?: number;
  details: Record<string, any>;
  errorMessage?: string;
}

export interface IPaymentStrategy {
  readonly method: PaymentMethod;
  execute(amount: number, details: any): Promise<PaymentExecutionResult>;
}

// 1. Concrete Strategy: Cash Tendered & Change Calculation
export class CashStrategy implements IPaymentStrategy {
  readonly method: PaymentMethod = 'CASH';

  async execute(amount: number, details: any): Promise<PaymentExecutionResult> {
    const tendered = Number(details?.tendered ?? amount);
    if (isNaN(tendered) || tendered < amount) {
      throw new Error(`Insufficient cash tendered. Total is $${amount.toFixed(2)}, but received $${tendered.toFixed(2)}.`);
    }

    const changeDue = Number((tendered - amount).toFixed(2));
    return {
      success: true,
      method: 'CASH',
      amount,
      changeDue,
      transactionId: `CASH-DRAWER-${Date.now().toString().slice(-6)}`,
      details: {
        tendered,
        changeDue,
        cashDrawerStatus: 'POPPED_OPEN',
        receiptNumber: `CASH-REC-${Math.floor(Math.random() * 90000 + 10000)}`,
      },
    };
  }
}

// 2. Concrete Strategy: Credit/Debit Card via Stripe Simulator
export class CreditCardStrategy implements IPaymentStrategy {
  readonly method: PaymentMethod = 'CREDIT_CARD';

  async execute(amount: number, details: any): Promise<PaymentExecutionResult> {
    const cardLast4 = details?.cardLast4 || details?.cardNumber?.slice(-4) || '4242';
    const cardHolder = details?.cardHolder || 'Valued Customer';
    const txnId = `stripe_ch_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;

    return {
      success: true,
      method: 'CREDIT_CARD',
      amount,
      transactionId: txnId,
      details: {
        cardHolder,
        cardLast4,
        brand: 'Visa/Mastercard',
        gateway: 'Stripe Secure Simulator',
        authCode: `AUTH-${Math.floor(Math.random() * 900000 + 100000)}`,
        status: 'SUCCEEDED',
      },
    };
  }
}

// 3. Concrete Strategy: Contactless Mobile Pay / Dynamic QR
export class MobilePayStrategy implements IPaymentStrategy {
  readonly method: PaymentMethod = 'MOBILE_PAY';

  async execute(amount: number, details: any): Promise<PaymentExecutionResult> {
    const provider = details?.provider || 'ApplePay / GoogleWallet / UPI';
    const qrReference = `QR_POS_${Date.now().toString().slice(-6)}`;

    return {
      success: true,
      method: 'MOBILE_PAY',
      amount,
      transactionId: qrReference,
      details: {
        provider,
        qrReference,
        captureMethod: 'NFC_OR_DYNAMIC_QR',
        status: 'VERIFIED_INSTANT',
      },
    };
  }
}

// 4. Concrete Strategy: Gift Card with Atomic Balance Validation
export class GiftCardStrategy implements IPaymentStrategy {
  readonly method: PaymentMethod = 'GIFT_CARD';
  private static giftCardLedger: Map<string, number> = new Map([
    ['GC-101', 100.0],
    ['GC-102', 25.0],
    ['GC-500', 50.0],
    ['GC-999', 0.0],
  ]);

  async execute(amount: number, details: any): Promise<PaymentExecutionResult> {
    const cardCode = details?.giftCardNumber || details?.cardCode || 'GC-101';
    const currentBalance = GiftCardStrategy.giftCardLedger.get(cardCode) ?? 0;

    if (currentBalance < amount) {
      throw new Error(`Gift Card ${cardCode} has insufficient balance ($${currentBalance.toFixed(2)}). Required: $${amount.toFixed(2)}.`);
    }

    const remainingBalance = Number((currentBalance - amount).toFixed(2));
    GiftCardStrategy.giftCardLedger.set(cardCode, remainingBalance);

    return {
      success: true,
      method: 'GIFT_CARD',
      amount,
      transactionId: `GC-TXN-${Date.now().toString().slice(-6)}`,
      details: {
        giftCardNumber: cardCode,
        originalBalance: currentBalance,
        remainingBalance,
        status: 'DEDUCTED',
      },
    };
  }
}

// Payment Context orchestrating strategies
export class PaymentContext {
  private strategies: Map<PaymentMethod, IPaymentStrategy> = new Map();

  constructor() {
    this.registerStrategy(new CashStrategy());
    this.registerStrategy(new CreditCardStrategy());
    this.registerStrategy(new MobilePayStrategy());
    this.registerStrategy(new GiftCardStrategy());
  }

  registerStrategy(strategy: IPaymentStrategy) {
    this.strategies.set(strategy.method, strategy);
  }

  getStrategy(method: PaymentMethod): IPaymentStrategy {
    const strategy = this.strategies.get(method);
    if (!strategy) {
      throw new Error(`Unsupported payment method: ${method}. Available: ${Array.from(this.strategies.keys()).join(', ')}`);
    }
    return strategy;
  }
}

// ============================================================================
// PaymentService coordinating persistence and strategy execution
// ============================================================================

export class PaymentService {
  private context = new PaymentContext();

  async processPayment(data: {
    orderId: string;
    amount: number;
    method: PaymentMethod | 'STRIPE_CARD'; // Allows frontend alias
    details?: any;
    splitNumber?: number;
  }) {
    // 1. Resolve normalized method (align frontend 'STRIPE_CARD' to Prisma 'CREDIT_CARD')
    const normalizedMethod: PaymentMethod =
      (data.method as string) === 'STRIPE_CARD' ? 'CREDIT_CARD' : (data.method as PaymentMethod);

    // 2. Validate order
    const order = await prisma.order.findUnique({
      where: { id: data.orderId },
      include: {
        payments: true,
        items: { include: { menuItem: true } },
        table: true,
      },
    });

    if (!order) {
      throw new Error(`Order #${data.orderId} not found`);
    }

    if (order.status === 'COMPLETED') {
      throw new Error(`Order #${data.orderId} is already completed and paid`);
    }

    // 3. Select strategy and execute
    const strategy = this.context.getStrategy(normalizedMethod);
    const execution = await strategy.execute(data.amount, data.details);

    // 4. Persist Payment record
    const payment = await prisma.payment.create({
      data: {
        orderId: data.orderId,
        amount: data.amount,
        method: normalizedMethod,
        status: 'COMPLETED',
        splitNumber: data.splitNumber,
        transactionId: execution.transactionId,
        processedAt: new Date(),
      },
    });

    // 5. Check if order is fully settled
    const allPayments = await prisma.payment.findMany({
      where: { orderId: data.orderId, status: 'COMPLETED' },
    });
    const totalPaid = allPayments.reduce((sum, p) => sum + Number(p.amount), 0);
    const orderTotal = Number(order.total) > 0 ? Number(order.total) : await this.calculateOrderTotal(order.id);

    let orderUpdated = false;
    if (totalPaid >= orderTotal - 0.01) {
      await prisma.order.update({
        where: { id: order.id },
        data: { status: 'COMPLETED', completedAt: new Date() },
      });

      if (order.tableId) {
        await prisma.table.update({
          where: { id: order.tableId },
          data: { status: 'DIRTY' },
        });
      }
      orderUpdated = true;
    }

    // 6. Real-time notifications
    const io = getIO();
    if (io) {
      io.to(`restaurant:${order.restaurantId}`).emit('payment:completed', {
        payment,
        execution,
        orderFullySettled: orderUpdated,
      });
      if (orderUpdated) {
        io.to(`restaurant:${order.restaurantId}`).emit('order:updated', {
          id: order.id,
          status: 'COMPLETED',
        });
      }
    }

    return {
      payment,
      execution,
      orderFullySettled: orderUpdated,
      totalPaid,
      orderTotal,
    };
  }

  async createPayment(data: {
    orderId: string;
    amount: number;
    method: PaymentMethod;
    splitNumber?: number;
    transactionId?: string;
  }) {
    return this.processPayment({
      orderId: data.orderId,
      amount: data.amount,
      method: data.method,
      splitNumber: data.splitNumber,
      details: { transactionId: data.transactionId },
    });
  }

  async confirmPayment(paymentId: string) {
    const payment = await prisma.payment.update({
      where: { id: paymentId },
      data: {
        status: 'COMPLETED',
        processedAt: new Date(),
      },
    });

    const order = await prisma.order.findUnique({
      where: { id: payment.orderId },
      include: { payments: true },
    });

    if (order) {
      const totalPaid = order.payments
        .filter((p) => p.status === 'COMPLETED')
        .reduce((sum, p) => sum + Number(p.amount), 0);

      const orderTotal = await this.calculateOrderTotal(order.id);

      if (totalPaid >= orderTotal) {
        await prisma.order.update({
          where: { id: order.id },
          data: { status: 'COMPLETED', completedAt: new Date() },
        });
      }
    }

    return payment;
  }

  async processRefund(paymentId: string, _amount?: number) {
    const payment = await prisma.payment.findUnique({
      where: { id: paymentId },
    });

    if (!payment) {
      throw new Error('Payment not found');
    }

    await prisma.payment.update({
      where: { id: paymentId },
      data: { status: 'REFUNDED' },
    });

    return { success: true };
  }

  async splitBill(orderId: string, splits: Array<{ amount: number; method?: PaymentMethod }>) {
    const order = await prisma.order.findUnique({
      where: { id: orderId },
      include: { items: { include: { menuItem: true } } },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const total = await this.calculateOrderTotal(orderId);
    const splitTotal = splits.reduce((sum, split) => sum + split.amount, 0);

    if (Math.abs(splitTotal - total) > 0.01) {
      throw new Error(`Split amounts ($${splitTotal.toFixed(2)}) do not match order total ($${total.toFixed(2)})`);
    }

    const results = [];
    for (let i = 0; i < splits.length; i++) {
      const s = splits[i];
      const res = await this.processPayment({
        orderId,
        amount: s.amount,
        method: s.method || 'CREDIT_CARD',
        splitNumber: i + 1,
      });
      results.push(res);
    }

    return results;
  }

  async calculateOrderTotal(orderId: string) {
    const order = await prisma.order.findUnique({
      where: { id: orderId },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
      },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const subtotal = order.items.reduce((sum, item) => {
      return sum + Number(item.menuItem.price) * item.quantity;
    }, 0);

    const tax = subtotal * 0.08;
    return subtotal + tax;
  }

  async getPaymentsByOrder(orderId: string) {
    return prisma.payment.findMany({
      where: { orderId },
      orderBy: { createdAt: 'desc' },
    });
  }
}
