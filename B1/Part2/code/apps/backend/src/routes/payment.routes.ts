import { Router } from 'express';
import { PaymentService } from '../services/payment.service';
import { authorize } from '../middleware/auth';

const router = Router();
const paymentService = new PaymentService();

// Removed intent route
// Create payment
router.post('/', async (req, res, next) => {
  try {
    const payment = await paymentService.createPayment(req.body);
    res.status(201).json(payment);
  } catch (error) {
    next(error);
  }
});

// Confirm payment
router.post('/:id/confirm', async (req, res, next) => {
  try {
    const payment = await paymentService.confirmPayment(req.params.id);
    res.json(payment);
  } catch (error) {
    next(error);
  }
});

// Process refund
router.post('/:id/refund', authorize(['ADMIN', 'MANAGER']), async (req, res, next) => {
  try {
    const { amount } = req.body;
    const refund = await paymentService.processRefund(req.params.id, amount);
    res.json(refund);
  } catch (error) {
    next(error);
  }
});

// Split bill
router.post('/split', async (req, res, next) => {
  try {
    const { orderId, splits } = req.body;
    const payments = await paymentService.splitBill(orderId, splits);
    res.json(payments);
  } catch (error) {
    next(error);
  }
});

// Get payments for order
router.get('/order/:orderId', async (req, res, next) => {
  try {
    const payments = await paymentService.getPaymentsByOrder(req.params.orderId);
    res.json(payments);
  } catch (error) {
    next(error);
  }
});

export default router;
