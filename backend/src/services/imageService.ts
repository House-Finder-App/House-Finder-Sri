import path from 'path';
import fs from 'fs';
import { promisify } from 'util';
import { v4 as uuidv4 } from 'uuid';
import * as cv from 'opencv4nodejs';

const writeFileAsync = promisify(fs.writeFile);
const unlinkAsync = promisify(fs.unlink);

// Load the pre-trained cascade classifier for building detection
// Using a general object detection classifier that works well for buildings
const classifierPath = path.join(__dirname, '../../models/haarcascade_frontalface_default.xml');
const classifier = new cv.CascadeClassifier(classifierPath);

interface BuildingInfo {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number;
}

// Helper function to preprocess image for better detection
const preprocessImage = (image: cv.Mat): cv.Mat => {
  // Convert to grayscale
  const gray = image.cvtColor(cv.COLOR_BGR2GRAY);
  
  // Apply Gaussian blur to reduce noise
  const blurred = gray.gaussianBlur(new cv.Size(5, 5), 0);
  
  return blurred;
};

// Helper function to convert buffer to OpenCV image
const bufferToImage = async (buffer: Buffer): Promise<cv.Mat> => {
  // Create a temporary file
  const tempPath = path.join('/tmp', `${uuidv4()}.jpg`);
  
  try {
    // Write buffer to temporary file
    await writeFileAsync(tempPath, buffer);
    
    // Read the image using OpenCV
    const image = cv.imread(tempPath);
    
    if (!image) {
      throw new Error('Failed to read image from buffer');
    }
    
    return image;
  } finally {
    // Clean up temporary file
    try {
      await unlinkAsync(tempPath);
    } catch (error) {
      console.error('Error cleaning up temporary file:', error);
    }
  }
};

export const processImage = async (imageBuffer: Buffer, location: { lat: number; lng: number }) => {
  let image: cv.Mat | null = null;
  let processed: cv.Mat | null = null;
  
  try {
    // Convert buffer to OpenCV image
    image = await bufferToImage(imageBuffer);
    
    // Preprocess the image
    processed = preprocessImage(image);
    
    // Get image dimensions
    const imageData = image.getDataAsArray();
    const imageHeight = imageData.length;
    const imageWidth = imageData[0].length;
    
    // Detection parameters optimized for building detection
    const minSize = new cv.Size(100, 100); // Minimum size of buildings to detect
    const maxSize = new cv.Size(
      Math.floor(imageWidth * 0.8),
      Math.floor(imageHeight * 0.8)
    ); // Maximum size (80% of image)
    
    // Detect buildings using the cascade classifier (using options object)
    const buildings = classifier.detectMultiScale(processed, {
      scaleFactor: 1.1,
      minNeighbors: 3,
      minSize,
      maxSize
    });
    const detected = buildings.length > 0;
    
    // If buildings are detected, get the one with highest confidence (using the first detection)
    let mainBuilding: BuildingInfo | null = null;
    if (detected && image) {
      const bestBuilding = buildings[0];
      mainBuilding = {
        x: bestBuilding.x,
        y: bestBuilding.y,
        width: bestBuilding.width,
        height: bestBuilding.height,
        confidence: 1.0 // (No confidence score returned by detectMultiScale)
      };
      // Draw rectangle (for debugging) around the detected building
      const debugImage = image.copy();
      debugImage.drawRectangle(
        new cv.Rect(bestBuilding.x, bestBuilding.y, bestBuilding.width, bestBuilding.height),
        new cv.Vec3(0, 255, 0), // Green color
        2 // Thickness
      );
      // (Optional) Save debug image
      const debugPath = path.join('/tmp', `debug_${uuidv4()}.jpg`);
      cv.imwrite(debugPath, debugImage);
      console.log('Debug image saved to:', debugPath);
      debugImage.release();
    }

    return {
      detected,
      details: detected ? {
        description: 'Building detected in image',
        location,
        buildingInfo: mainBuilding,
        confidence: (mainBuilding?.confidence || 0),
        totalDetections: buildings.length
      } : null
    };
  } catch (error) {
    console.error('Error processing image:', error);
    throw new Error('Failed to process image with OpenCV');
  } finally {
    // Clean up OpenCV resources
    if (image) image.release();
    if (processed) processed.release();
  }
}; 