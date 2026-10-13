import { Router } from 'express';
import { AuthService } from '../services/auth.service';

const router = Router();
const authService = new AuthService();

// Register new user
router.post('/register', async (req, res, next) => {
  try {
    const result = await authService.register(req.body);
    res.status(201).json(result);
  } catch (error) {
    next(error);
  }
});

// Login
router.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const result = await authService.login(email, password);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// Removed refresh and logout endpoints

// Verify token
router.get('/verify', async (req, res, next) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    const user = await authService.verifyToken(token);
    res.json({ user });
  } catch (error) {
    next(error);
  }
});

export default router;
