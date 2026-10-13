import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class MenuService {
  async getMenuByRestaurant(restaurantId: string) {
    return prisma.category.findMany({
      where: { restaurantId },
      include: {
        menuItems: {
          where: { isAvailable: true },
        },
      },
      orderBy: { displayOrder: 'asc' },
    });
  }

  async getMenuItem(id: string) {
    return prisma.menuItem.findUnique({
      where: { id },
      include: {
        category: true,
      },
    });
  }

  async createMenuItem(data: {
    name: string;
    description?: string;
    price: number;
    categoryId: string;
    restaurantId: string;
    imageUrl?: string;
    preparationTime?: number;
    isAvailable?: boolean;
  }) {
    return prisma.menuItem.create({
      data: {
        name: data.name,
        description: data.description,
        price: data.price,
        categoryId: data.categoryId,
        restaurantId: data.restaurantId,
        imageUrl: data.imageUrl,
        preparationTime: data.preparationTime,
        isAvailable: data.isAvailable,
      },
    });
  }

  async updateMenuItem(id: string, data: any) {
    return prisma.menuItem.update({
      where: { id },
      data,
    });
  }

  async deleteMenuItem(id: string) {
    return prisma.menuItem.delete({
      where: { id },
    });
  }

  async createCategory(data: {
    name: string;
    restaurantId: string;
    displayOrder?: number;
  }) {
    return prisma.category.create({
      data: {
        name: data.name,
        restaurantId: data.restaurantId,
        displayOrder: data.displayOrder || 0,
      },
    });
  }

  async updateCategory(id: string, data: any) {
    return prisma.category.update({
      where: { id },
      data,
    });
  }

  async deleteCategory(id: string) {
    return prisma.category.delete({
      where: { id },
    });
  }
}