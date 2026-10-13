import { PrismaClient, EmployeeRole } from '@prisma/client';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const prisma = new PrismaClient();

export class AuthService {
  private JWT_SECRET = process.env.JWT_SECRET || 'secret';
  private JWT_EXPIRES_IN = '15m';

  async register(data: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    restaurantId: string;
    role?: string;
  }) {
    const existingUser = await prisma.employee.findUnique({
      where: { email: data.email },
    });

    if (existingUser) {
      throw new Error('User already exists');
    }

    const hashedPassword = await bcrypt.hash(data.password, 10);

    const user = await prisma.employee.create({
      data: {
        email: data.email,
        passwordHash: hashedPassword,
        firstName: data.firstName,
        lastName: data.lastName,
        restaurantId: data.restaurantId,
        role: (data.role as EmployeeRole) || EmployeeRole.SERVER,
        isActive: true,
        pin: '1234',
      },
    });

    const { accessToken } = this.generateTokens({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    return {
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
      },
      accessToken,
    };
  }

  async login(email: string, password: string) {
    const user = await prisma.employee.findUnique({
      where: { email },
    });

    if (!user || !user.isActive) {
      throw new Error('Invalid credentials');
    }

    const isValidPassword = await bcrypt.compare(password, user.passwordHash);

    if (!isValidPassword) {
      throw new Error('Invalid credentials');
    }

    const { accessToken } = this.generateTokens({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    return {
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
      },
      accessToken,
    };
  }

  async verifyToken(token: string) {
    try {
      const decoded = jwt.verify(token, this.JWT_SECRET) as any;
      const user = await prisma.employee.findUnique({
        where: { id: decoded.id },
      });

      if (!user || !user.isActive) {
        throw new Error('User not found');
      }

      return {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
      };
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  private generateTokens(payload: { id: string; email: string; role: string }) {
    const accessToken = jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN as jwt.SignOptions['expiresIn'],
    });

    return { accessToken };
  }
}