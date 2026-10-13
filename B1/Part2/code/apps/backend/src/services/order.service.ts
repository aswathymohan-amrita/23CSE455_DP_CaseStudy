import { PrismaClient, OrderStatus, OrderItemStatus } from '@prisma/client';
import { mapCourseToStation, emitKitchenStationItem, getIO } from '../websocket';

const prisma = new PrismaClient();

export class OrderService {
  async createOrder(data: {
    tableId: string;
    customerId?: string;
    items: Array<{
      menuItemId: string;
      quantity: number;
      notes?: string;
      modifiers?: any;
    }>;
    notes?: string;
  }) {
    const table = await prisma.table.findUnique({
      where: { id: data.tableId },
      include: { floorPlan: true },
    });

    if (!table) {
      throw new Error('Table not found');
    }

    const itemIds = data.items.map(i => i.menuItemId);
    const menuItems = await prisma.menuItem.findMany({
      where: { id: { in: itemIds } }
    });
    const itemMap = new Map(menuItems.map(m => [m.id, m]));

    const order = await prisma.order.create({
      data: {
        tableId: data.tableId,
        restaurantId: table.floorPlan.restaurantId,
        status: 'OPEN',
        customerCount: 1, // Defaulting as required
        notes: data.notes,
        type: 'DINE_IN',
        serverId: 'default', // Since original request had no serverId, just provide a dummy or logic later
        subtotal: 0,
        tax: 0,
        total: 0,
        items: {
          create: data.items.map((item) => {
            const mi = itemMap.get(item.menuItemId);
            const price = Number(mi?.price || 0);
            return {
              menuItemId: item.menuItemId,
              quantity: item.quantity,
              unitPrice: price,
              total: price * item.quantity,
              specialInstructions: item.notes,
              status: 'PENDING',
            };
          }),
        },
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
    });

    // Update table status
    await prisma.table.update({
      where: { id: data.tableId },
      data: { status: 'OCCUPIED' },
    });

    // Emit WebSocket event
    getIO()?.to(`restaurant:${table.floorPlanId}`).emit('order:new', order);

    return order;
  }

  async getOrderById(id: string) {
    return prisma.order.findUnique({
      where: { id },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
        payments: true,
      },
    });
  }

  async getOrdersByTable(tableId: string) {
    return prisma.order.findMany({
      where: {
        tableId,
        status: { in: ['OPEN', 'IN_PROGRESS'] },
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async getActiveOrders(restaurantId: string) {
    return prisma.order.findMany({
      where: {
        table: {
          floorPlan: {
            restaurantId,
          },
        },
        status: { in: ['OPEN', 'IN_PROGRESS'] },
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async addItemsToOrder(orderId: string, items: Array<{
    menuItemId: string;
    quantity: number;
    notes?: string;
    modifiers?: any;
  }>) {
    const order = await prisma.order.findUnique({
      where: { id: orderId },
      include: { table: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const itemIds = items.map(i => i.menuItemId);
    const menuItems = await prisma.menuItem.findMany({
      where: { id: { in: itemIds } }
    });
    const itemMap = new Map(menuItems.map(m => [m.id, m]));

    const updatedOrder = await prisma.order.update({
      where: { id: orderId },
      data: {
        items: {
          create: items.map((item) => {
            const mi = itemMap.get(item.menuItemId);
            const price = Number(mi?.price || 0);
            return {
              menuItemId: item.menuItemId,
              quantity: item.quantity,
              unitPrice: price,
              total: price * item.quantity,
              specialInstructions: item.notes,
              status: 'PENDING',
            };
          }),
        },
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
    });

    getIO()?.to(`restaurant:${order.table.floorPlanId}`).emit('order:updated', updatedOrder);

    return updatedOrder;
  }

  async updateOrderItemStatus(itemId: string, status: OrderItemStatus) {
    const item = await prisma.orderItem.findUnique({
      where: { id: itemId },
      include: {
        order: {
          include: { table: true },
        },
      },
    });

    if (!item) {
      throw new Error('Order item not found');
    }

    const updatedItem = await prisma.orderItem.update({
      where: { id: itemId },
      data: { status },
    });

    getIO()?.to(`restaurant:${item.order.table.floorPlanId}`).emit('order:item:status:changed', {
      itemId,
      status,
      orderId: item.orderId,
    });

    return updatedItem;
  }

  async updateOrderStatus(orderId: string, status: OrderStatus) {
    const order = await prisma.order.findUnique({
      where: { id: orderId },
      include: { table: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const updatedOrder = await prisma.order.update({
      where: { id: orderId },
      data: { status },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
    });

    getIO()?.to(`restaurant:${order.table.floorPlanId}`).emit('order:updated', updatedOrder);

    return updatedOrder;
  }

  async completeOrder(orderId: string) {
    const order = await this.updateOrderStatus(orderId, 'COMPLETED');
    
    // Check if table has any other active orders
    const activeOrders = await prisma.order.count({
      where: {
        tableId: order.tableId,
        status: { in: ['OPEN', 'IN_PROGRESS'] },
      },
    });

    if (activeOrders === 0) {
      await prisma.table.update({
        where: { id: order.tableId },
        data: { status: 'DIRTY' },
      });
    }

    return order;
  }

  async cancelOrder(orderId: string, reason?: string) {
    const order = await prisma.order.findUnique({
      where: { id: orderId },
      include: { table: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const updatedOrder = await prisma.order.update({
      where: { id: orderId },
      data: {
        status: 'CANCELLED',
        notes: reason ? `${order.notes || ''}\nCancellation reason: ${reason}` : order.notes,
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
    });

    getIO()?.to(`restaurant:${order.table.floorPlanId}`).emit('order:updated', updatedOrder);

    return updatedOrder;
  }

  async getOrderTotal(orderId: string) {
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
      return sum + (Number(item.menuItem.price) * item.quantity);
    }, 0);

    const tax = subtotal * 0.08; // 8% tax
    const total = subtotal + tax;

    return {
      subtotal,
      tax,
      total,
      itemCount: order.items.reduce((sum, item) => sum + item.quantity, 0),
    };
  }

  async createOnlineOrder(data: {
    customerName: string;
    customerPhone: string;
    deliveryAddress?: string;
    orderType: 'DELIVERY' | 'TAKEOUT';
    items: Array<{
      menuItemId: string;
      quantity: number;
      notes?: string;
    }>;
  }) {
    // 1. Validation
    if (!data.customerName || data.customerName.trim().length === 0) {
      throw new Error('Customer full name is required');
    }
    if (!data.customerPhone || data.customerPhone.trim().length === 0) {
      throw new Error('Customer phone number is required');
    }
    if (data.orderType === 'DELIVERY' && (!data.deliveryAddress || data.deliveryAddress.trim().length === 0)) {
      throw new Error('Delivery address is required for delivery orders');
    }
    if (!data.items || !Array.isArray(data.items) || data.items.length === 0) {
      throw new Error('At least one item must be added to the order');
    }

    for (const item of data.items) {
      if (!item.menuItemId) throw new Error('Menu item ID is required for each item');
      if (!item.quantity || item.quantity <= 0) throw new Error('Quantity must be greater than 0');
    }

    // 2. Server-side pricing & item existence from trusted DB
    const itemIds = data.items.map((i) => i.menuItemId);
    const dbMenuItems = await prisma.menuItem.findMany({
      where: { id: { in: itemIds } },
      include: { category: true },
    });
    const itemMap = new Map(dbMenuItems.map((m) => [m.id, m]));

    for (const item of data.items) {
      const mi = itemMap.get(item.menuItemId);
      if (!mi) {
        throw new Error(`Menu item with ID ${item.menuItemId} does not exist`);
      }
      if (!mi.isAvailable || mi.is86d) {
        throw new Error(`Menu item "${mi.name}" is currently 86'd / unavailable`);
      }
    }

    // 3. Server-side totals calculation (Never trust client prices)
    let subtotal = 0;
    const orderItemsData = data.items.map((item) => {
      const mi = itemMap.get(item.menuItemId)!;
      const unitPrice = Number(mi.price);
      const lineTotal = Number((unitPrice * item.quantity).toFixed(2));
      subtotal += lineTotal;

      let course = 'ENTREE';
      const catName = mi.category?.name?.toUpperCase() || '';
      if (catName.includes('APPETIZER') || catName.includes('SALAD') || catName.includes('SOUP')) {
        course = 'APPETIZER';
      } else if (catName.includes('DESSERT')) {
        course = 'DESSERT';
      } else if (catName.includes('BEVERAGE') || catName.includes('DRINK')) {
        course = 'BEVERAGE';
      }

      return {
        menuItemId: item.menuItemId,
        quantity: item.quantity,
        unitPrice,
        total: lineTotal,
        course: course as any,
        specialInstructions: item.notes || null,
        status: 'PENDING' as any,
      };
    });

    subtotal = Number(subtotal.toFixed(2));
    const tax = Number((subtotal * 0.08).toFixed(2));
    const deliveryFee = data.orderType === 'DELIVERY' ? 3.99 : 0.00;
    const total = Number((subtotal + tax + deliveryFee).toFixed(2));

    // 4. Resolve Restaurant and Server context
    const restaurant = await prisma.restaurant.findFirst();
    const server = await prisma.employee.findFirst({ where: { role: 'SERVER' } }) || await prisma.employee.findFirst();

    const restaurantId = restaurant?.id || 'rest_default';
    const serverId = server?.id || 'emp_default';

    const customerNotes = `[Online ${data.orderType}] Customer: ${data.customerName.trim()} | Phone: ${data.customerPhone.trim()}${
      data.orderType === 'DELIVERY' ? ` | Address: ${data.deliveryAddress?.trim()}` : ' | Curbside Pickup'
    }`;

    // 5. Persist Order in DB
    const order = await prisma.order.create({
      data: {
        restaurantId,
        serverId,
        customerCount: 1,
        status: 'IN_PROGRESS',
        type: data.orderType === 'DELIVERY' ? 'DELIVERY' : 'TAKEOUT',
        subtotal,
        tax,
        total,
        notes: customerNotes,
        items: {
          create: orderItemsData,
        },
      },
      include: {
        items: {
          include: {
            menuItem: true,
          },
        },
        table: true,
      },
    });

    // 6. Real-time station routing and WebSocket dispatch
    const io = getIO();
    if (io) {
      io.to(`restaurant:${restaurantId}`).emit('order:new', order);
      io.to(`restaurant:${restaurantId}:kitchen`).emit('kitchen:order:new', order);

      // Route individual items to Cold, Hot, Bar stations
      for (const orderItem of order.items) {
        const station = mapCourseToStation(orderItem.course as any, orderItem.menuItem?.name);
        emitKitchenStationItem(io, restaurantId, {
          orderId: order.id,
          orderNumber: order.orderNumber,
          item: orderItem,
          station,
        });
      }
    }

    return order;
  }
}