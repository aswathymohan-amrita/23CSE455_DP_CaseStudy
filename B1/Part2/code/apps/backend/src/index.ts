import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { createServer } from 'http';
import { Server } from 'socket.io';
import dotenv from 'dotenv';
import { PrismaClient } from '@prisma/client';
import tableRoutes from './routes/table.routes';
import orderRoutes from './routes/order.routes';
import menuRoutes from './routes/menu.routes';
import authRoutes from './routes/auth.routes';
import employeeRoutes from './routes/employee.routes';
import inventoryRoutes from './routes/inventory.routes';
import analyticsRoutes from './routes/analytics.routes';
import paymentRoutes from './routes/payment.routes';
import { errorHandler } from './middleware/errorHandler';
import { authenticate } from './middleware/auth';
import { setupWebSocket } from './websocket';
import { OrderService } from './services/order.service';
import { MenuService } from './services/menu.service';

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true,
  },
});

export const prisma = new PrismaClient();
const orderService = new OrderService();
const menuService = new MenuService();

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Evolution 1: Public Online Ordering Endpoints (No staff authentication required)
app.post('/api/orders/online', async (req, res, next) => {
  try {
    const order = await orderService.createOnlineOrder(req.body);
    res.status(201).json(order);
  } catch (error) {
    next(error);
  }
});

app.get('/api/menu/public', async (req, res, next) => {
  try {
    const restaurant = await prisma.restaurant.findFirst();
    const menu = restaurant ? await menuService.getMenuByRestaurant(restaurant.id) : [];
    res.json(menu);
  } catch (error) {
    next(error);
  }
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/payments', paymentRoutes); // Evolution 3: Mounted payment routes with Strategy pattern
app.use('/api/tables', authenticate, tableRoutes);
app.use('/api/orders', authenticate, orderRoutes);
app.use('/api/menu', authenticate, menuRoutes);
app.use('/api/employees', authenticate, employeeRoutes);
app.use('/api/inventory', authenticate, inventoryRoutes);
app.use('/api/analytics', authenticate, analyticsRoutes);

// WebSocket setup
setupWebSocket(io);

// Error handling
app.use(errorHandler);

const PORT = process.env.PORT || 3000;

httpServer.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server');
  await prisma.$disconnect();
  httpServer.close(() => {
    console.log('HTTP server closed');
  });
});

export { io };
