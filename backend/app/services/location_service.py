from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.database import Property
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class LocationService:
    def get_nearby_properties(self, db: Session, lat: float, lon: float, radius: int = 50) -> List[Property]:
        """Get properties within radius (meters) of coordinates"""
        try:
            # Create a point geometry from the coordinates
            point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
            
            # Query properties within radius using PostGIS ST_DWithin
            properties = db.query(Property).filter(
                func.ST_DWithin(
                    Property.location,
                    point,
                    radius,  # radius in meters
                    use_spheroid=True  # use spheroid for more accurate distance calculation
                )
            ).all()
            
            logger.info(f"Found {len(properties)} properties within {radius}m of ({lat}, {lon})")
            return properties
        except Exception as e:
            logger.error(f"Error querying nearby properties: {str(e)}")
            raise
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Validate GPS coordinates are within reasonable bounds"""
        try:
            # Check if coordinates are within valid ranges
            if not (-90 <= lat <= 90):
                logger.warning(f"Invalid latitude: {lat}")
                return False
            if not (-180 <= lon <= 180):
                logger.warning(f"Invalid longitude: {lon}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error validating coordinates: {str(e)}")
            return False
    
    def create_point(self, lat: float, lon: float) -> Optional[func.ST_Point]:
        """Create a PostGIS point from coordinates"""
        try:
            if not self.validate_coordinates(lat, lon):
                return None
            return func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        except Exception as e:
            logger.error(f"Error creating point: {str(e)}")
            return None 