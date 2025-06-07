import { Router } from 'express';
import { findProperty } from '../controllers/propertyController';

const router = Router();

router.post('/find', findProperty);

export default router; 