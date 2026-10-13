import { PrismaClient, EmployeeRole, Prisma } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

export class EmployeeService {
  async getEmployees(restaurantId: string) {
    return prisma.employee.findMany({
      where: { restaurantId },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        role: true,
        isActive: true,
        phone: true,
        createdAt: true,
        updatedAt: true,
      },
      orderBy: { lastName: 'asc' },
    });
  }

  async getEmployee(id: string) {
    return prisma.employee.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        role: true,
        isActive: true,
        phone: true,
        createdAt: true,
        updatedAt: true,
      },
    });
  }

  async createEmployee(data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    restaurantId: string;
    role: string;
    phone?: string;
  }) {
    const existingEmployee = await prisma.employee.findUnique({
      where: { email: data.email },
    });

    if (existingEmployee) {
      throw new Error('Employee with this email already exists');
    }

    const hashedPassword = await bcrypt.hash(data.password, 10);

    const employee = await prisma.employee.create({
      data: {
        email: data.email,
        passwordHash: hashedPassword,
        firstName: data.firstName,
        lastName: data.lastName,
        restaurantId: data.restaurantId,
        role: data.role as EmployeeRole,
        phone: data.phone,
        isActive: true,
        pin: '0000', // Default pin
      },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        role: true,
        isActive: true,
        phone: true,
        createdAt: true,
      },
    });

    return employee;
  }

  async updateEmployee(id: string, data: any) {
    if (data.password) {
      data.passwordHash = await bcrypt.hash(data.password, 10);
      delete data.password;
    }

    return prisma.employee.update({
      where: { id },
      data,
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        role: true,
        isActive: true,
        phone: true,
        updatedAt: true,
      },
    });
  }

  async deactivateEmployee(id: string) {
    return prisma.employee.update({
      where: { id },
      data: { isActive: false },
    });
  }

  async clockIn(employeeId: string) {
    const activeShift = await prisma.timeEntry.findFirst({
      where: {
        employeeId,
        clockOut: null,
      },
    });

    if (activeShift) {
      throw new Error('Employee already clocked in');
    }

    return prisma.timeEntry.create({
      data: {
        employeeId,
        clockIn: new Date(),
      },
    });
  }

  async clockOut(employeeId: string) {
    const activeShift = await prisma.timeEntry.findFirst({
      where: {
        employeeId,
        clockOut: null,
      },
    });

    if (!activeShift) {
      throw new Error('No active shift found');
    }

    const clockOut = new Date();
    const hoursWorkedStr = ((clockOut.getTime() - activeShift.clockIn.getTime()) / (1000 * 60 * 60)).toFixed(2);
    
    return prisma.timeEntry.update({
      where: { id: activeShift.id },
      data: {
        clockOut,
        hoursWorked: new Prisma.Decimal(hoursWorkedStr),
      },
    });
  }

  async getEmployeeShifts(employeeId: string, startDate?: Date, endDate?: Date) {
    return prisma.timeEntry.findMany({
      where: {
        employeeId,
        clockIn: {
          gte: startDate,
          lte: endDate,
        },
      },
      orderBy: { clockIn: 'desc' },
    });
  }

  async getActiveShifts(restaurantId: string) {
    return prisma.timeEntry.findMany({
      where: {
        employee: { restaurantId },
        clockOut: null,
      },
      include: {
        employee: {
          select: {
            firstName: true,
            lastName: true,
            role: true,
          },
        },
      },
    });
  }
}