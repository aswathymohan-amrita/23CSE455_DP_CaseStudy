import { Server, Socket } from 'socket.io';
import * as jwt from 'jsonwebtoken';

interface SocketUser {
  id: string;
  email: string;
  role: string;
}

let ioInstance: Server | null = null;

export const getIO = (): Server | null => ioInstance;

export const setupWebSocket = (io: Server) => {
  ioInstance = io;
  // Authentication middleware for WebSocket
  io.use((socket: Socket, next) => {
    const token = socket.handshake.auth.token;
    
    if (!token) {
      return next(new Error('Authentication error'));
    }

    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret') as SocketUser;
      (socket as any).user = decoded;
      next();
    } catch (err) {
      next(new Error('Authentication error'));
    }
  });

  io.on('connection', (socket: Socket) => {
    const user = (socket as any).user as SocketUser;
    console.log(`User connected: ${user.email} (${socket.id})`);

    // Join restaurant room
    const restaurantId = socket.handshake.query.restaurantId as string;
    if (restaurantId) {
      socket.join(`restaurant:${restaurantId}`);
      console.log(`User ${user.email} joined restaurant ${restaurantId}`);
    }

    // Table status updates
    socket.on('table:update', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('table:updated', data);
    });

    socket.on('table:status', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('table:status:changed', data);
    });

    // Order events
    socket.on('order:created', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('order:new', data);
      // Notify kitchen
      io.to(`restaurant:${restaurantId}:kitchen`).emit('kitchen:order:new', data);
    });

    socket.on('order:updated', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('order:updated', data);
    });

    socket.on('order:item:status', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('order:item:status:changed', data);
      // Update server/host
      io.to(`restaurant:${restaurantId}:floor`).emit('order:item:ready', data);
    });

    // Kitchen display events
    socket.on('kitchen:join', () => {
      socket.join(`restaurant:${restaurantId}:kitchen`);
      console.log(`Kitchen display connected for restaurant ${restaurantId}`);
    });

    // Evolution 2: Station-specific subscription (Cold, Hot, Bar)
    socket.on('kitchen:station:join', (data: { station?: string }) => {
      const station = (data?.station || 'all').toLowerCase();
      socket.join(`restaurant:${restaurantId}:station:${station}`);
      socket.join(`restaurant:${restaurantId}:kitchen`);
      console.log(`Kitchen station display connected: ${station} for restaurant ${restaurantId}`);
    });

    socket.on('kitchen:item:complete', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('kitchen:item:completed', data);
    });

    socket.on('kitchen:station:item:status', (data: { orderId: string; itemId: string; status: string; station?: string }) => {
      io.to(`restaurant:${restaurantId}`).emit('kitchen:item:status:changed', data);
      if (data.status === 'READY') {
        io.to(`restaurant:${restaurantId}:floor`).emit('order:item:ready', data);
      }
    });

    // Payment events
    socket.on('payment:initiated', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('payment:processing', data);
    });

    socket.on('payment:completed', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('payment:success', data);
    });

    // Reservation events
    socket.on('reservation:created', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('reservation:new', data);
    });

    socket.on('reservation:updated', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('reservation:updated', data);
    });

    // Inventory alerts
    socket.on('inventory:low', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('inventory:alert', data);
    });

    // Employee clock in/out
    socket.on('employee:clock', (data) => {
      io.to(`restaurant:${restaurantId}`).emit('employee:status:changed', data);
    });

    // Disconnect
    socket.on('disconnect', () => {
      console.log(`User disconnected: ${user.email} (${socket.id})`);
    });
  });

  return io;
};

// Course to station mapping for Evolution 2
export const mapCourseToStation = (course?: string, categoryName?: string): 'cold' | 'hot' | 'bar' => {
  const c = course?.toUpperCase();
  if (c === 'SALAD' || c === 'APPETIZER' || c === 'SOUP') return 'cold';
  if (c === 'BEVERAGE' || c === 'DESSERT') return 'bar';
  if (c === 'ENTREE' || c === 'SIDE') return 'hot';

  const cat = (categoryName || '').toLowerCase();
  if (cat.includes('drink') || cat.includes('beverage') || cat.includes('dessert') || cat.includes('bar') || cat.includes('cocktail') || cat.includes('wine')) return 'bar';
  if (cat.includes('salad') || cat.includes('appetizer') || cat.includes('starter') || cat.includes('soup')) return 'cold';
  return 'hot';
};

// Helper functions to emit events from services
export const emitTableUpdate = (io: Server, restaurantId: string, data: any) => {
  io.to(`restaurant:${restaurantId}`).emit('table:updated', data);
};

export const emitOrderUpdate = (io: Server, restaurantId: string, data: any) => {
  io.to(`restaurant:${restaurantId}`).emit('order:updated', data);
  io.to(`restaurant:${restaurantId}:kitchen`).emit('kitchen:order:updated', data);
};

export const emitKitchenStationItem = (io: Server, restaurantId: string, payload: { orderId: string; orderNumber?: number; item: any; station: 'cold' | 'hot' | 'bar' }) => {
  // Emit to targeted station room
  io.to(`restaurant:${restaurantId}:station:${payload.station}`).emit('kitchen:station:item:new', payload);
  // Also emit to general kitchen room
  io.to(`restaurant:${restaurantId}:kitchen`).emit('kitchen:station:item:new', payload);
};

export const emitKitchenUpdate = (io: Server, restaurantId: string, data: any) => {
  io.to(`restaurant:${restaurantId}:kitchen`).emit('kitchen:updated', data);
  io.to(`restaurant:${restaurantId}:floor`).emit('order:item:ready', data);
};
