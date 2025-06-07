import httpx
from typing import List, Dict, Optional
import logging
from datetime import datetime
from app.models.database import Property
import uuid

logger = logging.getLogger(__name__)

class ZillowService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.bridgedataoutput.com/api/v2"  # Zillow API endpoint
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_properties_by_location(self, lat: float, lon: float, radius: int = 50) -> List[Dict]:
        """Fetch properties from Zillow API by location"""
        try:
            async with httpx.AsyncClient() as client:
                # Note: This is a placeholder URL and parameters
                # You'll need to adjust based on actual Zillow API documentation
                response = await client.get(
                    f"{self.base_url}/properties",
                    headers=self.headers,
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "radius": radius,
                        "limit": 50
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                logger.info(f"Retrieved {len(data.get('properties', []))} properties from Zillow API")
                return data.get("properties", [])
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while fetching properties: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error fetching properties from Zillow: {str(e)}")
            raise
    
    def parse_property_data(self, property_data: Dict) -> Property:
        """Parse Zillow API response into our Property model"""
        try:
            return Property(
                id=uuid.uuid4(),
                zillow_id=str(property_data.get("id")),
                address=property_data.get("address", {}).get("oneLine", ""),
                location=f"POINT({property_data.get('longitude')} {property_data.get('latitude')})",
                zillow_url=property_data.get("url"),
                image_url=property_data.get("photos", [{}])[0].get("href"),
                price=property_data.get("price"),
                bedrooms=property_data.get("bedrooms"),
                bathrooms=property_data.get("bathrooms"),
                created_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error parsing property data: {str(e)}")
            raise
    
    async def get_property_details(self, zillow_id: str) -> Optional[Dict]:
        """Get detailed information for a specific property"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/properties/{zillow_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while fetching property details: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching property details: {str(e)}")
            return None 