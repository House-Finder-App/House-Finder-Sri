import cv2
import numpy as np
from PIL import Image, ExifTags
from transformers import CLIPProcessor, CLIPModel
import torch
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        logger.info("Initializing CLIP model...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        logger.info("CLIP model initialized successfully")
    
    def extract_location_from_exif(self, image_path: str) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates from image EXIF data"""
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            if not exif:
                return None

            for tag_id in ExifTags.TAGS:
                if ExifTags.TAGS[tag_id] == 'GPSInfo':
                    gps_info = exif.get(tag_id)
                    if not gps_info:
                        return None

                    lat_ref = gps_info.get(1, 'N')
                    lat = gps_info.get(2, (0, 0, 0))
                    lon_ref = gps_info.get(3, 'E')
                    lon = gps_info.get(4, (0, 0, 0))

                    lat = self._convert_to_degrees(lat)
                    lon = self._convert_to_degrees(lon)

                    if lat_ref == 'S':
                        lat = -lat
                    if lon_ref == 'W':
                        lon = -lon

                    return (lat, lon)
        except Exception as e:
            logger.error(f"Error extracting EXIF data: {str(e)}")
            return None

    def _convert_to_degrees(self, value: Tuple[float, float, float]) -> float:
        """Convert GPS coordinates to decimal degrees"""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Resize and normalize image for processing"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image at {image_path}")
            
            # Convert to RGB (CLIP expects RGB)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to CLIP's expected size
            image = cv2.resize(image, (224, 224))
            
            # Normalize
            image = image.astype(np.float32) / 255.0
            return image
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def extract_image_features(self, image_path: str) -> torch.Tensor:
        """Extract feature embeddings using CLIP"""
        try:
            image = Image.open(image_path)
            inputs = self.processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
            return image_features
        except Exception as e:
            logger.error(f"Error extracting image features: {str(e)}")
            raise
    
    def calculate_similarity(self, features1: torch.Tensor, features2: torch.Tensor) -> float:
        """Calculate cosine similarity between image features"""
        try:
            # Normalize features
            features1 = features1 / features1.norm(dim=-1, keepdim=True)
            features2 = features2 / features2.norm(dim=-1, keepdim=True)
            
            # Calculate cosine similarity
            similarity = torch.nn.functional.cosine_similarity(features1, features2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            raise 