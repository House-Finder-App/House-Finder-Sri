import { Request, Response } from 'express';
import exifr from 'exifr';
import { Multer } from 'multer';
import { processImage } from '../services/imageService';

// Extend Express Request type to include file
interface MulterRequest extends Request {
  file?: Express.Multer.File;
}

export const uploadImage = async (req: MulterRequest, res: Response) => {
  try {
    let location = null;
    if (req.file && req.file.buffer) {
      // Try to extract GPS from image metadata
      const exif = await exifr.gps(req.file.buffer);
      if (exif && exif.latitude && exif.longitude) {
        location = { lat: exif.latitude, lng: exif.longitude };
      }
    }
    // Fallback: use location from request body
    if (!location && req.body && req.body.lat && req.body.lng) {
      location = { lat: parseFloat(req.body.lat), lng: parseFloat(req.body.lng) };
    }
    if (!location) {
      return res.status(400).json({ error: 'Location not found in image metadata or request body.' });
    }
    if (!req.file || !req.file.buffer) {
      return res.status(400).json({ error: 'No image file uploaded.' });
    }
    // Call house detection service
    const detectionResult = await processImage(req.file.buffer, location);
    res.status(200).json({ message: 'Image uploaded successfully', location, detection: detectionResult });
  } catch (error) {
    res.status(500).json({ error: 'Failed to process image.' });
  }
}; 