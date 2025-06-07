import { Router } from 'express';
import multer from 'multer';
import { uploadImage } from '../controllers/imageController';

const router = Router();

// Configure multer for memory storage
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
  },
  fileFilter: (_req, file, cb) => {
    // Accept only image files
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'));
    }
  },
});

// Upload endpoint with multer middleware
router.post('/upload', upload.single('image'), uploadImage);

export default router; 