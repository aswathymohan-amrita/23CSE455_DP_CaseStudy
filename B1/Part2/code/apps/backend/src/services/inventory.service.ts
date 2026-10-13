import { PrismaClient } from '@prisma/client';
import { io } from '../index';

const prisma = new PrismaClient();

export class InventoryService {
  async getInventoryItems(restaurantId: string) {
    return prisma.inventoryItem.findMany({
      where: { restaurantId },
      orderBy: { name: 'asc' },
    });
  }

  async getInventoryItem(id: string) {
    return prisma.inventoryItem.findUnique({
      where: { id },
    });
  }

  async createInventoryItem(data: {
    name: string;
    restaurantId: string;
    unit: string;
    quantity: number;
    reorderPoint: number;
    costPerUnit: number;
  }) {
    const item = await prisma.inventoryItem.create({
      data: {
        name: data.name,
        restaurantId: data.restaurantId,
        unit: data.unit,
        quantity: data.quantity,
        reorderPoint: data.reorderPoint,
        costPerUnit: data.costPerUnit,
      },
    });

    if (item.quantity <= item.reorderPoint) {
      this.emitLowStockAlert(item);
    }

    return item;
  }

  async updateInventoryItem(id: string, data: any) {
    const item = await prisma.inventoryItem.update({
      where: { id },
      data,
    });

    if (item.quantity <= item.reorderPoint) {
      this.emitLowStockAlert(item);
    }

    return item;
  }

  async adjustStock(id: string, qty: number, reason?: string) {
    const item = await prisma.inventoryItem.findUnique({
      where: { id },
    });

    if (!item) {
      throw new Error('Inventory item not found');
    }

    const newQty = Number(item.quantity) + qty;
    
    const updatedItem = await prisma.inventoryItem.update({
      where: { id },
      data: {
        quantity: newQty,
      },
    });

    if (updatedItem.quantity <= updatedItem.reorderPoint) {
      this.emitLowStockAlert(updatedItem);
    }

    return updatedItem;
  }

  async getLowStockItems(restaurantId: string) {
    return prisma.inventoryItem.findMany({
      where: {
        restaurantId,
        quantity: {
          lte: prisma.inventoryItem.fields.reorderPoint,
        },
      },
      orderBy: { quantity: 'asc' },
    });
  }

  async deleteInventoryItem(id: string) {
    return prisma.inventoryItem.delete({
      where: { id },
    });
  }

  private emitLowStockAlert(item: any) {
    io?.to(`restaurant:${item.restaurantId}`).emit('inventory:alert', {
      itemId: item.id,
      name: item.name,
      quantity: item.quantity,
      reorderPoint: item.reorderPoint,
      message: `Low stock alert: ${item.name} is running low (${item.quantity} ${item.unit} remaining)`,
    });
  }
}